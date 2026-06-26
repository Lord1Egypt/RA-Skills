#!/usr/bin/env python3
"""Build a browser-loadable Zhouyi Benjing data file from the local source text."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references" / "zhouyi-benjing-source.txt"
OUTPUT = ROOT / "data" / "zhouyi-benjing.js"

LINE_LABELS = ("初九", "初六", "九二", "六二", "九三", "六三", "九四", "六四", "九五", "六五", "上九", "上六")
EXTRA_LABELS = ("用九", "用六")


def compact(value: str) -> str:
    return re.sub(r"\s+", "", value.strip())


def parse_source(text: str) -> list[dict]:
    lines = [line.strip() for line in text.splitlines()]
    hexagrams: list[dict] = []
    i = 0

    while i < len(lines):
        if not re.match(r"^第\s*\S+\s*卦$", lines[i]):
            i += 1
            continue

        number = len(hexagrams) + 1
        i += 1
        while i < len(lines) and not lines[i]:
            i += 1

        name_line = lines[i]
        inline_judgment = ""
        inline_match = re.match(r"^([^：]+)：(.+)$", name_line)
        if inline_match:
            name = inline_match.group(1).strip()
            inline_judgment = inline_match.group(2).strip()
        else:
            name = name_line
        i += 1
        while i < len(lines) and not lines[i]:
            i += 1

        judgment_parts: list[str] = [inline_judgment] if inline_judgment else []
        yao_lines: list[dict] = []
        extra_lines: list[dict] = []

        while i < len(lines):
            line = lines[i]
            if re.match(r"^第\s*\S+\s*卦$", line):
                break
            i += 1
            if not line:
                continue

            match = re.match(r"^([^：]+)：(.+)$", line)
            if not match:
                if judgment_parts and not yao_lines and not extra_lines:
                    judgment_parts.append(line)
                continue

            label, text_part = match.group(1), match.group(2)
            if label in LINE_LABELS:
                yao_lines.append({"label": label, "text": text_part.strip()})
            elif label in EXTRA_LABELS:
                extra_lines.append({"label": label, "text": text_part.strip()})
            elif compact(label) == compact(name):
                judgment_parts.append(text_part.strip())
            elif judgment_parts and not yao_lines and not extra_lines:
                judgment_parts.append(line)

        hexagrams.append(
            {
                "number": number,
                "name": name,
                "judgment": "".join(judgment_parts),
                "lines": yao_lines,
                "extras": extra_lines,
            }
        )

    return hexagrams


def validate(hexagrams: list[dict]) -> None:
    if len(hexagrams) != 64:
        raise SystemExit(f"expected 64 hexagrams, got {len(hexagrams)}")

    for item in hexagrams:
        if not item["judgment"]:
            raise SystemExit(f"hexagram {item['number']} {item['name']} has no judgment")
        if len(item["lines"]) != 6:
            raise SystemExit(
                f"hexagram {item['number']} {item['name']} expected 6 lines, got {len(item['lines'])}"
            )

    if hexagrams[0]["name"] != "乾" or hexagrams[0]["extras"][0]["label"] != "用九":
        raise SystemExit("乾卦 or 用九 parse failed")
    if hexagrams[1]["name"] != "坤" or hexagrams[1]["extras"][0]["label"] != "用六":
        raise SystemExit("坤卦 or 用六 parse failed")
    if hexagrams[2]["lines"][1]["text"] != "屯如邅如，乘馬班如。匪寇婚媾，女子貞不字，十年乃字。":
        raise SystemExit("屯六二 source text was not preserved exactly")


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    hexagrams = parse_source(text)
    validate(hexagrams)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    payload = json.dumps(hexagrams, ensure_ascii=False, indent=2)
    OUTPUT.write_text(
        "const ZHOUYI_BENJING = "
        + payload
        + ";\n\n"
        + "if (typeof window !== \"undefined\") window.ZHOUYI_BENJING = ZHOUYI_BENJING;\n"
        + "if (typeof module !== \"undefined\") module.exports = ZHOUYI_BENJING;\n",
        encoding="utf-8",
    )
    print(f"wrote {OUTPUT.relative_to(ROOT)} with {len(hexagrams)} hexagrams")


if __name__ == "__main__":
    main()
