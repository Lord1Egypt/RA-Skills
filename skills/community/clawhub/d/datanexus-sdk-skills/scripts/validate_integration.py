#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_integration.py — SDK 接入后的自动化质量校验

对照 references/通用/质量/接入质量检查清单.md 的内容做可自动化的部分。
由 IDE Agent 在完成代码改动后自动调用，或由用户手动执行。

校验维度：
  1. SDK 依赖安装校验（package.json / Podfile / build.gradle / oh-package.json5）
  2. init() 与 start() 调用完整性校验（对 Android/iOS/鸿蒙 尤其关键）
  3. 占位符残留检查（user_action_set_id / secret_key / appid 是否填写真实值）
  4. 关键配置文件校验（AndroidManifest.xml 权限 / 服务器域名配置 / Linker Flags）
  5. 必报事件覆盖度抽查（对常见 action_type 做关键字扫描）

输出退出码：
  0 → 全部通过
  1 → 存在告警（WARN）
  2 → 存在错误（FAIL），接入可能无法工作

使用方式：
  python3 validate_integration.py <project_root> --sdk-end mini-game
  python3 validate_integration.py <project_root> --sdk-end android --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

# 同目录共用工具（注释剔除等）
try:
    from _common import strip_line_comment as _strip_line_comment
except ImportError:
    import os as _os
    sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from _common import strip_line_comment as _strip_line_comment  # type: ignore


# ─────────────────────────────────────────────────────────
# 数据结构
# ─────────────────────────────────────────────────────────

class Severity(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass
class CheckResult:
    id: str
    title: str
    severity: str
    message: str
    detail: Optional[str] = None


# ─────────────────────────────────────────────────────────
# 辅助工具
# ─────────────────────────────────────────────────────────

IGNORE_DIRS = {
    "node_modules", "Pods", ".git", ".svn", "build", ".build", "dist", ".next", ".nuxt",
    "DerivedData", "oh_modules", "miniprogram_npm",
    # Cocos Creator 编译产物 / IDE 状态目录
    "temp", "library", "profiles", ".creator", "local",
    # 通用
    "out", "coverage", ".cache", ".idea", ".vscode", ".gradle", ".cxx", "generated",
}


def _iter_files(root: Path, exts: set) -> List[Path]:
    files: List[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in exts:
            files.append(p)
    return files


def _read(root: Path, rel: str, max_bytes: int = 500_000) -> str:
    p = root / rel
    if not p.exists():
        return ""
    try:
        return p.read_text(encoding="utf-8", errors="ignore")[:max_bytes]
    except OSError:
        return ""


def _exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def _detect_android_sdk_version(root: Path, gradle_texts: str) -> Optional[str]:
    """从项目中提取 Android SDK 版本号。

    检测顺序：
      1. libs 目录中的 AAR/JAR 文件名（如 GDTActionSDK.min.1.9.2.aar）
      2. build.gradle 中的依赖声明版本号
    """
    # 方法1：扫描 libs 目录的 AAR 文件名
    libs_dir = root / "app" / "libs"
    if not libs_dir.exists():
        libs_dir = root / "libs"
    if libs_dir.exists():
        for f in libs_dir.iterdir():
            if f.is_file() and "GDTActionSDK" in f.name:
                # 匹配 GDTActionSDK.min.1.9.2.aar 或 GDTActionSDK.1.9.4.aar
                m = re.search(r"(\d+\.\d+\.\d+)", f.name)
                if m:
                    return m.group(1)

    # 方法2：从 build.gradle 依赖声明中提取
    m = re.search(r"GDTActionSDK[^\d]*(\d+\.\d+\.\d+)", gradle_texts)
    if m:
        return m.group(1)

    # 方法3：从 build.gradle 的 implementation/api 依赖中提取
    m = re.search(r"gdt[.-]action[^\d]*(\d+\.\d+\.\d+)", gradle_texts, re.IGNORECASE)
    if m:
        return m.group(1)

    return None


def _version_gte(version: Optional[str], target: str) -> bool:
    """判断 version 是否 >= target（语义化版本比较）"""
    if not version:
        return False
    try:
        v_parts = [int(x) for x in version.split(".")]
        t_parts = [int(x) for x in target.split(".")]
        return v_parts >= t_parts
    except (ValueError, AttributeError):
        return False


def _grep_in_files(files: List[Path], pattern: str) -> List[tuple]:
    """返回 [(path, line_no, line_text), ...]，会剔除注释中的命中"""
    hits: List[tuple] = []
    try:
        compiled = re.compile(pattern)
    except re.error:
        return hits
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for idx, line in enumerate(text.splitlines()):
            if compiled.search(_strip_line_comment(line)):
                hits.append((str(f), idx + 1, line.strip()[:200]))
    return hits


PLACEHOLDER_PATTERNS = [
    r"YOUR_USER_ACTION_SET_ID",
    r"YOUR_APP_SECRET_KEY",
    r"YOUR_ACTION_SET_ID",
    r"YOUR_SECRET_KEY",
    r"YOUR_APPID",
    r"your_user_action_set_id",
    r"your_secret_key",
    r"wx1234567890abcdef",
]


def _check_placeholders(files: List[Path]) -> List[tuple]:
    pattern = "|".join(PLACEHOLDER_PATTERNS)
    return _grep_in_files(files, pattern)


# ─────────────────────────────────────────────────────────
# 各端校验实现
# ─────────────────────────────────────────────────────────

def validate_mini_game(root: Path) -> List[CheckResult]:
    results: List[CheckResult] = []

    # 1. 依赖安装
    pkg_txt = _read(root, "package.json")
    has_dep = bool(pkg_txt) and ("@dn-sdk/minigame" in pkg_txt)
    results.append(CheckResult(
        id="dep_installed",
        title="小游戏 SDK 依赖已安装",
        severity=Severity.PASS if has_dep else Severity.FAIL,
        message="已在 package.json 发现 @dn-sdk/minigame" if has_dep
                else "未在 package.json 发现 @dn-sdk/minigame，请执行 `npm i @dn-sdk/minigame`",
    ))

    # 2. init 调用
    js_files = _iter_files(root, {".js", ".ts"})
    init_hits = _grep_in_files(js_files, r"new\s+SDK\s*\(")
    results.append(CheckResult(
        id="init_call",
        title="SDK 初始化调用存在",
        severity=Severity.PASS if init_hits else Severity.FAIL,
        message=f"找到 {len(init_hits)} 处 new SDK() 调用" if init_hits
                else "未找到 new SDK() 初始化调用，SDK 不会工作",
        detail=(init_hits[0][0] + ":" + str(init_hits[0][1])) if init_hits else None,
    ))

    # 3. setOpenId 或 setUnionId 至少调用一次
    id_hits = _grep_in_files(js_files, r"setOpenId\s*\(|setUnionId\s*\(")
    results.append(CheckResult(
        id="user_id_set",
        title="已设置 openid 或 unionid",
        severity=Severity.PASS if id_hits else Severity.WARN,
        message=f"找到 {len(id_hits)} 处 setOpenId/setUnionId 调用" if id_hits
                else "未找到 setOpenId/setUnionId 调用，SDK 会暂停上传",
    ))

    # 4. 占位符检查
    placeholder_hits = _check_placeholders(js_files)
    results.append(CheckResult(
        id="no_placeholder",
        title="未残留占位符（user_action_set_id / secret_key / appid）",
        severity=Severity.PASS if not placeholder_hits else Severity.FAIL,
        message="无占位符残留" if not placeholder_hits
                else f"检测到 {len(placeholder_hits)} 处占位符未替换",
        detail="\n".join(f"  {h[0]}:{h[1]}" for h in placeholder_hits[:5]) or None,
    ))

    # 5. 必报事件抽查（PURCHASE、REGISTER、LOAD_FINISH 至少覆盖其中 2 个）
    required_events = ["PURCHASE", "REGISTER", "LOAD_FINISH", "RE_ACTIVE"]
    covered = [e for e in required_events if _grep_in_files(js_files, re.escape(e))]
    results.append(CheckResult(
        id="required_events",
        title="小游戏必报事件覆盖",
        severity=Severity.PASS if len(covered) >= 2 else Severity.WARN,
        message=f"已覆盖必报事件：{covered}" if covered
                else "未扫到任何必报事件（PURCHASE / REGISTER / LOAD_FINISH 等），请人工核实",
    ))

    return results


def validate_mini_program(root: Path) -> List[CheckResult]:
    results: List[CheckResult] = []

    pkg_txt = _read(root, "package.json")
    has_dep = bool(pkg_txt) and ("@dn-sdk/miniprogram" in pkg_txt)
    results.append(CheckResult(
        id="dep_installed",
        title="小程序 SDK 依赖已安装",
        severity=Severity.PASS if has_dep else Severity.FAIL,
        message="已发现 @dn-sdk/miniprogram 依赖" if has_dep
                else "请执行 `npm i @dn-sdk/miniprogram` 并在微信开发者工具执行「构建 npm」",
    ))

    js_files = _iter_files(root, {".js", ".ts"})
    init_hits = _grep_in_files(js_files, r"new\s+SDK\s*\(")
    results.append(CheckResult(
        id="init_call",
        title="SDK 初始化调用存在",
        severity=Severity.PASS if init_hits else Severity.FAIL,
        message=f"找到 {len(init_hits)} 处初始化" if init_hits else "未找到 new SDK() 调用",
    ))

    placeholder_hits = _check_placeholders(js_files)
    results.append(CheckResult(
        id="no_placeholder",
        title="未残留占位符",
        severity=Severity.PASS if not placeholder_hits else Severity.FAIL,
        message="无占位符残留" if not placeholder_hits else f"{len(placeholder_hits)} 处占位符未替换",
    ))

    return results


def validate_android(root: Path) -> List[CheckResult]:
    results: List[CheckResult] = []

    # 1. 依赖：在 build.gradle 中引用 GDTActionSDK
    gradle_texts = "\n".join(
        _read(root, p) for p in [
            "app/build.gradle", "build.gradle", "app/build.gradle.kts", "build.gradle.kts",
        ]
    )
    has_dep = "GDTActionSDK" in gradle_texts or "gdt-action" in gradle_texts
    results.append(CheckResult(
        id="dep_installed",
        title="GDTActionSDK 已在 build.gradle 引用",
        severity=Severity.PASS if has_dep else Severity.FAIL,
        message="已引用 GDTActionSDK" if has_dep else "未发现 GDTActionSDK 依赖",
    ))

    code_files = _iter_files(root, {".java", ".kt"})

    # 2. init + start 双重调用
    init_hits = _grep_in_files(code_files, r"GDTAction\s*\.\s*init\s*\(")
    start_hits = _grep_in_files(code_files, r"GDTAction\s*\.\s*start\s*\(")
    results.append(CheckResult(
        id="init_call",
        title="GDTAction.init 已调用",
        severity=Severity.PASS if init_hits else Severity.FAIL,
        message=f"找到 {len(init_hits)} 处 init 调用" if init_hits else "未找到 GDTAction.init 调用",
    ))
    results.append(CheckResult(
        id="start_call",
        title="GDTAction.start 已调用（v2.1+ 必须）",
        severity=Severity.PASS if start_hits else Severity.FAIL,
        message=f"找到 {len(start_hits)} 处 start 调用" if start_hits
                else "未找到 GDTAction.start 调用；SDK 不会工作",
    ))

    # 3. INTERNET 权限
    manifest = _read(root, "app/src/main/AndroidManifest.xml") or _read(root, "AndroidManifest.xml")
    has_internet = "android.permission.INTERNET" in manifest
    results.append(CheckResult(
        id="internet_permission",
        title="AndroidManifest.xml 已声明 INTERNET 权限",
        severity=Severity.PASS if has_internet else Severity.FAIL,
        message="已声明" if has_internet else "未声明 INTERNET 权限，网络请求会失败",
    ))

    # 4. 混淆规则（如果有 proguard-rules.pro）
    proguard = _read(root, "app/proguard-rules.pro")
    if proguard:
        has_rule = "com.qq.gdt.action" in proguard
        results.append(CheckResult(
            id="proguard_rule",
            title="ProGuard 混淆规则已包含 SDK 白名单",
            severity=Severity.PASS if has_rule else Severity.WARN,
            message="已添加 -keep class com.qq.gdt.action.**" if has_rule
                    else "项目启用了 ProGuard 但未添加 SDK 白名单，可能导致运行时异常",
        ))

    # 5. START_APP 上报（版本感知判断）
    # 尝试从 libs 目录或 build.gradle 中提取 SDK 版本号
    sdk_version = _detect_android_sdk_version(root, gradle_texts)
    auto_start_supported = _version_gte(sdk_version, "1.9.4") if sdk_version else None

    start_app_hits = _grep_in_files(code_files, r"START_APP")
    # 额外检查是否显式关闭了自动采集
    auto_start_disabled = _grep_in_files(code_files, r"setAutoStartEnable\s*\(\s*false\s*\)")

    if start_app_hits:
        start_app_severity = Severity.PASS
        start_app_msg = f"找到 {len(start_app_hits)} 处 START_APP 引用"
    elif auto_start_supported is True and not auto_start_disabled:
        start_app_severity = Severity.PASS
        start_app_msg = f"SDK 版本 {sdk_version} ≥ 1.9.4，START_APP 默认自动采集，无需手动上报"
    elif auto_start_supported is False:
        start_app_severity = Severity.FAIL
        start_app_msg = (
            f"⚠️ SDK 版本 {sdk_version} < 1.9.4，不支持 START_APP 自动采集，"
            f"必须手动上报（冷启+热启各 1 条）。"
            f"建议在 GDTAction.init + start 后立即上报一条，"
            f"在主 Activity 的 onResume 中再上报一条"
        )
    elif auto_start_disabled:
        start_app_severity = Severity.FAIL
        start_app_msg = (
            "检测到 setAutoStartEnable(false) 关闭了自动采集，"
            "但未发现 START_APP 手动上报代码，必须手动上报（冷启+热启各 1 条）"
        )
    else:
        start_app_severity = Severity.WARN
        start_app_msg = (
            "未发现 START_APP 上报代码，也未能检测到 SDK 版本。"
            "Android SDK v1.9.4+ 默认自动采集 START_APP；低于 1.9.4 必须手动上报。"
            "请确认 SDK 版本"
        )

    results.append(CheckResult(
        id="start_app_report",
        title="START_APP 事件上报检查",
        severity=start_app_severity,
        message=start_app_msg,
    ))

    placeholder_hits = _check_placeholders(code_files)
    results.append(CheckResult(
        id="no_placeholder",
        title="未残留占位符",
        severity=Severity.PASS if not placeholder_hits else Severity.FAIL,
        message="无占位符残留" if not placeholder_hits else f"{len(placeholder_hits)} 处占位符未替换",
    ))

    return results


def validate_ios(root: Path) -> List[CheckResult]:
    results: List[CheckResult] = []

    # 1. Podfile 包含 GDTActionSDK
    podfile = _read(root, "Podfile")
    has_pod = "GDTActionSDK" in podfile
    results.append(CheckResult(
        id="dep_installed",
        title="Podfile 已引用 GDTActionSDK",
        severity=Severity.PASS if has_pod else Severity.FAIL,
        message="已引用" if has_pod else "未在 Podfile 中发现 GDTActionSDK",
    ))

    code_files = _iter_files(root, {".m", ".mm", ".swift", ".h"})

    # 2. init + start
    init_hits = _grep_in_files(code_files, r"GDTAction\s+init\s*:|GDTAction\.init\s*\(")
    start_hits = _grep_in_files(code_files, r"GDTAction\s+start|GDTAction\.start\s*\(")
    results.append(CheckResult(
        id="init_call",
        title="GDTAction init 已调用",
        severity=Severity.PASS if init_hits else Severity.FAIL,
        message=f"找到 {len(init_hits)} 处 init" if init_hits else "未找到 init 调用",
    ))
    results.append(CheckResult(
        id="start_call",
        title="GDTAction start 已调用（v2.1+ 必须）",
        severity=Severity.PASS if start_hits else Severity.FAIL,
        message=f"找到 {len(start_hits)} 处 start" if start_hits else "未找到 start 调用",
    ))

    # 3. START_APP 手动上报
    start_app_hits = _grep_in_files(code_files, r'START_APP')
    results.append(CheckResult(
        id="start_app_report",
        title="START_APP 事件已上报（iOS 需手动）",
        severity=Severity.PASS if start_app_hits else Severity.WARN,
        message=f"找到 {len(start_app_hits)} 处 START_APP 引用" if start_app_hits
                else "iOS 端 START_APP 不自动采集，建议在 applicationDidBecomeActive 中手动 logAction",
    ))

    placeholder_hits = _check_placeholders(code_files)
    results.append(CheckResult(
        id="no_placeholder",
        title="未残留占位符",
        severity=Severity.PASS if not placeholder_hits else Severity.FAIL,
        message="无占位符残留" if not placeholder_hits else f"{len(placeholder_hits)} 处占位符未替换",
    ))

    return results


def validate_harmony(root: Path) -> List[CheckResult]:
    results: List[CheckResult] = []

    pkg = _read(root, "oh-package.json5")
    has_dep = "@dn-sdk/harmony" in pkg
    results.append(CheckResult(
        id="dep_installed",
        title="oh-package.json5 已引用 @dn-sdk/harmony",
        severity=Severity.PASS if has_dep else Severity.FAIL,
        message="已引用" if has_dep else "未在 oh-package.json5 发现 @dn-sdk/harmony",
    ))

    code_files = _iter_files(root, {".ts", ".ets"})
    init_hits = _grep_in_files(code_files, r"dnSDK\s*\.\s*init\s*\(")
    start_hits = _grep_in_files(code_files, r"dnSDK\s*\.\s*start\s*\(")
    results.append(CheckResult(
        id="init_call",
        title="dnSDK.init 已调用",
        severity=Severity.PASS if init_hits else Severity.FAIL,
        message=f"找到 {len(init_hits)} 处 init" if init_hits else "未找到 init 调用",
    ))
    results.append(CheckResult(
        id="start_call",
        title="dnSDK.start 已调用",
        severity=Severity.PASS if start_hits else Severity.FAIL,
        message=f"找到 {len(start_hits)} 处 start" if start_hits else "未找到 start 调用",
    ))

    # module.json5 权限
    module_json = _read(root, "entry/src/main/module.json5") or _read(root, "entry/module.json5")
    has_internet = "ohos.permission.INTERNET" in module_json
    results.append(CheckResult(
        id="internet_permission",
        title="module.json5 已声明 INTERNET 权限",
        severity=Severity.PASS if has_internet else Severity.FAIL,
        message="已声明" if has_internet else "未声明 INTERNET 权限",
    ))

    placeholder_hits = _check_placeholders(code_files)
    results.append(CheckResult(
        id="no_placeholder",
        title="未残留占位符",
        severity=Severity.PASS if not placeholder_hits else Severity.FAIL,
        message="无占位符残留" if not placeholder_hits else f"{len(placeholder_hits)} 处占位符未替换",
    ))

    return results


VALIDATORS = {
    "mini-game": validate_mini_game,
    "mini-program": validate_mini_program,
    "android": validate_android,
    "ios": validate_ios,
    "harmony": validate_harmony,
}


# ─────────────────────────────────────────────────────────
# 汇总输出
# ─────────────────────────────────────────────────────────

def _summarize(checks: List[CheckResult]) -> Dict[str, int]:
    return {
        "total": len(checks),
        "pass": sum(1 for c in checks if c.severity == Severity.PASS),
        "warn": sum(1 for c in checks if c.severity == Severity.WARN),
        "fail": sum(1 for c in checks if c.severity == Severity.FAIL),
    }


def _exit_code(summary: Dict[str, int]) -> int:
    if summary["fail"] > 0:
        return 2
    if summary["warn"] > 0:
        return 1
    return 0


def _print_human(sdk_end: str, checks: List[CheckResult], summary: Dict[str, int]) -> None:
    print(f"🔎 DataNexus SDK 接入质量校验（SDK 端：{sdk_end}）")
    print()
    for c in checks:
        icon = {"PASS": "✅", "WARN": "⚠️ ", "FAIL": "❌"}[c.severity]
        print(f"  {icon} [{c.id}] {c.title}")
        print(f"      → {c.message}")
        if c.detail:
            for line in c.detail.splitlines():
                print(f"      {line}")
    print()
    print(f"📊 汇总：PASS {summary['pass']} / WARN {summary['warn']} / FAIL {summary['fail']} （共 {summary['total']} 项）")
    if summary["fail"]:
        print("❌ 存在错误，SDK 可能无法正常工作，请修复后重跑本脚本。")
    elif summary["warn"]:
        print("⚠️ 存在告警，请人工核实；也可继续进入联调阶段。")
    else:
        print("✅ 全部通过！建议继续走 SKILL.md 能力4（联调与数据对账）。")


def main() -> int:
    parser = argparse.ArgumentParser(description="SDK 接入后的自动化校验")
    parser.add_argument("project_root", help="客户项目根目录")
    parser.add_argument(
        "--sdk-end",
        required=True,
        choices=list(VALIDATORS.keys()),
        help="SDK 端",
    )
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"❌ 项目路径不存在：{root}", file=sys.stderr)
        return 2

    checks = VALIDATORS[args.sdk_end](root)
    summary = _summarize(checks)

    if args.json:
        print(json.dumps({
            "sdk_end": args.sdk_end,
            "project_root": str(root),
            "summary": summary,
            "checks": [asdict(c) for c in checks],
        }, ensure_ascii=False, indent=2))
    else:
        _print_human(args.sdk_end, checks, summary)

    return _exit_code(summary)


if __name__ == "__main__":
    sys.exit(main())
