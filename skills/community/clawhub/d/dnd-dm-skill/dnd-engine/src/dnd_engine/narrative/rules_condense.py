"""规则层瘦身：把「整份规则常驻」改成「常驻摘要 + 按需检索详规」。

现状：DM_RULES.md 等 7 个文件 ≈ 39.6k tok 每轮常驻——这是最大的固定开销，
比模组切片还大。但它们绝大多数内容并不需要每轮都在场。

做法：
1. 按 `## 规则X` 切段，读段首的 `<!-- layer: N -->` 标记；
2. **layer 0 常驻**（红线、会话启动、token 预算这类每轮都要的）→ 进 core；
3. 其余规则只保留「编号 + 标题 + 层」一行索引，需要时按编号取全文；
4. 输出 `rules_core.md`（常驻）与 `rules_index.json`（检索用，含行范围）。
"""

from __future__ import annotations

import json
import pathlib
import re
from typing import Any

from .budget import estimate_tokens

RULE_RE = re.compile(r"^##\s+(规则[0-9A-Za-z.]+)\s*[:：]?\s*(.*)$", re.M)
LAYER_RE = re.compile(r"<!--\s*layer:\s*(\d+)\s*-->")
ALWAYS_ON = (0,)


def _segments(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    marks: list[dict[str, Any]] = []
    for index, line in enumerate(lines, start=1):
        match = RULE_RE.match(line)
        if match:
            marks.append({"rule_id": match.group(1), "title": match.group(2).strip(),
                          "start": index})
    segments: list[dict[str, Any]] = []
    for position, mark in enumerate(marks):
        end = marks[position + 1]["start"] - 1 if position + 1 < len(marks) else len(lines)
        body_lines = lines[mark["start"] - 1:end]
        body = "\n".join(body_lines)
        layer_match = LAYER_RE.search(body)
        title = mark["title"]
        if not title:
            for candidate in body_lines[1:12]:
                stripped = candidate.strip()
                if stripped and not stripped.startswith("<!--"):
                    title = stripped
                    break
        segments.append({
            "rule_id": mark["rule_id"],
            "title": title,
            "layer": int(layer_match.group(1)) if layer_match else 99,
            "start_line": mark["start"],
            "end_line": end,
            "chars": len(body),
            "body": body,
        })
    return segments


def condense_rules(rules_path: pathlib.Path, out_dir: pathlib.Path,
                   extra_files: tuple[pathlib.Path, ...] = ()) -> dict[str, Any]:
    """生成常驻 core 与检索索引；返回统计（含 token 估算）。"""
    text = rules_path.read_text(encoding="utf-8", errors="ignore")
    segments = _segments(text)
    core_segments = [s for s in segments if s["layer"] in ALWAYS_ON]

    core_lines = [f"# 常驻规则核心（layer 0）—— 源自 {rules_path.name}", ""]
    for segment in core_segments:
        core_lines.append(segment["body"].rstrip())
        core_lines.append("")
    core_lines.append("# 规则索引（需要细节时按编号检索详规）")
    for segment in segments:
        core_lines.append(f"- {segment['rule_id']}（layer {segment['layer']}）：{segment['title']}")
    core_text = "\n".join(core_lines)

    out_dir.mkdir(parents=True, exist_ok=True)
    core_path = out_dir / "rules_core.md"
    core_path.write_text(core_text, encoding="utf-8")

    index = {
        "version": 1,
        "source": str(rules_path),
        "rules": [{k: v for k, v in segment.items() if k != "body"} for segment in segments],
        "always_on": [segment["rule_id"] for segment in core_segments],
    }
    index_path = out_dir / "rules_index.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    total_chars = len(text)
    for extra in extra_files:
        if extra.exists():
            total_chars += extra.stat().st_size
    tokens = {
        "core": estimate_tokens(core_text),
        "original": estimate_tokens(text) + sum(
            estimate_tokens(extra.read_text(encoding="utf-8", errors="ignore"))
            for extra in extra_files if extra.exists()),
    }
    tokens["saved"] = tokens["original"] - tokens["core"]
    return {
        "segments": len(segments),
        "always_on": len(core_segments),
        "core_chars": len(core_text),
        "original_chars": total_chars,
        "core_path": str(core_path),
        "index_path": str(index_path),
        "estimated_tokens": tokens,
    }


def load_index(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def rule_body(rules_path: pathlib.Path, rule_id: str) -> str:
    """按编号取某条规则的全文（按需检索用）。"""
    text = rules_path.read_text(encoding="utf-8", errors="ignore")
    for segment in _segments(text):
        if segment["rule_id"] == rule_id:
            return segment["body"]
    return ""


def rules_for_keywords(rules_path: pathlib.Path, keywords: list[str],
                       limit: int = 3) -> list[dict[str, Any]]:
    """关键词检索规则（命中标题或正文），返回最多 limit 条全文。"""
    text = rules_path.read_text(encoding="utf-8", errors="ignore")
    hits: list[tuple[int, dict[str, Any]]] = []
    for segment in _segments(text):
        score = sum(1 for word in keywords if word and word in segment["body"])
        if score:
            hits.append((score, segment))
    hits.sort(key=lambda item: -item[0])
    return [{"rule_id": s["rule_id"], "title": s["title"], "body": s["body"]}
            for _, s in hits[:limit]]
