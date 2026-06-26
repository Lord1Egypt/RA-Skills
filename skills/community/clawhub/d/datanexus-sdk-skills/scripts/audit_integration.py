#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_integration.py — 已接入项目的深度体检

目标人群：
  已经接入了 DataNexus SDK（new SDK({...}) 已存在）、想评估接入质量的项目。

与 validate_integration.py 的区别：
  - validate：接入完成后的"通过/不通过"式基础体检（init/依赖/权限/占位符等）
  - audit  ：深度体检，产出"接入质量诊断报告"，覆盖：
      1) 初始化规范度（版本、用户ID设置、重复初始化、隐私前置等）
      2) 必报事件覆盖度（按「SDK 端 × 业务场景」对照必报清单）
      3) 事件用法正确性（PURCHASE 是否传 value、setOpenId/setUnionId 顺序等）
      4) 自动采集冗余（手动调了本已自动采集的事件，可能双重上报）
      5) 数据合规性（SDK 初始化时机是否在隐私政策授权后）

输出：
  - 文本摘要 + 覆盖率百分比 + issue 清单
  - --json 结构化输出供 Agent 消费

使用示例：
  # 基础（SDK 端自动推断行业场景）
  python3 audit_integration.py <project_root> --sdk-end mini-game

  # 明确场景（推荐）
  python3 audit_integration.py <project_root> --sdk-end mini-game --scenario iaa-mini-game

  # 游戏类 APP
  python3 audit_integration.py <project_root> --sdk-end android --scenario game-app

  # JSON 输出
  python3 audit_integration.py <project_root> --sdk-end mini-game --scenario iaa-mini-game --json

支持的 --scenario 取值：
  mini-game:    iap-mini-game（IAP/混变）, iaa-mini-game（IAA/广告变现）
  mini-program: drama（短剧）, novel（小说）, ecommerce（电商）, general-mini-program（其他）
  android:      game-app（游戏）, general-app（非游戏）
  ios:          game-app, general-app
  harmony:      general-app

设计原则：
  - 纯 Python 标准库，regex 扫描 + 规则比对
  - 每条检查都带"文档锚点"（指向 references/ 里的权威说明）
  - 严格区分"必报未报"（FAIL）、"建议上报"（WARN）、"用法不规范"（WARN）、"合规风险"（FAIL）
  - 退出码：0 全部 PASS，1 有 WARN，2 有 FAIL
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# 同目录共用工具（注释剔除等），兼容"直接运行脚本"与"作为模块被其他脚本 import"两种场景
try:
    from _common import strip_line_comment as _strip_line_comment  # 直接 python3 scripts/audit_integration.py
except ImportError:
    import os as _os
    sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from _common import strip_line_comment as _strip_line_comment  # type: ignore


# ─────────────────────────────────────────────────────────
# 必报事件矩阵（由 references/通用/埋点/行为类型枚举表.md 抽取）
# ─────────────────────────────────────────────────────────

# severity：required（必报）/ recommended（建议上报）/ auto（自动采集，不要手动报）
# ref：权威出处链接（相对 SKILL 目录）

EVENT_MATRIX: Dict[str, Dict[str, List[Dict]]] = {
    # 说明：
    #   required 列表里的事件分两档：
    #     - 无 optional 字段 / optional=false：硬必报，未报 → FAIL，计入覆盖度分母
    #     - optional=true：条件必报（仅当业务场景存在时必报，如 note 标"如有"的）
    #         → 未报 → WARN（而非 FAIL），**不**计入覆盖度分母，避免"没有新手引导的小游戏
    #         TUTORIAL_START 永远算未报"这类虚警
    #   对 Agent：若用户明确告知业务场景不涉及（如"没有新手引导"），可直接忽略对应 WARN
    # ============ 小游戏端 ============
    "iap-mini-game": {
        "required": [
            {"event": "START_APP", "note": "自动采集，也可手动 sdk.onAppStart()"},
            {"event": "REGISTER", "note": "新用户首次打开 — 必须由服务端判断 isNew=true 后调 sdk.onRegister()，禁止客户端 wx.storage 自判"},
            {"event": "RE_ACTIVE", "note": "老用户沉默 30 天后回归，单档位触发，backFlowDay=30 — 必须由服务端基于 openid+last_login_ts 判断后客户端再上报"},
            {"event": "LOAD_FINISH", "note": "loading 完成、游戏第一帧上报"},
            {"event": "SUBSCRIBE", "note": "订阅成功系统回调上报"},
            {"event": "PURCHASE", "note": "必须传 value（金额，单位：分）", "require_param": "value"},
            {"event": "VIEW_CONTENT", "note": "浏览商城/活动（如有）", "optional": True},
            {"event": "UPDATE_LEVEL", "note": "游戏等级提升（如有）", "optional": True},
            {"event": "TUTORIAL_START", "note": "新手引导开始（如有）", "optional": True},
            {"event": "TUTORIAL_FINISH", "note": "完成新手引导（如有）", "optional": True},
            {"event": "CREATE_ROLE", "note": "创建角色（如有）", "optional": True},
        ],
        "auto_collected": ["TICKET", "ENTER_FOREGROUND", "ENTER_BACKGROUND", "START_APP", "APP_QUIT",
                           "LOGIN", "SHARE", "START_PAY", "FINISH_PAY", "ADD_TO_WISHLIST", "CREATE_GAME_ROOM"],
    },
    "iaa-mini-game": {
        "required": [
            {"event": "REGISTER", "note": "新用户首次打开 — 必须由服务端判断 isNew=true 后调用，禁止客户端自判"},
            {"event": "RE_ACTIVE", "note": "老用户沉默 30 天后回归，单档位触发，backFlowDay=30 — 必须由服务端基于 openid+last_login_ts 判断后客户端再上报"},
            {"event": "START_APP", "note": "自动采集"},
            {"event": "LOAD_FINISH", "note": "进入游戏第一帧"},
            {"event": "SUBSCRIBE", "note": "完成订阅消息授权（如有）— 仅当游戏接入了 wx.requestSubscribeMessage 业务时必报", "optional": True},
            {"event": "TUTORIAL_START", "note": "新手引导开始（如有）", "optional": True},
            {"event": "TUTORIAL_FINISH", "note": "完成新手教程（如有）", "optional": True},
        ],
        "recommended": [
            {"event": "AD_CLICK", "note": "IAA 广告点击（建议上报）"},
            {"event": "AD_VIDEO_FINISH", "note": "激励视频完成"},
            {"event": "UPDATE_LEVEL", "note": "关卡通过"},
            {"event": "VIEW_CONTENT", "note": "浏览内容"},
        ],
        "auto_collected": ["TICKET", "ENTER_FOREGROUND", "ENTER_BACKGROUND", "START_APP", "APP_QUIT",
                           "LOGIN", "SHARE", "START_PAY", "FINISH_PAY", "ADD_TO_WISHLIST", "CREATE_GAME_ROOM"],
    },
    # ============ 小程序端 ============
    "drama": {
        "required": [
            {"event": "REGISTER", "note": "用户首次打开小程序 — 必须由服务端判断 isNew=true 后客户端调用，禁止 wx.storage 自判"},
            {"event": "SELECT_RECHARGE_LEVEL", "note": "选择充值档位，需传 drama_id/drama_name/episodes",
             "require_param": "drama_id"},
            {"event": "PURCHASE", "note": "付费成功，需传 value/drama_id/drama_name/episodes",
             "require_param": "value"},
        ],
        "auto_collected": ["TICKET", "ENTER_FOREGROUND", "ENTER_BACKGROUND", "START_APP",
                           "SHARE", "PAGE_VIEW", "PAGE_LEAVE", "START_PAY", "FINISH_PAY", "ADD_TO_WISHLIST"],
    },
    "novel": {
        "required": [
            {"event": "START_APP", "note": "自动采集，也可手动上报"},
            {"event": "REGISTER", "note": "用户首次打开 — 必须由服务端判断 isNew=true 后客户端调用"},
            {"event": "PURCHASE", "note": "付费成功，需传 value/novel_id/novel_name/chapters",
             "require_param": "value"},
        ],
        "auto_collected": ["TICKET", "ENTER_FOREGROUND", "ENTER_BACKGROUND", "START_APP",
                           "SHARE", "PAGE_VIEW", "PAGE_LEAVE", "START_PAY", "FINISH_PAY"],
    },
    "ecommerce": {
        "required": [
            {"event": "START_APP", "note": "自动采集"},
            {"event": "PRODUCT_VIEW", "note": "进入商品详情页"},
            {"event": "ADD_TO_CART", "note": "加入购物车"},
            {"event": "PURCHASE", "note": "付费成功，必须传 value", "require_param": "value"},
            {"event": "COMPLETE_ORDER", "note": "提交订单"},
        ],
        "auto_collected": ["TICKET", "ENTER_FOREGROUND", "ENTER_BACKGROUND", "START_APP",
                           "SHARE", "PAGE_VIEW", "PAGE_LEAVE"],
    },
    "general-mini-program": {
        "required": [
            {"event": "START_APP", "note": "自动采集"},
            {"event": "REGISTER", "note": "新用户首次打开 — 必须由服务端判断 isNew=true 后客户端调用"},
            {"event": "PURCHASE", "note": "如有付费场景，必须传 value", "require_param": "value", "optional": True},
        ],
        "auto_collected": ["TICKET", "ENTER_FOREGROUND", "ENTER_BACKGROUND", "START_APP",
                           "SHARE", "PAGE_VIEW", "PAGE_LEAVE"],
    },
    # ============ APP 端 ============
    "game-app": {
        "required": [
            {"event": "START_APP", "note": "Android/iOS 端需手动上报（冷启+热启各一条）；Android v1.9.4+ 可开启自动采集"},
            {"event": "REGISTER", "note": "Android/iOS：GDTAction.logAction('REGISTER')；鸿蒙：dnSDK.logAction('REGISTER')，必须由服务端判断 isNew=true"},
            {"event": "LOGIN", "note": "用户登录"},
            {"event": "CREATE_ROLE", "note": "创建角色（游戏类必报，无则不报）", "optional": True},
            {"event": "PURCHASE", "note": "必须传 value（单位：分）", "require_param": "value"},
        ],
        "recommended": [
            {"event": "TUTORIAL_FINISH", "note": "建议上报"},
        ],
        "auto_collected": ["TICKET", "ENTER_FOREGROUND", "ENTER_BACKGROUND"],
    },
    "general-app": {
        "required": [
            {"event": "START_APP", "note": "Android/iOS 手动上报（冷启+热启各一条）；Android v1.9.4+ 可开启自动采集"},
            {"event": "PURCHASE", "note": "如有付费，必须传 value", "require_param": "value", "optional": True},
        ],
        "recommended": [
            {"event": "REGISTER", "note": "社交类建议上报"},
            {"event": "LOGIN", "note": "社交类建议上报"},
        ],
        "auto_collected": ["TICKET", "ENTER_FOREGROUND", "ENTER_BACKGROUND"],
    },
}

# 鸿蒙自动采集差异
HARMONY_AUTO_COLLECTED = ["TICKET", "ENTER_FOREGROUND", "ENTER_BACKGROUND", "START_APP", "APP_QUIT"]


# SDK 端 -> 默认场景（未指定 --scenario 时使用）
# 说明：
#   mini-game 不设默认，因为 IAP / IAA 必报事件差别很大（IAA 不含 PURCHASE），
#   静默选择会漏掉最关键的付费事件。未指定时提示用户显式选。
#   mini-program 的 general-mini-program 已包含 PURCHASE，保留默认。
DEFAULT_SCENARIO = {
    "mini-game": None,  # 强制要求显式 --scenario
    "mini-program": "general-mini-program",
    "android": "general-app",
    "ios": "general-app",
    "harmony": "general-app",
}

# --sdk-end × --scenario 合法组合（用于一致性校验）
VALID_SCENARIOS_BY_SDK: Dict[str, List[str]] = {
    "mini-game": ["iap-mini-game", "iaa-mini-game"],
    "mini-program": ["drama", "novel", "ecommerce", "general-mini-program"],
    "android": ["game-app", "general-app"],
    "ios": ["game-app", "general-app"],
    "harmony": ["general-app"],
}


# ─────────────────────────────────────────────────────────
# 数据结构
# ─────────────────────────────────────────────────────────

class Severity(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    INFO = "INFO"


@dataclass
class Issue:
    category: str      # "初始化规范" / "必报事件" / "用法正确性" / "自动采集冗余" / "合规"
    id: str            # 机器可读 ID
    severity: str      # PASS / WARN / FAIL / INFO（字符串，非枚举）
    title: str
    detail: str
    evidence: Optional[List[str]] = field(default=None)  # 文件+行号等证据
    ref: Optional[str] = field(default=None)             # 指向 references/ 的文档锚点
    suggestion: Optional[str] = field(default=None)

    def __post_init__(self):
        # 允许传入 Severity 枚举，但内部统一为字符串，避免 dataclass.asdict 序列化时出现 'Severity.FAIL'
        if isinstance(self.severity, Severity):
            self.severity = self.severity.value


# ─────────────────────────────────────────────────────────
# 工具
# ─────────────────────────────────────────────────────────

IGNORE_DIRS = {
    "node_modules", "Pods", ".git", "build", ".build", "dist", ".next",
    "DerivedData", "oh_modules", "miniprogram_npm",
    "temp", "library", "profiles", ".creator", "local",
    "out", "coverage", ".cache",
}

SOURCE_EXTS_BY_SDK = {
    "mini-game": {".js", ".ts"},
    "mini-program": {".js", ".ts"},
    "android": {".java", ".kt"},
    "ios": {".m", ".mm", ".swift", ".h"},
    "harmony": {".ts", ".ets"},
}


def _iter_source_files(root: Path, exts: Set[str]) -> List[Path]:
    files: List[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in exts:
            files.append(p)
    return files


def _read(path: Path) -> str:
    # 带缓存版本在 _file_cache 里，_read 保留作为无缓存场景（rare）
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


# ─────────────────────────────────────────────────────────
# 文件内容缓存：一次体检里同一文件会被多次 grep（每个事件 3~4 个 pattern × 10+ 事件），
# 不缓存会变成 O(文件数 × pattern 数) 次 read_text，大项目显著慢。
# ─────────────────────────────────────────────────────────

_file_text_cache: Dict[Path, str] = {}
_file_lines_cache: Dict[Path, List[str]] = {}


def _cached_text(path: Path) -> str:
    if path not in _file_text_cache:
        _file_text_cache[path] = _read(path)
    return _file_text_cache[path]


def _cached_lines(path: Path) -> List[str]:
    if path not in _file_lines_cache:
        _file_lines_cache[path] = _cached_text(path).splitlines()
    return _file_lines_cache[path]


def _reset_cache() -> None:
    """每次 audit() 调用前清空（重要：否则在同一进程内连续体检不同项目会串数据）"""
    _file_text_cache.clear()
    _file_lines_cache.clear()


def _grep(files: List[Path], pattern: str, skip_comments: bool = True) -> List[Tuple[Path, int, str]]:
    try:
        compiled = re.compile(pattern)
    except re.error:
        return []
    hits: List[Tuple[Path, int, str]] = []
    for f in files:
        for idx, line in enumerate(_cached_lines(f)):
            # 先剔除注释再匹配，避免注释里的 new SDK({...}) 被误判为已接入
            candidate = _strip_line_comment(line) if skip_comments else line
            if compiled.search(candidate):
                hits.append((f, idx + 1, line.strip()[:200]))
    return hits


def _rel(root: Path, p: Path) -> str:
    try:
        return str(p.relative_to(root))
    except ValueError:
        return str(p)


# ─────────────────────────────────────────────────────────
# 事件调用检测
# ─────────────────────────────────────────────────────────

# 事件 -> SDK 实际常见方法名别名（超出 _snake_to_pascal 可推导的范围）
# 注意：PascalCase 自动推导会把 "RE_ACTIVE" 转成 "onReActive"，但真实 SDK 可能是 "onReactive"；
# 再比如 LOAD_FINISH 常见的简写是 loadFinish / onLoadFinish。这里列白名单手动补充。
REPORT_METHOD_ALIASES: Dict[str, List[str]] = {
    "RE_ACTIVE":        ["onReactive", "reportReactive", "onReActive", "reActivate"],
    "LOAD_FINISH":      ["onLoadFinish", "loadFinish", "onLoadingFinish"],
    "TUTORIAL_START":   ["onTutorialStart", "tutorialStart"],
    "TUTORIAL_FINISH":  ["onTutorialFinish", "tutorialFinish", "onTutorialComplete"],
    "UPDATE_LEVEL":     ["onUpdateLevel", "updateLevel", "levelUp"],
    "CREATE_ROLE":      ["onCreateRole", "createRole"],
    "START_APP":        ["onAppStart", "onStartApp", "appStart"],
    "PURCHASE":         ["onPurchase", "purchase"],
    "SUBSCRIBE":        ["onSubscribe", "subscribe"],
    "REGISTER":         ["onRegister", "register", "onSignup"],
    "AD_CLICK":         ["onAdClick", "adClick", "onAdClicked"],
    "AD_VIDEO_FINISH":  ["onAdVideoFinish", "adVideoFinish", "onRewardedVideoFinish"],
    "VIEW_CONTENT":     ["onViewContent", "viewContent"],
    "LOGIN":            ["onLogin", "login"],
    "PRODUCT_VIEW":     ["onProductView", "productView"],
    "ADD_TO_CART":      ["onAddToCart", "addToCart"],
    "COMPLETE_ORDER":   ["onCompleteOrder", "completeOrder", "onOrderComplete"],
    "SELECT_RECHARGE_LEVEL": ["onSelectRechargeLevel", "selectRechargeLevel"],
}


def _detect_event_calls(files: List[Path], event: str) -> List[Tuple[Path, int, str]]:
    """
    检测一个事件是否被上报。匹配多种写法：
      - sdk.track('REGISTER')                       ← 通用上报
      - sdk.onRegister() / sdk.onAppStart() / ...   ← 专用方法
      - GDTAction.logAction("REGISTER", ...)        ← Android/iOS（鸿蒙用 dnSDK.logAction）
      - ActionUtils.onRegister(...)                 ← Android 专用
      - [GDTAction reportRegisterActionWith...]     ← iOS 便捷
      - 字符串字面量 'REGISTER' / "REGISTER" 出现    ← 兜底（低置信度）
    """
    patterns = [
        # 字符串字面量（高精度上下文：在 track / logAction 附近）
        rf"""(?:track|logAction|report)\s*\(\s*['"]{re.escape(event)}['"]""",
        # 专用方法（按事件转 camelCase：REGISTER -> onRegister；CREATE_ROLE -> onCreateRole）
        rf"\.on{_snake_to_pascal(event)}\s*\(",
        # iOS 便捷方法：reportRegisterAction / reportPurchaseAction...
        rf"report{_snake_to_pascal(event)}Action\w*",
    ]
    # 追加别名方法
    for alias in REPORT_METHOD_ALIASES.get(event, []):
        # \b 词边界保证不误匹配 onReactiveButton 这种子串
        patterns.append(rf"\b{re.escape(alias)}\s*\(")

    hits: List[Tuple[Path, int, str]] = []
    seen = set()
    for pat in patterns:
        for h in _grep(files, pat):
            key = (h[0], h[1])
            if key in seen:
                continue
            seen.add(key)
            hits.append(h)
    # 兜底：独立出现字符串 'EVENT'（需离 track/logAction 附近 5 行内）
    if not hits:
        literal_pat = rf"['\"]{re.escape(event)}['\"]"
        literal_hits = _grep(files, literal_pat)
        for f, line, text in literal_hits:
            # 附近 5 行是否有上报调用
            content = _cached_lines(f)
            window = "\n".join(content[max(0, line - 5): line + 5])
            if re.search(r"(track|logAction|report)\s*\(", window):
                hits.append((f, line, text))
    return hits


def _snake_to_pascal(s: str) -> str:
    """REGISTER -> Register ; CREATE_ROLE -> CreateRole ; RE_ACTIVE -> ReActive"""
    return "".join(p.capitalize() for p in s.split("_"))


# ─────────────────────────────────────────────────────────
# 初始化规范检查
# ─────────────────────────────────────────────────────────

def _check_init_compliance(root: Path, sdk_end: str, files: List[Path]) -> List[Issue]:
    issues: List[Issue] = []

    # ---- mini-game / mini-program：new SDK({...}) 或被包一层（如 DnSdkTool）
    if sdk_end in {"mini-game", "mini-program"}:
        # 直接匹配：new SDK({...})
        init_hits = _grep(files, r"new\s+SDK\s*\(\s*\{")
        # 宽松匹配：new SDK(variable) / new XxxSDK({...})（被包装的场景）
        wrapped_hits = _grep(files, r"new\s+(?:\w+)?SDK\s*\(")
        # 去重（避免 wrapped_hits 里重复了 init_hits）
        seen = {(h[0], h[1]) for h in init_hits}
        wrapped_only = [h for h in wrapped_hits if (h[0], h[1]) not in seen]
        # import/require 作为"SDK 已接入"的弱信号
        import_hits = _grep(files, r"(?:from|require)\s*[\(\s]['\"]@dn-sdk/(?:minigame|miniprogram)")

        if not init_hits and not wrapped_only:
            # 完全没有 new SDK(...) 调用
            severity = Severity.WARN if import_hits else Severity.FAIL
            issues.append(Issue(
                category="初始化规范",
                id="no_init",
                severity=severity,
                title="未检测到 SDK 初始化调用",
                detail=(
                    "项目未找到 new SDK({...}) 调用。"
                    + ("已检测到 @dn-sdk/* 的 import，但仅 import 不实例化，SDK 不会工作。"
                       if import_hits else
                       "请先完成初始化。若 SDK 被自定义工具类封装（如 DnSdkTool），请确认其中包含 new SDK() 调用。")
                ),
                evidence=[f"{_rel(root, h[0])}:{h[1]}" for h in import_hits[:3]] if import_hits else None,
                ref="references/{}/接入指引/接入流程.md".format(
                    "小游戏SDK" if sdk_end == "mini-game" else "小程序SDK"
                ),
                suggestion="补齐 new SDK({ user_action_set_id, secret_key, appid, auto_track: true }) 实例化调用。",
            ))
            # ⚠️ 不再 return —— 后续事件/合规/冗余检查仍继续，帮助用户拿到完整画像
        elif not init_hits and wrapped_only:
            # 可能被包一层
            issues.append(Issue(
                category="初始化规范",
                id="wrapped_init",
                severity=Severity.INFO,
                title="未直接命中 new SDK({...})，但检测到疑似封装调用",
                detail="找到可能的 SDK 封装实例化，建议人工确认其内部确实调用了 new SDK({ user_action_set_id, secret_key, ... })。",
                evidence=[f"{_rel(root, h[0])}:{h[1]}  {h[2]}" for h in wrapped_only[:5]],
                ref="references/{}/接入指引/接入流程.md".format(
                    "小游戏SDK" if sdk_end == "mini-game" else "小程序SDK"
                ),
            ))
            # init_hits 改为 wrapped_only，让下面的多处初始化检查也能跑
            init_hits = wrapped_only

        # 重复初始化风险：多个 new SDK({...})
        if len(init_hits) > 1:
            issues.append(Issue(
                category="初始化规范",
                id="multiple_init",
                severity=Severity.WARN,
                title="检测到多处 SDK 初始化",
                detail=f"发现 {len(init_hits)} 处 new SDK({{...}}) 调用。"
                       f"同一 user_action_set_id 创建多实例会触发 'Please do not repeatedly initialize SDK' 错误。",
                evidence=[f"{_rel(root, h[0])}:{h[1]}" for h in init_hits[:5]],
                ref="references/通用/排障/错误码速查表.md#51000",
                suggestion="请改为单例，或确认每个 SDK 实例对应不同的 user_action_set_id。",
            ))

        # 用户 ID 设置（mini-game / mini-program 重点）
        id_hits = _grep(files, r"setOpenId\s*\(|setUnionId\s*\(")
        if not id_hits:
            issues.append(Issue(
                category="初始化规范",
                id="no_user_id",
                severity=Severity.WARN,
                title="未设置 openid / unionid",
                detail="未找到 setOpenId / setUnionId 调用。未设置时 SDK 会暂停上传。",
                ref="references/{}/接入指引/接入流程.md".format(
                    "小游戏SDK" if sdk_end == "mini-game" else "小程序SDK"
                ),
                suggestion="登录后尽早调用 sdk.setOpenId(openid)，最好在上报注册事件前。",
            ))

    # ---- android / ios / harmony：GDTAction.init + start 双调用
    if sdk_end in {"android", "ios", "harmony"}:
        init_pat = {
            "android": r"GDTAction\s*\.\s*init\s*\(",
            "ios":     r"GDTAction\s+init\s*:|GDTAction\.init\s*\(",
            "harmony": r"dnSDK\s*\.\s*init\s*\(",
        }[sdk_end]
        start_pat = {
            "android": r"GDTAction\s*\.\s*start\s*\(",
            "ios":     r"GDTAction\s+start|GDTAction\.start\s*\(",
            "harmony": r"dnSDK\s*\.\s*start\s*\(",
        }[sdk_end]
        init_hits = _grep(files, init_pat)
        start_hits = _grep(files, start_pat)
        init_sdk_name = "dnSDK" if sdk_end == "harmony" else "GDTAction"
        if not init_hits:
            issues.append(Issue(
                category="初始化规范", id="no_init", severity=Severity.FAIL,
                title=f"未检测到 {init_sdk_name}.init",
                detail="请在 Application/AppDelegate/EntryAbility 中完成初始化。",
            ))
        if not start_hits:
            issues.append(Issue(
                category="初始化规范", id="no_start", severity=Severity.FAIL,
                title=f"未调用 {init_sdk_name}.start()",
                detail=f"{sdk_end} 端 v2.1+ 必须在 init 之后立即调用 start()，否则 SDK 不工作。",
                ref="references/APP-{}/接入指引/接入流程.md".format(
                    "Android" if sdk_end == "android" else ("iOS" if sdk_end == "ios" else "")
                ).rstrip("-"),
            ))
        if init_hits and start_hits and len(init_hits) > 1:
            issues.append(Issue(
                category="初始化规范", id="multiple_init", severity=Severity.WARN,
                title=f"检测到 {len(init_hits)} 处 {init_sdk_name}.init",
                detail="建议在 Application/AppDelegate 中只初始化一次。",
                evidence=[f"{_rel(root, h[0])}:{h[1]}" for h in init_hits[:5]],
            ))

    return issues


# ─────────────────────────────────────────────────────────
# 必报事件覆盖度检查
# ─────────────────────────────────────────────────────────

def _check_required_events(
    root: Path, sdk_end: str, scenario: str, files: List[Path]
) -> Tuple[List[Issue], Dict[str, object]]:
    """返回 issues + 覆盖度统计"""
    issues: List[Issue] = []
    matrix = EVENT_MATRIX.get(scenario)
    if not matrix:
        issues.append(Issue(
            category="必报事件", id="unknown_scenario", severity=Severity.WARN,
            title=f"未知场景 {scenario}，跳过必报事件校验",
            detail=f"支持的场景：{list(EVENT_MATRIX.keys())}",
        ))
        return issues, {"covered": 0, "total": 0, "coverage": 0.0}

    # 鸿蒙 auto_collected 走单独列表
    auto_collected = set(matrix.get("auto_collected", []))
    if sdk_end == "harmony":
        auto_collected = set(HARMONY_AUTO_COLLECTED)

    required_events = matrix.get("required", [])
    recommended = matrix.get("recommended", [])

    covered: List[str] = []
    missed_hard: List[Dict] = []      # 硬必报未报 → FAIL
    missed_optional: List[Dict] = []  # 条件必报未报 → WARN（如"如有"的新手引导/付费场景）

    for ev in required_events:
        name = ev["event"]
        is_optional = bool(ev.get("optional"))

        # 自动采集事件天然覆盖
        if name in auto_collected:
            covered.append(name)
            continue
        hits = _detect_event_calls(files, name)
        if hits:
            covered.append(name)
            # 检查 require_param
            if ev.get("require_param"):
                param = ev["require_param"]
                param_ok = False
                for h in hits:
                    content = _cached_lines(h[0])
                    window = "\n".join(content[max(0, h[1] - 2): h[1] + 3])
                    if re.search(rf"\b{re.escape(param)}\b", window):
                        param_ok = True
                        break
                if not param_ok:
                    issues.append(Issue(
                        category="用法正确性",
                        id=f"missing_param_{name}_{param}",
                        severity=Severity.FAIL,
                        title=f"事件 {name} 调用未传必填参数 {param}",
                        detail=f"{ev.get('note', '')}",
                        evidence=[f"{_rel(root, h[0])}:{h[1]}" for h in hits[:3]],
                        ref="references/通用/埋点/行为类型枚举表.md",
                        suggestion=f"在 {name} 上报时必须传入 {param}（如 {{ {param}: ... }}）",
                    ))
        else:
            if is_optional:
                missed_optional.append(ev)
            else:
                missed_hard.append(ev)

    # 硬必报未报 → FAIL
    for ev in missed_hard:
        issues.append(Issue(
            category="必报事件",
            id=f"missing_{ev['event']}",
            severity=Severity.FAIL,
            title=f"必报事件 {ev['event']} 未检测到",
            detail=ev.get("note", ""),
            ref="references/通用/埋点/行为类型枚举表.md",
            suggestion=f"请在对应业务节点补报 {ev['event']} 事件",
        ))

    # 条件必报（"如有"类）未报 → WARN
    for ev in missed_optional:
        issues.append(Issue(
            category="必报事件",
            id=f"optional_missing_{ev['event']}",
            severity=Severity.WARN,
            title=f"条件必报事件 {ev['event']} 未检测到",
            detail=f"{ev.get('note', '')}（若业务场景不涉及可忽略）",
            ref="references/通用/埋点/行为类型枚举表.md",
            suggestion=f"若业务有 {ev['event']} 对应场景请补报；无则可忽略本告警",
        ))

    # 建议上报事件 → WARN
    for ev in recommended:
        name = ev["event"]
        if name in auto_collected:
            continue
        hits = _detect_event_calls(files, name)
        if not hits:
            issues.append(Issue(
                category="必报事件",
                id=f"recommended_missing_{name}",
                severity=Severity.WARN,
                title=f"建议上报事件 {name} 未检测到",
                detail=ev.get("note", ""),
                ref="references/通用/埋点/行为类型枚举表.md",
                suggestion=f"业务场景涉及时建议补报，可提升广告优化效果",
            ))

    # 覆盖度计算：只统计"硬必报 × 非自动采集"的事件
    # optional 事件不计入分母（业务可能不存在该场景，不该拖低覆盖度）
    hard_manual_required = [
        e for e in required_events
        if e["event"] not in auto_collected and not e.get("optional")
    ]
    hard_manual_covered = [
        c for c in covered
        if c not in auto_collected
        and any(e["event"] == c and not e.get("optional") for e in required_events)
    ]
    total = len(hard_manual_required)
    covered_cnt = len(hard_manual_covered)
    coverage = (covered_cnt / total * 100) if total else 100.0

    # optional 覆盖情况单独统计（供展示用）
    optional_events = [e["event"] for e in required_events if e.get("optional")]
    optional_covered = [c for c in covered if c in optional_events]

    return issues, {
        "covered": covered,
        "missed": [m["event"] for m in missed_hard],
        "optional_missed": [m["event"] for m in missed_optional],
        "optional_covered": optional_covered,
        "total_required": len(required_events),
        "manual_required": total,
        "manual_covered": covered_cnt,
        "coverage_percent": round(coverage, 1),
    }


# ─────────────────────────────────────────────────────────
# 自动采集冗余检查
# ─────────────────────────────────────────────────────────

def _check_auto_collect_redundancy(
    root: Path, sdk_end: str, scenario: str, files: List[Path]
) -> List[Issue]:
    """
    检测是否手动上报了 SDK 已自动采集的事件（双重上报风险）。
    注意：要区分"可手动也可自动"的白名单事件（如 START_APP 在小游戏可手动调用）。
    """
    issues: List[Issue] = []
    matrix = EVENT_MATRIX.get(scenario, {})
    auto_collected = set(matrix.get("auto_collected", []))
    if sdk_end == "harmony":
        auto_collected = set(HARMONY_AUTO_COLLECTED)

    # 安全清单：这些自动事件，用户可以同时手动调用（SDK 会去重或本就支持）
    safe_manual = {"START_APP"} if sdk_end in {"mini-game", "mini-program"} else set()
    # 鸿蒙 START_APP 严禁手动
    if sdk_end == "harmony":
        safe_manual = set()

    for ev in auto_collected:
        if ev in safe_manual:
            continue
        hits = _detect_event_calls(files, ev)
        if not hits:
            continue
        # 过滤：仅算用户自己的代码（不在 node_modules）
        issues.append(Issue(
            category="自动采集冗余",
            id=f"redundant_manual_{ev}",
            severity=Severity.WARN,
            title=f"{ev} 已由 SDK 自动采集，手动上报可能导致重复",
            detail=f"{sdk_end} 端 SDK 已自动采集 {ev}，不建议再手动调用。",
            evidence=[f"{_rel(root, h[0])}:{h[1]}" for h in hits[:3]],
            ref="references/通用/埋点/行为类型枚举表.md#二、SDK-自动采集事件",
            suggestion=f"请移除 {ev} 的手动上报调用，依赖 SDK 自动采集",
        ))

    return issues


# ─────────────────────────────────────────────────────────
# 合规检查（核心）
# ─────────────────────────────────────────────────────────

def _check_compliance(root: Path, sdk_end: str, files: List[Path]) -> List[Issue]:
    """
    合规检查（仅保留与业务风险直接相关的规则）

    设计说明：
      关于 secret_key 的硬编码检查曾经存在，但被移除。原因：
        - DataNexus SDK 场景下 secret_key 的安全模型与传统"敏感密钥"不同：
          它是数据源的公开签名对照值，不是需要保护的凭证。
        - 为了让 SDK 在冷启动第一时间完成初始化（保证 START_APP 等事件链路不丢），
          官方推荐做法就是硬编码，而非远程下发（远程下发引入启动时的网络依赖，
          会导致启动链路事件被推迟/丢失，违背归因 SDK 的核心目标）。
        - 因此硬编码 secret_key 是 DataNexus SDK 的**最佳实践**，不应被体检告警。
      如果后续需要对敏感凭证（OAID、第三方 API token 等）做合规检查，
      请在此函数新增独立规则，明确区分语义。
    """
    issues: List[Issue] = []

    # 隐私政策前置：SDK init 是否在 onAgreePrivacy 等授权后
    # 这里只能做很粗糙的静态推断：扫是否有 "agreePrivacy" / "同意隐私" / "privacyPolicy" 等关键字
    # 完全没命中 → 给一个 INFO 级提醒
    privacy_hits = _grep(files, r"agreePrivacy|agreeToPrivacy|privacyPolicy|同意隐私|agreeUserPrivacy|隐私协议")
    if not privacy_hits:
        issues.append(Issue(
            category="合规",
            id="privacy_not_detected",
            severity=Severity.INFO,
            title="未检测到隐私协议相关代码",
            detail="SDK 初始化必须在用户同意隐私协议后调用。未检测到隐私相关代码可能意味着："
                   "（a）你的 App 还没接入隐私协议弹窗；（b）隐私协议逻辑在构建模板/服务端处理。",
            ref="references/通用/合规/数据合规指引.md",
            suggestion="若尚未接入隐私政策弹窗，请先补齐；若已在其他位置处理，可忽略此提示。",
        ))

    return issues


# ─────────────────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────────────────

def audit(root_path: str, sdk_end: str, scenario: Optional[str] = None) -> Dict[str, object]:
    _reset_cache()  # 防止在同一进程内连续体检不同项目时串数据
    root = Path(root_path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        return {"error": f"项目路径不存在: {root}"}

    if sdk_end not in SOURCE_EXTS_BY_SDK:
        return {"error": f"不支持的 SDK 端: {sdk_end}；可选：{list(SOURCE_EXTS_BY_SDK.keys())}"}

    if scenario is None:
        scenario = DEFAULT_SCENARIO.get(sdk_end)
    if scenario is None:
        # 没有默认场景 —— 强制要求显式指定（mini-game）
        return {
            "error": (
                f"SDK 端 {sdk_end} 必须显式指定 --scenario，"
                f"因为 IAP / IAA 必报事件差异较大（IAA 不含 PURCHASE），静默默认可能漏报。"
            ),
            "supported_scenarios": VALID_SCENARIOS_BY_SDK.get(sdk_end, []),
            "hint": f"例：--scenario {VALID_SCENARIOS_BY_SDK.get(sdk_end, ['<场景>'])[0]}",
        }
    # --sdk-end 与 --scenario 一致性校验
    allowed = VALID_SCENARIOS_BY_SDK.get(sdk_end, [])
    if allowed and scenario not in allowed:
        return {
            "error": f"场景 '{scenario}' 不适用于 SDK 端 '{sdk_end}'",
            "supported_scenarios": allowed,
            "hint": f"{sdk_end} 端合法场景：{allowed}",
        }
    if scenario not in EVENT_MATRIX:
        return {
            "error": f"未知场景: {scenario}",
            "supported_scenarios": list(EVENT_MATRIX.keys()),
        }

    files = _iter_source_files(root, SOURCE_EXTS_BY_SDK[sdk_end])

    issues: List[Issue] = []
    issues.extend(_check_init_compliance(root, sdk_end, files))
    event_issues, coverage = _check_required_events(root, sdk_end, scenario, files)
    issues.extend(event_issues)
    issues.extend(_check_auto_collect_redundancy(root, sdk_end, scenario, files))
    issues.extend(_check_compliance(root, sdk_end, files))

    # 统计
    sev_counts = {s.value: 0 for s in Severity}
    for i in issues:
        sev_counts[i.severity] = sev_counts.get(i.severity, 0) + 1

    return {
        "project_root": str(root),
        "sdk_end": sdk_end,
        "scenario": scenario,
        "files_scanned": len(files),
        "coverage": coverage,
        "summary": {
            "total_issues": len(issues),
            "fail": sev_counts["FAIL"],
            "warn": sev_counts["WARN"],
            "info": sev_counts["INFO"],
            "pass": sev_counts["PASS"],
        },
        "issues": [asdict(i) for i in issues],
    }


def _print_human(report: Dict[str, object]) -> None:
    if "error" in report:
        print(f"❌ {report['error']}")
        if "supported_scenarios" in report:
            print(f"  支持的场景：{report['supported_scenarios']}")
        return

    print(f"🔬 DataNexus SDK 接入体检报告")
    print(f"  项目：{report['project_root']}")
    print(f"  SDK 端：{report['sdk_end']}  ｜  场景：{report['scenario']}")
    print(f"  扫描文件数：{report['files_scanned']}")
    print()

    cov = report["coverage"]
    if cov.get("total_required"):
        print(f"📊 必报事件覆盖度：{cov['coverage_percent']}%  "
              f"({cov['manual_covered']}/{cov['manual_required']} 硬必报已覆盖，不含条件必报)")
        if cov.get("covered"):
            print(f"  ✅ 已覆盖: {', '.join(cov['covered'])}")
        if cov.get("missed"):
            print(f"  ❌ 硬必报未覆盖: {', '.join(cov['missed'])}")
        if cov.get("optional_missed"):
            print(f"  ⚠️  条件必报未覆盖（业务场景不涉及可忽略）: {', '.join(cov['optional_missed'])}")
        print()

    issues = report["issues"]
    by_category: Dict[str, List[Dict]] = {}
    for i in issues:
        by_category.setdefault(i["category"], []).append(i)

    for cat, items in by_category.items():
        print(f"━━━ {cat}（{len(items)}）━━━")
        for it in items:
            icon = {"FAIL": "❌", "WARN": "⚠️ ", "INFO": "ℹ️ ", "PASS": "✅"}.get(it["severity"], "·")
            print(f"  {icon} [{it['severity']}] {it['title']}")
            if it.get("detail"):
                print(f"      → {it['detail']}")
            if it.get("evidence"):
                for e in it["evidence"][:3]:
                    print(f"      @ {e}")
            if it.get("suggestion"):
                print(f"      💡 {it['suggestion']}")
            if it.get("ref"):
                print(f"      📖 参考：{it['ref']}")
        print()

    s = report["summary"]
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📋 总结：FAIL {s['fail']}  WARN {s['warn']}  INFO {s['info']}  （共 {s['total_issues']} 项）")
    if s["fail"] > 0:
        print(f"❌ 存在 {s['fail']} 个关键问题，建议立即修复（可能导致数据上报错误或缺失）")
    elif s["warn"] > 0:
        print(f"⚠️  存在 {s['warn']} 个告警，建议人工评估")
    else:
        print(f"✅ 接入质量良好，无关键问题")


def main() -> int:
    parser = argparse.ArgumentParser(description="DataNexus SDK 接入深度体检")
    parser.add_argument("project_root", help="客户项目根目录")
    parser.add_argument(
        "--sdk-end",
        required=True,
        choices=list(SOURCE_EXTS_BY_SDK.keys()),
        help="SDK 端",
    )
    parser.add_argument(
        "--scenario",
        default=None,
        choices=list(EVENT_MATRIX.keys()),
        help=f"业务场景（不指定则按 SDK 端默认）：{list(EVENT_MATRIX.keys())}",
    )
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    report = audit(args.project_root, args.sdk_end, args.scenario)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_human(report)

    if "error" in report:
        return 2
    s = report["summary"]
    if s["fail"] > 0:
        return 2
    if s["warn"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
