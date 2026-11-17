#!/usr/bin/env python3
"""分镜脚本解析与校验的公共库

被 check_storyboard.py 和 export_shots.py 共用，避免三处重复实现解析器。
"""

import json
import re
from pathlib import Path

GLOBAL_LEARNINGS = Path.home() / ".workbuddy" / "avs" / "learnings.jsonl"
PROJECT_LEARNINGS = Path(".avs") / "learnings.jsonl"

REQUIRED_FIELDS = ["画面", "中文提示词", "英文提示词", "配音", "字幕"]
FIELD_RE = re.compile(r"^(画面|中文提示词|英文提示词|配音|字幕)\s*[：:]\s*(.*)$")
SHOT_RE = re.compile(r"^##\s*镜头\s*(\d+)")
TIME_RE = re.compile(r"(\d+)\s*[-–—]\s*(\d+)\s*秒")
HEADING_RE = re.compile(r"^#{1,6}\s")

DEFAULT_STYLE_CN = "竖屏 9:16，电影级打光，干净的极简科技风，柔和景深，画面稳定无闪烁。"
DEFAULT_STYLE_EN = (
    "vertical 9:16, cinematic lighting, clean minimal tech aesthetic, "
    "soft depth of field, stable frames, no flicker."
)
DEFAULT_NEGATIVE_CN = "变形文字，乱码字符，水印，商标 logo，画面闪烁，过度饱和，廉价广告风"
DEFAULT_NEGATIVE_EN = (
    "distorted text, garbled characters, watermark, brand logo, flicker, "
    "oversaturation, cheap advertising style"
)
TEXT_RISK = ["写着", "字样", "文字", "标题显示", "打印出", "浮现出", "海报上出现"]
NUMBER_RISK = re.compile(r"(\d+(\.\d+)?\s*(元|美元|块|万|亿|%|％|毫秒|秒))|(¥\s*\d+)|(\$\s*\d+)")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def cn_len(text):
    """统计中文字数，忽略空白和标点，用于估算朗读时长"""
    return len(CJK_RE.findall(text))


def parse(content):
    """把分镜 Markdown 解析成结构化镜头列表"""
    shots = []
    current = None
    field = None
    for raw in content.splitlines():
        line = raw.replace("**", "").strip()
        if not line or HEADING_RE.match(line) and not SHOT_RE.match(line):
            # 保留镜头标题，忽略其它层级的标题行
            if HEADING_RE.match(line):
                field = None
            continue
        m = SHOT_RE.match(line)
        if m:
            if current:
                shots.append(current)
            t = TIME_RE.search(line)
            current = {
                "index": int(m.group(1)),
                "title": line,
                "start": int(t.group(1)) if t else None,
                "end": int(t.group(2)) if t else None,
                "fields": {},
            }
            field = None
            continue
        if current is None:
            continue
        f = FIELD_RE.match(line)
        if f:
            field = f.group(1)
            current["fields"][field] = f.group(2).strip()
        elif field:
            current["fields"][field] = (current["fields"][field] + " " + line).strip()
    if current:
        shots.append(current)
    return shots


def read_global(content, heading):
    """读取「## 全局风格前缀」这类小节里的第一段内容，返回 (中文行, 英文行)"""
    lines = content.splitlines()
    inside = False
    collected = []
    for raw in lines:
        line = raw.strip()
        if re.match(r"^##\s*" + heading, line):
            inside = True
            continue
        if inside:
            if line.startswith("## ") or line == "---":
                break
            if line:
                collected.append(line)
    cn = next((l for l in collected if CJK_RE.search(l)), "")
    en = next((l for l in collected if l and not CJK_RE.search(l)), "")
    return cn, en


def load_avoid_words():
    """从经验文件里读出历史累积的画面禁用词，让过去的教训变成今天的检查项"""
    words = {}
    for p in (GLOBAL_LEARNINGS, PROJECT_LEARNINGS):
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("kind") == "avoid" and obj.get("text"):
                words[obj["text"]] = obj.get("why", "")
    return words


def check(shots, style_cn="", style_en="", speech_rate=4.5, extra_avoid=None):
    """返回 (errors, warnings, stats)"""
    errors, warnings = [], []
    total = 0

    for s in shots:
        name = f"镜头 {s['index']}"
        missing = [f for f in REQUIRED_FIELDS if not s["fields"].get(f)]
        if missing:
            errors.append(f"E1 {name} 缺少字段：{'、'.join(missing)}")

        placeholders = [
            f for f in REQUIRED_FIELDS
            if f in s["fields"] and re.search(r"TODO|待定|TBD", s["fields"][f] or "", re.I)
        ]
        if placeholders:
            errors.append(f"E9 {name} 以下字段还是占位符没有填：{'、'.join(placeholders)}")

        duration = None
        if s["start"] is None or s["end"] is None:
            errors.append(f"E5 {name} 标题里找不到起止秒，格式应为（12-22 秒）")
        else:
            duration = s["end"] - s["start"]
            if duration <= 0:
                errors.append(f"E5 {name} 时长为非正数：{s['start']}-{s['end']} 秒")
            elif duration > 8:
                warnings.append(f"W5 {name} 时长 {duration} 秒超过 8 秒，观众容易走神")
            total = max(total, s["end"])

        vo = s["fields"].get("配音", "")
        if vo and duration:
            budget = int(duration * speech_rate)
            used = cn_len(vo)
            if used > budget:
                errors.append(f"E2 {name} 配音 {used} 字超出 {duration} 秒可容纳的 {budget} 字")
            elif used < duration * 2.2:
                warnings.append(f"W6 {name} 配音仅 {used} 字，{duration} 秒的画面太空，建议补信息")

        canvas = s["fields"].get("画面", "")
        for w in TEXT_RISK:
            if w in canvas:
                errors.append(f"E3 {name} 画面描述含「{w}」，模型会渲染出乱码，请改为后期叠加字幕")
                break

        prompt = s["fields"].get("中文提示词", "")
        if prompt:
            if len(prompt) < 15:
                warnings.append(f"W2 {name} 中文提示词仅 {len(prompt)} 字，可能太笼统")
            elif len(prompt) > 200:
                warnings.append(f"W2 {name} 中文提示词 {len(prompt)} 字，可能过长导致模型抓不住重点")
            if style_cn and style_cn not in prompt:
                errors.append(f"E6 {name} 中文提示词没有带上全局风格前缀，七个镜头会像七部不同的片子")

        for word, why in (extra_avoid or {}).items():
            if word and word in canvas + " " + prompt:
                tail = f"，{why}" if why else ""
                errors.append(f"E8 {name} 命中历史禁用词「{word}」{tail}")
                break

        en = s["fields"].get("英文提示词", "")
        if en:
            if CJK_RE.search(en):
                errors.append(f"E7 {name} 英文提示词里混入了中文字符")
            if style_en and style_en not in en:
                errors.append(f"E6 {name} 英文提示词没有带上全局风格前缀")

        sub = s["fields"].get("字幕", "")
        if sub and len(sub) > 15:
            warnings.append(f"W4 {name} 字幕 {len(sub)} 字超过 15 字，竖屏一行放不下")

        hit = NUMBER_RISK.search(canvas + " " + prompt)
        if hit:
            warnings.append(f"W1 {name} 画面或提示词出现数字「{hit.group(0)}」，建议移出画面只保留配音")

    n = len(shots)
    if not 6 <= n <= 9:
        errors.append(f"E4 镜头数 {n} 不在 6 到 9 之间")

    prev_end = None
    for i, s in enumerate(shots):
        if i == 0 and s["start"] != 0:
            errors.append("E5 第一个镜头起点应为 0 秒")
        if prev_end is not None and s["start"] is not None and s["start"] != prev_end:
            errors.append(f"E5 镜头 {s['index']} 起点 {s['start']} 秒与上一镜头终点 {prev_end} 秒对不上")
        if s["end"] is not None:
            prev_end = s["end"]

    stats = {"shots": n, "total": total, "speech_rate": speech_rate}
    return errors, warnings, stats
