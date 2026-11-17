#!/usr/bin/env python3
"""Offline fixture renderer; it never opens a browser or claims online collection."""
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
visible = data["visible"]
print(f"# 《{visible['title']}》章节笔记")
print(f"\n学习目标：{data['learningGoal']}")
print("采集范围：离线页面资料模拟；未读取视频音画面。")
chapters, subtitles = visible.get("chapters", []), visible.get("subtitles", [])
if not chapters and not subtitles and not visible.get("summary"):
    print("\n缺项：未见可用字幕/章节/摘要；仅报告可见标题，不能声称已看完视频。")
    print(f"来源：{data['videoUrl']}（离线模拟资料标注）")
    sys.exit(0)
print("\n| 时间/章节 | 笔记 | 可定位证据 |\n| --- | --- | --- |")


def timestamp_key(value):
    """Sort displayed timestamps numerically while retaining their original text."""
    try:
        parts = [int(part) for part in value.split(":")]
    except (AttributeError, ValueError):
        return (1, value)
    total = 0
    for part in parts:
        total = total * 60 + part
    return (0, total)


entries = []
for item in chapters:
    entries.append((item["time"], "chapter", item))
for item in subtitles:
    entries.append((item["time"], "subtitle", item))

for time, kind, item in sorted(entries, key=lambda entry: timestamp_key(entry[0])):
    if kind == "chapter":
        print(f"| {time} / {item['title']} | 可见章节：{item['title']} | 页面可见章节；{data['videoUrl']} |")
    else:
        print(f"| {time} / 字幕 | {item['text']} | 页面可见字幕；{data['videoUrl']} |")
print("\n缺项：仅依据此离线可见资料模拟；未出现的内容未采集。")
