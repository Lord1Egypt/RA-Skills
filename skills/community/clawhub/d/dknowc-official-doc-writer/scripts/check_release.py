#!/usr/bin/env python3
"""阻止客户信息、API Key 和本地生成物进入 ClawHub 公开包。"""

import re
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
SKIP_PARTS = {".git", "__pycache__", "official-docs"}
SKIP_FILES = {"CHANGE_log.md"}
BANNED_FILES = {"config.ini"}
BANNED_TERMS = (
    "广东省政务服务和数据管理" + "局",
    "广东省政数" + "局",
    "粤政" + "数",
    "粤政" + "易",
)
ALLOWED_API_KEY_VALUES = {"", "your_api_key_here", "你的深知搜索 API Key"}
API_KEY_PATTERN = re.compile(r"(?im)^\s*api_key\s*=\s*([^\s#;]+)\s*$")
SECRET_TOKEN_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")


def main():
    findings = []
    for path in SKILL_ROOT.rglob("*"):
        if path.is_file() and path.name in BANNED_FILES:
            findings.append(f"{path.relative_to(SKILL_ROOT)}: 公开包不得包含真实配置文件")
            continue
        if not path.is_file() or path.name in SKIP_FILES or any(part in SKIP_PARTS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            for term in BANNED_TERMS:
                if term in line:
                    findings.append(f"{path.relative_to(SKILL_ROOT)}:{line_number}: {term}")
        if path.suffix != ".py":
            for match in API_KEY_PATTERN.finditer(text):
                if match.group(1) not in ALLOWED_API_KEY_VALUES:
                    findings.append(f"{path.relative_to(SKILL_ROOT)}: 发现非占位符 api_key")
        if SECRET_TOKEN_PATTERN.search(text):
            findings.append(f"{path.relative_to(SKILL_ROOT)}: 发现疑似 API Key")

    if findings:
        print("发布检查失败：发现客户强相关内容")
        print("\n".join(findings))
        raise SystemExit(1)
    print("发布检查通过：未发现已登记的客户强相关内容")


if __name__ == "__main__":
    main()
