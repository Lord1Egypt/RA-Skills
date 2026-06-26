#!/usr/bin/env python3
"""
Android 开发环境检测脚本
检测 JDK、Android SDK、NDK 版本，推荐兼容的 AGP/Gradle 版本组合
"""

import subprocess
import os
import sys
import json
import re
from pathlib import Path

NATIVE_STRONG_KEYWORDS = (
    "jni",
    "ndk",
    "cmake",
    "externalnativebuild",
    "native lib",
    "native library",
    "native module",
    "native code",
    "c++",
    "cpp",
    "c/c++",
    "so库",
    ".so",
    "原生模块",
    "原生库",
    "本地库",
    "native工程",
)

NATIVE_WEAK_KEYWORDS = (
    "native",
    "底层",
    "性能优化",
    "高性能",
    "c语言",
    "c 语言",
)


def run_command(cmd: list) -> tuple:
    """运行命令并返回 (returncode, stdout, stderr)"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return -1, "", f"Command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out: {cmd[0]}"


def detect_native_intent(prompt: str | None) -> dict:
    """根据提示词判断是否应启用 Native 工程。"""
    if not prompt or not prompt.strip():
        return {
            "native_candidate": False,
            "native_enabled": False,
            "needs_confirmation": False,
            "confidence": "none",
            "matched_strong_keywords": [],
            "matched_weak_keywords": [],
            "reason": "No prompt content provided.",
        }

    normalized = prompt.lower()
    strong_hits = sorted({keyword for keyword in NATIVE_STRONG_KEYWORDS if keyword in normalized})
    weak_hits = sorted({keyword for keyword in NATIVE_WEAK_KEYWORDS if keyword in normalized})

    if strong_hits:
        return {
            "native_candidate": True,
            "native_enabled": True,
            "needs_confirmation": False,
            "confidence": "high",
            "matched_strong_keywords": strong_hits,
            "matched_weak_keywords": weak_hits,
            "reason": "Strong native keywords detected in prompt.",
        }

    if weak_hits:
        return {
            "native_candidate": True,
            "native_enabled": False,
            "needs_confirmation": True,
            "confidence": "medium",
            "matched_strong_keywords": [],
            "matched_weak_keywords": weak_hits,
            "reason": "Weak native signals detected; confirm before enabling native template.",
        }

    return {
        "native_candidate": False,
        "native_enabled": False,
        "needs_confirmation": False,
        "confidence": "none",
        "matched_strong_keywords": [],
        "matched_weak_keywords": [],
        "reason": "No native-related keywords detected.",
    }


def resolve_native_enabled(prompt: str | None, explicit_native_enabled: bool | None = None) -> dict:
    """综合提示词与显式开关，输出最终 native_enabled 决策。"""
    intent = detect_native_intent(prompt)

    if explicit_native_enabled is not None:
        return {
            **intent,
            "native_enabled": bool(explicit_native_enabled),
            "decision_source": "explicit_flag",
        }

    if intent["native_enabled"]:
        source = "strong_keywords"
    elif intent["needs_confirmation"]:
        source = "weak_keywords_confirmation_required"
    else:
        source = "no_signal"

    return {
        **intent,
        "decision_source": source,
    }


def detect_jdk_version() -> dict:
    """检测 JDK 版本"""
    returncode, stdout, stderr = run_command(["java", "-version"])
    
    if returncode != 0 and returncode != -1:
        # java -version 返回非零但仍有输出
        output = stderr if stderr else stdout
    else:
        output = stderr if stderr else stdout
    
    if not output:
        return {"detected": False, "version": None, "error": "JDK not found"}
    
    # 解析版本号 (格式: "17.0.1" 或 "1.8.0_312")
    match = re.search(r'version "(\d+)(?:\.(\d+))?', output)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2)) if match.group(2) else 0
        
        # 处理 Java 8 的特殊版本号 (1.8.x)
        if major == 1 and minor == 8:
            version = 8
        else:
            version = major
        
        return {"detected": True, "version": version, "raw": output.strip()}
    
    return {"detected": False, "version": None, "raw": output.strip()}


def detect_java_home() -> dict:
    """检测 JAVA_HOME 配置及其版本。"""
    java_home = os.environ.get("JAVA_HOME")
    if not java_home:
        return {"configured": False, "path": None, "version": None}

    java_cmd = str(Path(java_home) / "bin" / ("java.exe" if os.name == "nt" else "java"))
    returncode, stdout, stderr = run_command([java_cmd, "-version"])
    output = stderr if stderr else stdout

    if returncode == -1 or not output:
        return {
            "configured": True,
            "path": java_home,
            "version": None,
            "error": "JAVA_HOME is set but java executable could not be run",
        }

    match = re.search(r'version "(\d+)(?:\.(\d+))?', output)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2)) if match.group(2) else 0
        version = 8 if major == 1 and minor == 8 else major
        return {"configured": True, "path": java_home, "version": version, "raw": output.strip()}

    return {"configured": True, "path": java_home, "version": None, "raw": output.strip()}


def detect_path_java() -> dict:
    """检测 PATH 中的 java 可执行文件及版本。"""
    where_cmd = "where" if os.name == "nt" else "which"
    returncode, stdout, stderr = run_command([where_cmd, "java"])
    if returncode != 0 or not stdout.strip():
        return {"detected": False, "path": None, "version": None}

    java_path = stdout.strip().splitlines()[0].strip()
    version_code, version_out, version_err = run_command([java_path, "-version"])
    output = version_err if version_err else version_out
    if version_code == -1 or not output:
        return {"detected": True, "path": java_path, "version": None}

    match = re.search(r'version "(\d+)(?:\.(\d+))?', output)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2)) if match.group(2) else 0
        version = 8 if major == 1 and minor == 8 else major
        return {"detected": True, "path": java_path, "version": version, "raw": output.strip()}

    return {"detected": True, "path": java_path, "version": None, "raw": output.strip()}


def detect_gradle_jdk_context(java_home_info: dict, path_java_info: dict) -> dict:
    """推断 Gradle CLI 最可能使用的 JDK 来源。"""
    if java_home_info.get("configured"):
        warning = None
        if path_java_info.get("detected") and java_home_info.get("version") != path_java_info.get("version"):
            warning = "JAVA_HOME and PATH java point to different JDK versions. Gradle CLI will prefer JAVA_HOME."
        return {
            "gradle_jdk_source": "JAVA_HOME",
            "gradle_jdk_path": java_home_info.get("path"),
            "gradle_jdk_version": java_home_info.get("version"),
            "consistency_warning": warning,
        }

    if path_java_info.get("detected"):
        return {
            "gradle_jdk_source": "PATH",
            "gradle_jdk_path": path_java_info.get("path"),
            "gradle_jdk_version": path_java_info.get("version"),
            "consistency_warning": "JAVA_HOME is not configured. Gradle CLI will fall back to PATH java, which is less stable across shells and machines.",
        }

    return {
        "gradle_jdk_source": "none",
        "gradle_jdk_path": None,
        "gradle_jdk_version": None,
        "consistency_warning": None,
    }


def detect_android_sdk() -> dict:
    """检测 Android SDK"""
    sdk_path = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
    
    if not sdk_path:
        # 尝试常见路径
        common_paths = [
            Path.home() / "Android" / "Sdk",  # Linux
            Path.home() / "Library" / "Android" / "sdk",  # macOS
            Path(os.environ.get("LOCALAPPDATA", "")) / "Android" / "Sdk",  # Windows
        ]
        for path in common_paths:
            if path.exists():
                sdk_path = str(path)
                break
    
    if not sdk_path or not Path(sdk_path).exists():
        return {"detected": False, "path": None, "error": "Android SDK not found"}
    
    # 检测 build-tools 版本
    build_tools_dir = Path(sdk_path) / "build-tools"
    build_tools_versions = []
    if build_tools_dir.exists():
        try:
            build_tools_versions = sorted(
                [d.name for d in build_tools_dir.iterdir() if d.is_dir()],
                reverse=True
            )
        except (FileNotFoundError, PermissionError):
            build_tools_versions = []

    platforms_dir = Path(sdk_path) / "platforms"
    platform_versions = []
    if platforms_dir.exists():
        try:
            platform_versions = sorted(
                [d.name for d in platforms_dir.iterdir() if d.is_dir()],
                reverse=True
            )
        except (FileNotFoundError, PermissionError):
            platform_versions = []

    cmdline_tools_dir = Path(sdk_path) / "cmdline-tools"
    cmdline_tools_installed = cmdline_tools_dir.exists()

    licenses_dir = Path(sdk_path) / "licenses"
    licenses_present = licenses_dir.exists() and any(licenses_dir.iterdir())
    
    return {
        "detected": True,
        "path": sdk_path,
        "build_tools_versions": build_tools_versions[:5],  # 只保留最新的 5 个
        "platform_versions": platform_versions[:5],
        "cmdline_tools_installed": cmdline_tools_installed,
        "licenses_present": licenses_present,
    }


def detect_ndk(sdk_path: str = None) -> dict:
    """检测 NDK"""
    ndk_path = os.environ.get("ANDROID_NDK_HOME") or os.environ.get("NDK_HOME")
    
    if not ndk_path and sdk_path:
        ndk_bundle = Path(sdk_path) / "ndk-bundle"
        if ndk_bundle.exists():
            ndk_path = str(ndk_bundle)
    
    if not ndk_path:
        return {"detected": False, "path": None}
    
    # 读取 NDK 版本
    source_props = Path(ndk_path) / "source.properties"
    if source_props.exists():
        try:
            content = source_props.read_text()
            match = re.search(r'Pkg.Revision\s*=\s*([\d.]+)', content)
            if match:
                return {"detected": True, "path": ndk_path, "version": match.group(1)}
        except (FileNotFoundError, PermissionError, OSError):
            pass
    
    return {"detected": True, "path": ndk_path, "version": "unknown"}


def recommend_config(jdk_version: int = None) -> dict:
    """根据 JDK 版本推荐配置"""
    if jdk_version is None or jdk_version < 11:
        return {
            "config": "legacy",
            "agp": "7.4.2",
            "gradle": "7.5",
            "kotlin": "1.9.22",
            "jdk_required": "11",
            "warning": "JDK 17+ 推荐用于 AGP 8.x+"
        }
    elif jdk_version >= 17:
        # JDK 17+ 可以使用最新版本
        return {
            "config": "stable",
            "agp": "8.7.0",
            "gradle": "8.9",
            "kotlin": "2.0.21",
            "jdk_required": "17",
            "warning": None
        }
    elif jdk_version >= 11:
        # JDK 11-16 使用 AGP 7.x
        return {
            "config": "compatible",
            "agp": "7.4.2",
            "gradle": "7.5",
            "kotlin": "1.9.22",
            "jdk_required": "11",
            "warning": "建议升级到 JDK 17 以使用 AGP 8.x+"
        }
    else:
        return {
            "config": "unknown",
            "agp": "7.4.2",
            "gradle": "7.5",
            "kotlin": "1.9.22",
            "jdk_required": "11",
            "warning": "无法确定 JDK 版本，使用保守配置"
        }


def assess_environment(
    jdk_info: dict,
    java_home_info: dict,
    path_java_info: dict,
    gradle_jdk_context: dict,
    sdk_info: dict,
    ndk_info: dict
) -> dict:
    """评估当前环境是否适合直接生成并构建 stable 配置。"""
    blocking_issues = []
    warnings = []

    if not jdk_info.get("detected"):
        blocking_issues.append("JDK not detected. Install JDK 17 before generating a stable AGP 8.x project.")
    elif (jdk_info.get("version") or 0) < 17:
        blocking_issues.append("JDK 17+ is required for the default stable profile.")

    if gradle_jdk_context.get("consistency_warning"):
        warnings.append(gradle_jdk_context["consistency_warning"])

    if jdk_info.get("detected") and not java_home_info.get("configured"):
        warnings.append("JAVA_HOME is not configured. Configure JAVA_HOME or use a project-level Gradle JDK setting for reproducible builds.")

    if java_home_info.get("configured") and java_home_info.get("version") and java_home_info.get("version") < 17:
        blocking_issues.append("JAVA_HOME points to a JDK below 17, which is incompatible with the default stable profile.")

    if not sdk_info.get("detected"):
        blocking_issues.append("Android SDK not detected.")
    else:
        if not sdk_info.get("build_tools_versions"):
            blocking_issues.append("Android SDK is missing build-tools.")
        if "android-35" not in sdk_info.get("platform_versions", []):
            blocking_issues.append("Android SDK is missing platforms/android-35 for the stable profile.")
        if not sdk_info.get("cmdline_tools_installed"):
            warnings.append("Android cmdline-tools not detected; wrapper generation and sdkmanager workflows may fail.")
        if not sdk_info.get("licenses_present"):
            blocking_issues.append("Android SDK licenses not accepted or licenses directory is missing.")

    if not ndk_info.get("detected"):
        warnings.append("NDK not detected. This is fine for non-NDK projects.")

    status = "ready"
    if blocking_issues:
        status = "blocked"
    elif warnings:
        status = "degraded"

    return {
        "ready_for_build": len(blocking_issues) == 0,
        "status": status,
        "blocking_issues": blocking_issues,
        "warnings": warnings,
    }


def main(prompt: str | None = None, native_enabled: bool | None = None):
    """主函数"""
    print("=" * 50)
    print("Android 开发环境检测")
    print("=" * 50)
    print()
    
    # 检测 JDK
    print("检测 JDK...")
    jdk_info = detect_jdk_version()
    if jdk_info["detected"]:
        print(f"  [OK] JDK 版本: {jdk_info['version']}")
    else:
        print(f"  [X] 未检测到 JDK: {jdk_info.get('error', '未知错误')}")
    print()

    print("检测 JAVA_HOME...")
    java_home_info = detect_java_home()
    if java_home_info["configured"]:
        print(f"  [OK] JAVA_HOME: {java_home_info['path']}")
    else:
        print("  [-] JAVA_HOME 未配置")
    print()

    print("检测 PATH 中的 java...")
    path_java_info = detect_path_java()
    if path_java_info["detected"]:
        print(f"  [OK] PATH java: {path_java_info['path']}")
    else:
        print("  [-] PATH 中未检测到 java")
    print()

    gradle_jdk_context = detect_gradle_jdk_context(java_home_info, path_java_info)
    print("Gradle CLI JDK 来源...")
    print(f"  来源: {gradle_jdk_context['gradle_jdk_source']}")
    if gradle_jdk_context.get("gradle_jdk_path"):
        print(f"  路径: {gradle_jdk_context['gradle_jdk_path']}")
    if gradle_jdk_context.get("consistency_warning"):
        print(f"  [!] {gradle_jdk_context['consistency_warning']}")
    print()
    
    # 检测 Android SDK
    print("检测 Android SDK...")
    sdk_info = detect_android_sdk()
    if sdk_info["detected"]:
        print(f"  [OK] SDK 路径: {sdk_info['path']}")
        if sdk_info['build_tools_versions']:
            print(f"  [OK] Build Tools: {', '.join(sdk_info['build_tools_versions'][:3])}")
    else:
        print(f"  [X] 未检测到 Android SDK")
    print()
    
    # 检测 NDK
    print("检测 NDK...")
    ndk_info = detect_ndk(sdk_info.get("path"))
    if ndk_info["detected"]:
        print(f"  [OK] NDK 路径: {ndk_info['path']}")
        if ndk_info.get("version"):
            print(f"  [OK] NDK 版本: {ndk_info['version']}")
    else:
        print(f"  [-] 未检测到 NDK (可选)")
    print()
    
    # 推荐配置
    print("=" * 50)
    print("推荐配置")
    print("=" * 50)
    config = recommend_config(jdk_info.get("version"))
    print(f"  配置方案: {config['config']}")
    print(f"  AGP 版本: {config['agp']}")
    print(f"  Gradle 版本: {config['gradle']}")
    print(f"  Kotlin 版本: {config['kotlin']}")
    print(f"  JDK 要求: {config['jdk_required']}")
    if config.get("warning"):
        print(f"  [!] {config['warning']}")
    print()

    native_decision = resolve_native_enabled(prompt, native_enabled)
    print("=" * 50)
    print("Native 工程触发评估")
    print("=" * 50)
    print(f"  native_candidate: {native_decision['native_candidate']}")
    print(f"  native_enabled: {native_decision['native_enabled']}")
    print(f"  decision_source: {native_decision['decision_source']}")
    if native_decision.get("matched_strong_keywords"):
        print(f"  strong hits: {', '.join(native_decision['matched_strong_keywords'])}")
    if native_decision.get("matched_weak_keywords"):
        print(f"  weak hits: {', '.join(native_decision['matched_weak_keywords'])}")
    if native_decision.get("needs_confirmation"):
        print("  [!] 仅命中弱信号，建议二次确认是否启用 native 模板。")
    print()
    
    # 输出 JSON 格式（供 AI 解析）
    result = {
        "jdk": jdk_info,
        "java_home": java_home_info,
        "path_java": path_java_info,
        "gradle_jdk_context": gradle_jdk_context,
        "android_sdk": sdk_info,
        "ndk": ndk_info,
        "native_decision": native_decision,
        "recommended_config": config,
        "environment_assessment": assess_environment(
            jdk_info,
            java_home_info,
            path_java_info,
            gradle_jdk_context,
            sdk_info,
            ndk_info
        )
    }
    
    print("JSON 输出:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Android environment and native-intent detector")
    parser.add_argument("--prompt", default=None, help="User prompt text used for native keyword detection.")
    parser.add_argument(
        "--native-enabled",
        choices=["true", "false"],
        default=None,
        help="Explicitly override native_enabled decision.",
    )
    args = parser.parse_args()

    explicit_native = None
    if args.native_enabled is not None:
        explicit_native = args.native_enabled.lower() == "true"

    main(prompt=args.prompt, native_enabled=explicit_native)
