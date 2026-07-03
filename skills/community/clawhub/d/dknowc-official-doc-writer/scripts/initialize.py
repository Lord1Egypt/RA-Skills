#!/usr/bin/env python3
"""检查运行环境，并按用户授权保存可选的本地写作偏好。"""

import argparse
import json
import os
import platform
import shutil
import subprocess
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
PROFILE_PATH = SKILL_ROOT / "config" / "user_profile.json"
FORMAT_PATH = SKILL_ROOT / "config" / "format.json"


def configured_fonts():
    with FORMAT_PATH.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)
    return sorted({
        section.get("font")
        for section in config.values()
        if isinstance(section, dict) and section.get("font")
    })


def installed_font_names():
    system = platform.system()
    if system == "Darwin":
        roots = [Path.home() / "Library/Fonts", Path("/Library/Fonts"), Path("/System/Library/Fonts")]
        filenames = "\n".join(path.name for root in roots if root.exists() for path in root.rglob("*.*"))
        try:
            result = subprocess.run(
                ["system_profiler", "SPFontsDataType"], capture_output=True, text=True,
                check=False, timeout=30,
            )
            return filenames + "\n" + result.stdout
        except (OSError, subprocess.TimeoutExpired):
            return filenames
    if shutil.which("fc-list"):
        result = subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True, check=False)
        return result.stdout
    if system == "Windows":
        root = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
        return "\n".join(path.name for path in root.glob("*.*")) if root.exists() else ""
    return ""


def check_environment():
    names = installed_font_names().lower().replace("_", "")
    fonts = []
    for font in configured_fonts():
        normalized = font.lower().replace("_", "")
        fonts.append({"name": font, "installed": normalized in names})
    return {
        "python": platform.python_version(),
        "python_docx": shutil.which("python3") is not None and _module_available("docx"),
        "config_ini": (SKILL_ROOT / "config.ini").exists(),
        "fonts": fonts,
    }


def _module_available(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def main():
    parser = argparse.ArgumentParser(description="深知写作助手初始化与环境检查")
    parser.add_argument("--organization", help="常用发文机关；不填写则使用 XX单位")
    parser.add_argument("--doc-prefix", help="常用发文字号前缀；不填写则使用 XX")
    parser.add_argument("--region", help="常用搜索地域；不填写则按任务询问")
    parser.add_argument("--print-unit", help="常用印发单位")
    parser.add_argument("--save", action="store_true", help="经用户授权后，将所填设置仅保存到本机")
    args = parser.parse_args()

    if args.save:
        profile = {
            "organization": args.organization or "",
            "doc_prefix": args.doc_prefix or "",
            "region": args.region or "",
            "print_unit": args.print_unit or "",
        }
        PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with PROFILE_PATH.open("w", encoding="utf-8") as profile_file:
            json.dump(profile, profile_file, ensure_ascii=False, indent=2)

    result = check_environment()
    result["profile_saved"] = args.save
    result["profile_path"] = "config/user_profile.json" if args.save else None
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
