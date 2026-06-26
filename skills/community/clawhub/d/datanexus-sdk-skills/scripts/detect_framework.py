#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
detect_framework.py — DataNexus SDK 接入场景识别

目标：在客户项目根目录快速识别
  1. SDK 端：mini-program / mini-game / android / ios / harmony
  2. 开发框架/引擎：native / Taro / uni-app / WePY / mpvue /
                    Cocos Creator / LayaAir / Egret / Unity / ...
  3. 包管理器：npm / CocoaPods / Gradle / ohpm / 手动
  4. 主语言：TypeScript / JavaScript / Java / Kotlin / Objective-C / Swift / ArkTS

使用方式：
    python3 detect_framework.py <project_root>
    python3 detect_framework.py <project_root> --json     # 结构化输出，供 Agent 消费

设计原则：
  - 纯规则匹配，不调用任何 LLM
  - 优先匹配强特征文件（project.config.json / game.json / Podfile 等）
  - 多端项目（monorepo）会返回候选列表，由上层 Agent 再向用户确认
  - 识别失败 → 返回 {sdk_end: "unknown", confidence: 0} 而非抛异常
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ─────────────────────────────────────────────────────────
# 特征定义
# ─────────────────────────────────────────────────────────

# (特征文件，权重) — 权重高的优先
SDK_END_SIGNATURES: Dict[str, List[Tuple[str, int]]] = {
    "mini-game": [
        ("game.json", 100),
        ("project.config.json", 30),  # 也可能是小程序，需二次判断
    ],
    "mini-program": [
        ("app.json", 90),
        ("project.config.json", 30),
        ("project.private.config.json", 20),
        ("miniprogram/app.json", 90),  # 云开发项目
    ],
    "android": [
        ("build.gradle", 90),
        ("build.gradle.kts", 90),
        ("settings.gradle", 40),
        ("AndroidManifest.xml", 30),
        ("app/build.gradle", 100),
        ("app/src/main/AndroidManifest.xml", 80),
    ],
    "ios": [
        ("Podfile", 100),
        ("Package.swift", 50),
    ],
    "harmony": [
        ("oh-package.json5", 100),
        ("build-profile.json5", 80),
        ("entry/module.json5", 90),
        ("entry/src/main/module.json5", 90),
    ],
}

# 框架/引擎特征：依据 package.json 依赖或关键文件
JS_FRAMEWORK_PATTERNS: Dict[str, List[str]] = {
    # 小程序框架
    "Taro": ["@tarojs/taro", "@tarojs/cli"],
    "uni-app": ["@dcloudio/uni-app", "@dcloudio/uni-cli-shared"],
    "WePY": ["wepy", "wepy-cli"],
    "mpvue": ["mpvue"],
    "Kbone": ["@wechatjs/kbone", "kbone"],
    "remax": ["remax"],
    # 小游戏引擎
    "Cocos Creator": ["cc", "cocos-creator-api"],
    "LayaAir": ["laya"],
    "Egret": ["egret-core"],
    "Unity": [],  # Unity 不在 package.json，靠其他文件
}

# 通过文件/目录存在识别的引擎
FILE_BASED_ENGINES: List[Tuple[str, str]] = [
    ("assets/main", "Cocos Creator"),          # Cocos Creator 目录结构
    ("laya/.laya", "LayaAir"),
    ("Assets/Plugins", "Unity"),
    ("ProjectSettings/ProjectVersion.txt", "Unity"),
    ("proj.wx/project.config.json", "Cocos Creator"),  # Cocos 发布到微信小游戏
]

# Podfile 中的 iOS 框架特征
IOS_FRAMEWORK_PATTERNS: Dict[str, List[str]] = {
    "SwiftUI": ["SwiftUI"],
    "Flutter": ["Flutter"],
    "React Native": ["React-Core", "React-RCTCore"],
}

# Android 依赖特征
ANDROID_FRAMEWORK_PATTERNS: Dict[str, List[str]] = {
    "Flutter": ["io.flutter"],
    "React Native": ["com.facebook.react"],
    "Jetpack Compose": ["androidx.compose"],
    "Kotlin": ["org.jetbrains.kotlin"],
}


# ─────────────────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────────────────

def _exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def _read_text(root: Path, rel: str, max_bytes: int = 200_000) -> str:
    p = root / rel
    if not p.exists() or not p.is_file():
        return ""
    try:
        return p.read_text(encoding="utf-8", errors="ignore")[:max_bytes]
    except OSError:
        return ""


def _read_json(root: Path, rel: str) -> Optional[dict]:
    txt = _read_text(root, rel)
    if not txt:
        return None
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        return None


# ─────────────────────────────────────────────────────────
# 检测逻辑
# ─────────────────────────────────────────────────────────

def detect_sdk_ends(root: Path) -> List[Tuple[str, int]]:
    """返回按置信度排序的候选 SDK 端列表"""
    scores: Dict[str, int] = {}
    for sdk_end, sigs in SDK_END_SIGNATURES.items():
        for fname, weight in sigs:
            if _exists(root, fname):
                scores[sdk_end] = scores.get(sdk_end, 0) + weight

    # project.config.json + game.json = mini-game；否则 mini-program
    if "mini-game" in scores and "mini-program" in scores:
        if _exists(root, "game.json"):
            # 明确是小游戏，削弱小程序
            scores["mini-program"] = scores.get("mini-program", 0) - 50

    return sorted(
        [(k, v) for k, v in scores.items() if v > 0],
        key=lambda kv: kv[1],
        reverse=True,
    )


def detect_js_framework(root: Path) -> Optional[str]:
    """从 package.json 依赖识别 JS 侧框架"""
    pkg = _read_json(root, "package.json")
    if not pkg:
        return None
    deps = {}
    deps.update(pkg.get("dependencies", {}) or {})
    deps.update(pkg.get("devDependencies", {}) or {})
    dep_names = set(deps.keys())

    for framework, patterns in JS_FRAMEWORK_PATTERNS.items():
        for p in patterns:
            if p in dep_names:
                return framework
    return None


def detect_file_based_engine(root: Path) -> Optional[str]:
    for path_pattern, engine in FILE_BASED_ENGINES:
        if _exists(root, path_pattern):
            return engine
    # Cocos Creator 3.x 源码项目：package.json 里有 creator.version
    pkg = _read_json(root, "package.json")
    if pkg and isinstance(pkg.get("creator"), dict) and "version" in pkg["creator"]:
        return "Cocos Creator"
    return None


def _infer_cocos_creator_target(root: Path) -> Optional[str]:
    """
    Cocos Creator 3.x 源码项目识别：
      - package.json 里有 creator.version
      - tsconfig.json 里 types 含 minigame-api-typings → mini-game
      - build-templates 里有 wechat-mini-game / bytedance-mini-game → mini-game
      - 上述都没有但有 assets/ + settings/ → 无法确定，返回 None
    """
    pkg = _read_json(root, "package.json") or {}
    creator = pkg.get("creator")
    if not isinstance(creator, dict):
        return None

    # 检查是否是小游戏构建目标
    ts_text = _read_text(root, "tsconfig.json")
    if "minigame-api-typings" in ts_text or "wechat-minigame-api" in ts_text:
        return "mini-game"

    # build-templates 下的发布平台判断
    bt_root = root / "build-templates"
    if bt_root.exists():
        children = {p.name for p in bt_root.iterdir() if p.is_dir()}
        if any(name in children for name in {
            "wechatgame", "wechat-mini-game", "mini-game", "bytedance-mini-game",
        }):
            return "mini-game"
        if any(name in children for name in {
            "wechat-mini-program", "mini-program",
        }):
            return "mini-program"

    return None


def detect_ios_details(root: Path) -> Dict[str, object]:
    podfile_text = _read_text(root, "Podfile")
    uses_cocoapods = bool(podfile_text)
    frameworks_detected: List[str] = []
    for fw, patterns in IOS_FRAMEWORK_PATTERNS.items():
        for p in patterns:
            if p in podfile_text:
                frameworks_detected.append(fw)
                break
    # 语言判断：Package.swift 或 *.swift 文件存在 → Swift；否则 ObjC
    has_swift = _exists(root, "Package.swift") or any(
        p.suffix == ".swift"
        for p in root.rglob("*.swift")
        if "Pods" not in p.parts and ".build" not in p.parts
    )
    language = "Swift" if has_swift else "Objective-C"
    return {
        "package_manager": "CocoaPods" if uses_cocoapods else "Manual",
        "language": language,
        "frameworks": frameworks_detected,
    }


def detect_android_details(root: Path) -> Dict[str, object]:
    # 读取 app/build.gradle 或 build.gradle
    for candidate in ["app/build.gradle", "app/build.gradle.kts", "build.gradle", "build.gradle.kts"]:
        txt = _read_text(root, candidate)
        if txt:
            break
    else:
        txt = ""

    frameworks: List[str] = []
    for fw, patterns in ANDROID_FRAMEWORK_PATTERNS.items():
        for p in patterns:
            if p in txt:
                frameworks.append(fw)
                break

    # 语言：存在 .kt 文件 → Kotlin+Java 混合；否则 Java
    has_kotlin = any(
        p.suffix == ".kt"
        for p in root.rglob("*.kt")
        if "build" not in p.parts
    )
    language = "Kotlin/Java" if has_kotlin else "Java"

    return {
        "package_manager": "Gradle",
        "language": language,
        "frameworks": frameworks,
    }


def detect_harmony_details(root: Path) -> Dict[str, object]:
    pkg = _read_json(root, "oh-package.json5") or _read_json(root, "build-profile.json5")
    uses_ohpm = _exists(root, "oh-package.json5")
    return {
        "package_manager": "ohpm" if uses_ohpm else "Manual",
        "language": "ArkTS",
        "frameworks": [],
    }


def detect_miniprogram_or_game_details(root: Path, sdk_end: str) -> Dict[str, object]:
    pkg = _read_json(root, "package.json") or {}
    framework = detect_js_framework(root)
    engine = detect_file_based_engine(root)

    # 特殊：Cocos Creator 3.x 源码态项目，通过 package.json.creator 推断出来
    # 但此时 FILE_BASED_ENGINES 可能没命中（源码没构建），framework/engine 都是 None
    # 必须强制设为 "Cocos Creator"，否则会 fallback "原生"，generate_init_patch 选不到 Cocos 三段式模板
    if not engine and isinstance(pkg.get("creator"), dict) and "version" in pkg["creator"]:
        engine = "Cocos Creator"

    # 若是 mini-game，优先看引擎
    if sdk_end == "mini-game":
        selected = engine or framework or "原生"
    else:
        selected = framework or "原生"

    # 语言：有 .ts 文件就算 TypeScript
    has_ts = any(
        p.suffix in {".ts", ".tsx"}
        for p in root.rglob("*.ts*")
        if "node_modules" not in p.parts
    )
    return {
        "package_manager": "npm" if _exists(root, "package.json") else "Manual",
        "language": "TypeScript" if has_ts else "JavaScript",
        "framework": selected,
    }


# ─────────────────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────────────────

def detect(root_path: str) -> Dict[str, object]:
    root = Path(root_path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        return {
            "error": f"项目路径不存在或不是目录: {root}",
            "sdk_end": "unknown",
            "confidence": 0,
        }

    candidates = detect_sdk_ends(root)
    if not candidates:
        # 二次推断：Cocos Creator 3.x 源码项目（还没构建时没有 game.json / project.config.json）
        creator_inferred = _infer_cocos_creator_target(root)
        if creator_inferred:
            candidates = [(creator_inferred, 70)]
        else:
            return {
                "sdk_end": "unknown",
                "confidence": 0,
                "candidates": [],
                "auto_integration_supported": False,
                "auto_integration_reason": "未识别出已知的 SDK 端",
                "hint": "未识别出已知的 SDK 端。请人工确认项目类型，或检查是否在项目根目录下运行。",
                "project_root": str(root),
            }

    primary_end, primary_score = candidates[0]
    # 计算置信度（经验公式）
    confidence = min(100, int(primary_score / 100 * 100))

    # 进一步填充详情
    details: Dict[str, object] = {}
    if primary_end in ("mini-program", "mini-game"):
        details = detect_miniprogram_or_game_details(root, primary_end)
    elif primary_end == "android":
        details = detect_android_details(root)
    elif primary_end == "ios":
        details = detect_ios_details(root)
    elif primary_end == "harmony":
        details = detect_harmony_details(root)

    # 是否支持自动化接入（白名单）
    supported = _is_supported_for_auto_integration(primary_end, details)

    result: Dict[str, object] = {
        "sdk_end": primary_end,
        "confidence": confidence,
        "details": details,
        "candidates": [{"sdk_end": c[0], "score": c[1]} for c in candidates],
        "auto_integration_supported": supported["ok"],
        "auto_integration_reason": supported["reason"],
        "project_root": str(root),
    }
    return result


# 白名单判断：仅确定性高的场景允许自动写入代码
SUPPORTED_WHITELIST = {
    "mini-program": {"原生", "Taro", "uni-app"},
    "mini-game": {"原生", "Cocos Creator", "LayaAir"},
    "android": {"Java", "Kotlin/Java"},
    "ios": {"Objective-C", "Swift"},
    "harmony": {"ArkTS"},
}


def _is_supported_for_auto_integration(sdk_end: str, details: Dict[str, object]) -> Dict[str, object]:
    if sdk_end == "unknown":
        return {"ok": False, "reason": "SDK 端未识别，无法自动接入"}

    whitelist = SUPPORTED_WHITELIST.get(sdk_end, set())

    if sdk_end in ("mini-program", "mini-game"):
        fw = details.get("framework", "")
        if fw in whitelist:
            return {"ok": True, "reason": f"{sdk_end} / {fw} 在白名单"}
        return {
            "ok": False,
            "reason": f"框架 '{fw}' 尚未支持自动接入，建议降级到能力2（只展示代码示例）",
        }

    if sdk_end in ("android", "harmony"):
        lang = details.get("language", "")
        if lang in whitelist or lang.startswith("Kotlin"):
            return {"ok": True, "reason": f"{sdk_end} / {lang} 支持自动接入"}

    if sdk_end == "ios":
        lang = details.get("language", "")
        pm = details.get("package_manager", "")
        if lang in whitelist and pm == "CocoaPods":
            return {"ok": True, "reason": "iOS / CocoaPods 项目支持自动接入"}
        return {
            "ok": False,
            "reason": f"iOS 手动集成或 {lang} 项目，建议降级到能力2（只展示代码示例）",
        }

    return {"ok": False, "reason": "默认降级"}


def _print_human(result: Dict[str, object]) -> None:
    if "error" in result:
        print(f"❌ {result['error']}")
        return

    sdk_end = result["sdk_end"]
    confidence = result["confidence"]
    details = result.get("details", {}) or {}
    print(f"🔍 项目场景识别结果")
    print(f"  SDK 端：{sdk_end}  （置信度 {confidence}%）")
    if details:
        for k, v in details.items():
            print(f"  {k}: {v}")
    print()
    print(f"🎯 自动化接入：{'✅ 支持' if result['auto_integration_supported'] else '⚠️ 不支持'}")
    print(f"  原因：{result['auto_integration_reason']}")
    if not result["auto_integration_supported"]:
        print("  建议：走 SKILL.md 能力2（接入开发指引），只展示代码示例不自动写入。")

    if len(result.get("candidates", [])) > 1:
        print()
        print("⚠️ 同时检测到多种 SDK 端候选（monorepo？）：")
        for c in result["candidates"]:
            print(f"  - {c['sdk_end']} (score={c['score']})")
        print("  请人工确认目标接入的 SDK 端。")


def main() -> int:
    parser = argparse.ArgumentParser(description="识别 DataNexus SDK 接入场景")
    parser.add_argument("project_root", help="客户项目根目录")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出（供 Agent 消费）")
    args = parser.parse_args()

    result = detect(args.project_root)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_human(result)

    return 0 if result.get("sdk_end") != "unknown" else 1


if __name__ == "__main__":
    sys.exit(main())
