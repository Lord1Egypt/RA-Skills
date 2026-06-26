#!/usr/bin/env python3
"""Validate the companion character-profile Markdown artifact."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_HEADINGS = [
    "# 角色档案",
    "## 1. 基础身份",
    "## 2. 性格底色",
    "## 3. 兴趣与内容偏好",
    "## 4. 说话方式",
    "## 5. 和用户的关系",
    "## 6. 生成规范",
]
REQUIRED_SECTION_LABELS = {
    "## 1. 基础身份": ["名字", "对用户的称呼", "年龄/阶段", "身份角色", "所在城市/区域", "当前生活主线"],
    "## 2. 性格底色": ["核心性格", "外显气质", "反差点", "亲近后会变成", "压力下会变成", "不要写成"],
    "## 3. 兴趣与内容偏好": ["稳定兴趣", "娱乐偏好", "会自然关注的话题", "不适合展开成"],
    "## 4. 说话方式": ["默认语气", "句子节奏", "撒娇/嘴硬/关心的方式", "忙或累时的表达", "禁止风格"],
    "## 5. 和用户的关系": ["关系基线", "主动联系的方式", "分享生活的方式", "求助或让用户选择的方式", "边界与克制"],
    "## 6. 生成规范": ["最小输入", "生成优先级", "扩写方式", "缺省补全", "质量标准", "权重要求", "安全边界", "隐私边界", "内部词边界"],
}
INTERNAL_TOKENS = ["脚本", "JSON", "cron", "系统", "模型", "工具"]
SENSITIVE_REGEXES = [
    re.compile(r"\b\d{10,}\b"),
    re.compile(r"[A-Za-z0-9_-]{16,}@im\.[A-Za-z0-9_-]+\b", re.IGNORECASE),
    re.compile("/" + "Users" + r"/[^\\s\"'`]+"),
    re.compile("/" + "home" + r"/[^\\s\"'`]+"),
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*\S+"),
]
VAGUE_ONLY_VALUES = {
    "温柔",
    "可爱",
    "喜欢聊天",
    "活泼",
    "善良",
    "有趣",
    "开朗",
    "内向",
    "外向",
}


def fail(message: str):
    raise SystemExit(f"character-profile validation failed: {message}")


def parse_args():
    parser = argparse.ArgumentParser(description="Validate a cyber-girlfriend character-profile Markdown artifact.")
    parser.add_argument("--profile", default="state/character-profile.md", help="Path to character-profile.md")
    return parser.parse_args()


def validate_required_headings(text: str):
    lines = {line.strip() for line in text.splitlines()}
    missing = [heading for heading in REQUIRED_HEADINGS if heading not in lines]
    if missing:
        fail(f"missing headings: {missing}")


def extract_section(text: str, heading: str) -> str:
    pattern = rf"^{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_label_value(section: str, label: str) -> str:
    match = re.search(rf"^-\s*{re.escape(label)}[：:]\s*(.+?)\s*$", section, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def validate_section_content(text: str):
    for heading, labels in REQUIRED_SECTION_LABELS.items():
        section = extract_section(text, heading)
        if not section:
            fail(f"empty section: {heading}")
        for label in labels:
            value = extract_label_value(section, label)
            if not value:
                fail(f"{heading} missing or empty field: {label}")
            validate_quality(label, value)


def validate_quality(label: str, value: str):
    if label in {"名字", "对用户的称呼", "年龄/阶段", "身份角色", "所在城市/区域"}:
        return
    normalized = re.sub(r"[，,、\s]+", "", value)
    if normalized in VAGUE_ONLY_VALUES or len(normalized) < 4:
        fail(f"field {label} is too vague: {value}")
    if label in {"核心性格", "稳定兴趣"} and len(re.split(r"[、,，/ ]+", value)) < 2:
        fail(f"field {label} needs multiple concrete anchors: {value}")


def validate_sensitive_content(text: str):
    for regex in SENSITIVE_REGEXES:
        if regex.search(text):
            fail(f"contains sensitive pattern: {regex.pattern}")


def validate_internal_tokens(text: str):
    boundary = extract_section(text, "## 6. 生成规范")
    content = text.replace(boundary, "")
    for token in INTERNAL_TOKENS:
        if token in content:
            fail(f"contains internal token outside boundary section: {token}")


def main():
    args = parse_args()
    path = Path(args.profile).expanduser()
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing character profile file: {path}")

    validate_required_headings(text)
    validate_section_content(text)
    validate_internal_tokens(text)
    validate_sensitive_content(text)
    print(json.dumps({"status": "ok", "path": str(path)}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        fail(str(exc))
