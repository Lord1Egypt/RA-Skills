#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_integration_points.py — 扫描客户项目中 SDK 接入的关键点位

目标：
  1. 定位 SDK 初始化应该插入的位置（生命周期入口：App.onLaunch / Application.onCreate / AppDelegate.didFinishLaunching / EntryAbility.onCreate）
  2. 发现付费/登录/分享/注册等关键业务点，用于：
     - 提示客户哪些行为可以被 SDK 自动采集覆盖
     - 哪些需要手动埋点
  3. 检测已有第三方归因 SDK（友商 SDK、自研埋点），给出冲突/迁移建议

输出格式（JSON）：
  {
    "sdk_end": "mini-game",
    "init_points": [{...}],     # 建议插入 init 的位置
    "event_hooks": [{...}],     # 业务事件触发点（付费/登录/分享等）
    "existing_sdks": [{...}],   # 已有的其他归因 SDK（冲突检测）
    "summary": {...},           # 统计摘要
  }

使用方式：
    python3 scan_integration_points.py <project_root> --sdk-end mini-game
    python3 scan_integration_points.py <project_root> --sdk-end android --json

设计原则：
  - 先用 detect_framework.py 拿到 sdk_end，再传给本脚本（避免重复识别）
  - 跳过 node_modules / Pods / build / .git 等无关目录
  - 每个匹配提供前后 3 行 context，给 Agent 足够上下文判断
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# 同目录共用工具（注释剔除等）
try:
    from _common import strip_line_comment as _strip_line_comment
except ImportError:
    import os as _os
    sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from _common import strip_line_comment as _strip_line_comment  # type: ignore


# ─────────────────────────────────────────────────────────
# 扫描规则（按 SDK 端组织）
# ─────────────────────────────────────────────────────────

# 统一结构：{rule_name: [(正则, 描述, 文件类型限制)]}

MINI_GAME_RULES = {
    "init_points": [
        # 传统微信小游戏模板
        (r"App\s*\(\s*\{", "小游戏 App() 生命周期定义（init 插入点）", [".js", ".ts"]),
        (r"onLaunch\s*[:(]", "onLaunch 生命周期（第一选择插入点）", [".js", ".ts"]),
        # Cocos Creator 3.x：@ccclass + extends Component + onLoad
        (r"@ccclass\s*\(", "Cocos Creator 组件声明（候选入口类）", [".ts"]),
        (r"extends\s+(cc\.)?Component\b", "Cocos Creator 组件（候选入口类）", [".ts"]),
        (r"async\s+onLoad\s*\(|(?<!\w)onLoad\s*\(\s*\)", "Cocos Creator onLoad 生命周期（Creator 3.x 首选插入点）", [".ts"]),
        # LayaAir / Egret 典型入口
        (r"class\s+\w+\s+extends\s+Laya\.Scene", "LayaAir Scene 入口", [".ts"]),
        (r"class\s+\w+\s+extends\s+egret\.DisplayObjectContainer", "Egret 入口", [".ts"]),
    ],
    "event_hooks": [
        (r"wx\.requestPayment\s*\(", "付费接口 → PURCHASE 自动采集", [".js", ".ts"]),
        (r"wx\.login\s*\(", "登录接口 → LOGIN 自动采集", [".js", ".ts"]),
        (r"wx\.shareAppMessage\s*\(", "分享接口 → SHARE 自动采集", [".js", ".ts"]),
        (r"wx\.onShareAppMessage\s*\(", "分享回调 → SHARE 自动采集", [".js", ".ts"]),
        (r"wx\.reportMonitor\s*\(", "自定义业务埋点（可能需要迁移）", [".js", ".ts"]),
        (r"createRewardedVideoAd\s*\(|createBannerAd\s*\(", "激励视频/Banner 广告（IAA 场景，需补 action 埋点）", [".js", ".ts"]),
    ],
    "existing_sdks": [
        (r"require\s*\(\s*['\"]@tencent/gdt", "已有其他 GDT 归因 SDK（旧版）", [".js", ".ts"]),
        # 本 SDK import（含 @dn-sdk/minigame 及子路径深引用如 /build/index.js）
        (r"import\s+.*from\s+['\"]@dn-sdk/minigame(?:/[\w\./-]+)?['\"]", "已有 DataNexus 小游戏 SDK import", [".js", ".ts"]),
        (r"require\s*\(\s*['\"]@dn-sdk/minigame(?:/[\w\./-]+)?['\"]", "已有 DataNexus 小游戏 SDK require", [".js", ".ts"]),
        # 真正的实例化（强信号：代码在用，不仅是 import）
        (r"new\s+SDK\s*\(\s*\{", "DataNexus SDK 实例化已存在（new SDK({...})）", [".js", ".ts"]),
    ],
}

MINI_PROGRAM_RULES = {
    "init_points": [
        (r"App\s*\(\s*\{", "小程序 App() 生命周期定义（init 插入点）", [".js", ".ts"]),
        (r"onLaunch\s*[:(]", "onLaunch 生命周期（第一选择插入点）", [".js", ".ts"]),
    ],
    "event_hooks": [
        (r"wx\.requestPayment\s*\(", "付费接口 → PURCHASE 自动采集", [".js", ".ts"]),
        (r"wx\.login\s*\(", "登录接口 → LOGIN 自动采集", [".js", ".ts"]),
        (r"wx\.shareAppMessage\s*\(", "分享接口 → SHARE 自动采集", [".js", ".ts"]),
        (r"onShareAppMessage\s*[:(]", "分享回调 → SHARE 自动采集", [".js", ".ts"]),
    ],
    "existing_sdks": [
        (r"require\s*\(\s*['\"]@tencent/gdt", "已有其他 GDT 归因 SDK（旧版）", [".js", ".ts"]),
        (r"import\s+.*from\s+['\"]@dn-sdk/miniprogram", "已有 DataNexus 小程序 SDK（本 SDK）", [".js", ".ts"]),
    ],
}

ANDROID_RULES = {
    "init_points": [
        # Java: class X extends Application
        (r"class\s+\w+\s+extends\s+Application\b", "Java Application 子类（init 插入点）", [".java"]),
        # Kotlin: class X : Application()   或   class X : android.app.Application()
        (r"class\s+\w+\s*:\s*(?:\w+\.)*Application\s*\(", "Kotlin Application 子类（init 插入点）", [".kt"]),
        (r"override\s+fun\s+onCreate", "Kotlin Application.onCreate", [".kt"]),
        (r"public\s+void\s+onCreate\s*\(\s*\)", "Java Application.onCreate", [".java"]),
    ],
    "event_hooks": [
        (r"com\.tencent\.mm\.opensdk\.", "微信支付 SDK 付费点", [".java", ".kt"]),
        (r"IWXAPI", "微信 SDK 调用点（支付/登录/分享）", [".java", ".kt"]),
        (r"Alipay|com\.alipay", "支付宝支付点", [".java", ".kt"]),
    ],
    "existing_sdks": [
        (r"com\.qq\.gdt\.action\.GDTAction", "已有 GDTAction SDK（本 SDK）", [".java", ".kt"]),
        (r"com\.umeng\.", "友商 SDK（友盟）", [".java", ".kt"]),
        (r"com\.appsflyer\.", "友商 SDK（AppsFlyer）", [".java", ".kt"]),
    ],
}

IOS_RULES = {
    "init_points": [
        (r"didFinishLaunchingWithOptions", "AppDelegate 启动方法（init 插入点）", [".m", ".mm", ".swift"]),
        (r"application\(_\s*:\s*UIApplication", "SwiftUI/UIKit 启动回调", [".swift"]),
        (r"@main\b", "Swift App 入口", [".swift"]),
    ],
    "event_hooks": [
        (r"WXApi\b", "微信 SDK（支付/登录/分享）", [".m", ".mm", ".swift"]),
        (r"sendAuthReq|sendPayReq", "微信授权/支付请求", [".m", ".mm", ".swift"]),
    ],
    "existing_sdks": [
        (r"#import\s+<GDTActionSDK/", "已有 GDTAction SDK（本 SDK，ObjC 导入）", [".m", ".mm", ".h"]),
        (r"import\s+GDTActionSDK", "已有 GDTAction SDK（本 SDK，Swift 导入）", [".swift"]),
        (r"import\s+AppsFlyerLib", "友商 SDK（AppsFlyer）", [".swift", ".m"]),
    ],
}

HARMONY_RULES = {
    "init_points": [
        (r"class\s+\w+\s+extends\s+UIAbility", "EntryAbility 定义（init 插入点）", [".ts", ".ets"]),
        (r"onCreate\s*\([^)]*\)\s*:\s*void", "Ability onCreate（最佳插入位置）", [".ts", ".ets"]),
    ],
    "event_hooks": [
        (r"@ohos\.payment", "华为支付点", [".ts", ".ets"]),
    ],
    "existing_sdks": [
        (r"from\s+['\"]@dn-sdk/harmony['\"]", "已有 DataNexus SDK（本 SDK）", [".ts", ".ets"]),
        (r"import\s+dnSDK\s+from\s+['\"]@dn-sdk/harmony['\"]", "已有 DataNexus SDK（本 SDK）", [".ts", ".ets"]),
    ],
}

RULES_BY_SDK_END = {
    "mini-game": MINI_GAME_RULES,
    "mini-program": MINI_PROGRAM_RULES,
    "android": ANDROID_RULES,
    "ios": IOS_RULES,
    "harmony": HARMONY_RULES,
}

# 忽略目录
IGNORE_DIRS: Set[str] = {
    "node_modules", "Pods", ".git", ".svn", "build", ".build", "DerivedData",
    "dist", ".next", ".nuxt", ".idea", ".vscode", "miniprogram_npm",
    "oh_modules", ".gradle", ".cxx", "generated",
    # Cocos Creator 编译产物 / IDE 状态目录
    "temp", "library", "profiles", ".creator", "local",
    # 通用
    "out", "coverage", ".cache",
}


# ─────────────────────────────────────────────────────────
# 数据结构
# ─────────────────────────────────────────────────────────

@dataclass
class Match:
    file: str
    line: int
    description: str
    matched_text: str
    context_before: List[str] = field(default_factory=list)
    context_after: List[str] = field(default_factory=list)
    priority: int = 50  # 0-100, 数字越大越优先


# ─────────────────────────────────────────────────────────
# 扫描实现
# ─────────────────────────────────────────────────────────

def _iter_source_files(root: Path, exts: Set[str]) -> List[Path]:
    results: List[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in exts:
            results.append(p)
    return results


def _scan_file(path: Path, rules_group: List[Tuple[str, str, List[str]]]) -> List[Match]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []

    lines = text.splitlines()
    matches: List[Match] = []
    # 文件名启发式：GameManager / AppMain / Main / Entry 等"主入口文件"加权
    fname = path.name.lower()
    is_main_file = any(kw in fname for kw in [
        "gamemanager", "appmain", "main.ts", "entry", "launcher", "bootstrap",
        "app.ts", "index.ts",
    ])

    for pattern, desc, allowed_exts in rules_group:
        if path.suffix.lower() not in allowed_exts:
            continue
        try:
            compiled = re.compile(pattern)
        except re.error:
            continue
        for idx, line in enumerate(lines):
            # 剔除注释后再匹配，避免注释里的代码被误认为真实接入点
            m = compiled.search(_strip_line_comment(line))
            if not m:
                continue
            before = lines[max(0, idx - 3): idx]
            after = lines[idx + 1: min(len(lines), idx + 4)]
            # 根据文件名上下文调整优先级
            pr = _compute_priority(desc)
            if is_main_file and pr >= 90:
                pr = min(99, pr + 2)  # 主入口文件的生命周期再上浮
            # 上下文包含现有初始化链调用 → 更可能是"真正的应用入口"
            ctx_text = "\n".join(before + [line] + after)
            if re.search(r"(WechatGameTool|GameManager|AppInit|BootStrap)\s*\.\s*init\s*\(", ctx_text):
                pr = min(99, pr + 3)
            matches.append(Match(
                file=str(path),
                line=idx + 1,
                description=desc,
                matched_text=line.strip()[:240],
                context_before=[l.rstrip() for l in before],
                context_after=[l.rstrip() for l in after],
                priority=pr,
            ))
    return matches


def _compute_priority(desc: str) -> int:
    # 简单启发式：生命周期入口最高，付费次之
    # 红色告警级：本 SDK 已被实际使用（new SDK({...})）
    if "DataNexus SDK 实例化已存在" in desc:
        return 100
    if "SDK 初始化已存在" in desc:
        return 99  # 告警：别重复接入
    # 黄色告警：本 SDK 只 import 没用（可能安装了但还没接入）
    if "DataNexus 小游戏 SDK import" in desc or "DataNexus 小游戏 SDK require" in desc:
        return 58
    if "onLoad" in desc and "Cocos" in desc:
        return 95
    if "onLaunch" in desc or "onCreate" in desc or "didFinishLaunching" in desc:
        return 95
    if "AppDelegate" in desc or "启动方法" in desc or "启动回调" in desc:
        return 92
    if "Swift App 入口" in desc or "@main" in desc:
        return 90
    if "Application" in desc or "EntryAbility" in desc:
        return 90
    if "付费" in desc or "PURCHASE" in desc or "Purchase" in desc:
        return 80
    if "Cocos Creator 组件" in desc:
        return 75
    if "登录" in desc or "LOGIN" in desc:
        return 70
    if "分享" in desc or "SHARE" in desc:
        return 60
    if "广告" in desc or "IAA" in desc:
        return 65
    if "友商" in desc or "本 SDK" in desc:
        return 55
    return 50


def _collect_extensions(rules: Dict[str, List[Tuple[str, str, List[str]]]]) -> Set[str]:
    exts: Set[str] = set()
    for rules_group in rules.values():
        for _, _, allowed in rules_group:
            exts.update(allowed)
    return exts


def scan(root_path: str, sdk_end: str, max_matches_per_category: int = 50) -> Dict[str, object]:
    root = Path(root_path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        return {"error": f"项目路径不存在: {root}", "sdk_end": sdk_end}

    rules = RULES_BY_SDK_END.get(sdk_end)
    if not rules:
        return {
            "error": f"不支持的 SDK 端: {sdk_end}；可选：{list(RULES_BY_SDK_END.keys())}",
            "sdk_end": sdk_end,
        }

    exts = _collect_extensions(rules)
    source_files = _iter_source_files(root, exts)

    buckets: Dict[str, List[Match]] = {k: [] for k in rules.keys()}
    for f in source_files:
        for category, rules_group in rules.items():
            for m in _scan_file(f, rules_group):
                if len(buckets[category]) >= max_matches_per_category:
                    break
                buckets[category].append(m)

    # 每类按 priority 倒序
    for k in buckets:
        buckets[k].sort(key=lambda m: (-m.priority, m.file, m.line))

    summary = {
        "files_scanned": len(source_files),
        "init_points_found": len(buckets.get("init_points", [])),
        "event_hooks_found": len(buckets.get("event_hooks", [])),
        "existing_sdks_found": len(buckets.get("existing_sdks", [])),
    }

    return {
        "sdk_end": sdk_end,
        "project_root": str(root),
        "summary": summary,
        "init_points": [asdict(m) for m in buckets.get("init_points", [])],
        "event_hooks": [asdict(m) for m in buckets.get("event_hooks", [])],
        "existing_sdks": [asdict(m) for m in buckets.get("existing_sdks", [])],
    }


def _print_human(result: Dict[str, object]) -> None:
    if "error" in result:
        print(f"❌ {result['error']}")
        return

    s = result["summary"]
    print(f"🔍 SDK 接入点扫描结果（SDK 端：{result['sdk_end']}）")
    print(f"  扫描文件数：{s['files_scanned']}")
    print(f"  发现 init 候选点位：{s['init_points_found']}")
    print(f"  发现业务事件触发点：{s['event_hooks_found']}")
    print(f"  发现已有 SDK：{s['existing_sdks_found']}")
    print()

    if result["init_points"]:
        print("📌 建议的 init 插入位置（按优先级排序）：")
        for m in result["init_points"][:5]:
            print(f"  [优先级 {m['priority']}] {m['file']}:{m['line']}")
            print(f"    {m['description']}")
            print(f"    > {m['matched_text']}")
        print()

    if result["event_hooks"]:
        print("🎯 发现的业务事件点（可由 SDK 自动采集覆盖）：")
        for m in result["event_hooks"][:10]:
            print(f"  - {m['file']}:{m['line']}  {m['description']}")
        print()

    if result["existing_sdks"]:
        print("⚠️ 检测到已有第三方/本 SDK，接入时请评估冲突：")
        for m in result["existing_sdks"][:10]:
            print(f"  - {m['file']}:{m['line']}  {m['description']}")
        print()

    if not any([result["init_points"], result["event_hooks"], result["existing_sdks"]]):
        print("⚠️ 未扫到任何关键点位。可能原因：")
        print("  - 项目根路径不对（确认在项目根目录运行）")
        print("  - 源码不在常规位置（比如 monorepo 的子包）")


def main() -> int:
    parser = argparse.ArgumentParser(description="扫描 SDK 接入关键点位")
    parser.add_argument("project_root", help="客户项目根目录")
    parser.add_argument(
        "--sdk-end",
        required=True,
        choices=list(RULES_BY_SDK_END.keys()),
        help="SDK 端（通过 detect_framework.py 先识别）",
    )
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    result = scan(args.project_root, args.sdk_end)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_human(result)

    return 0 if "error" not in result else 1


if __name__ == "__main__":
    sys.exit(main())
