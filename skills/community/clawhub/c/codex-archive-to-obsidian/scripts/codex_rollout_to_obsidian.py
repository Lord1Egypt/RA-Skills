#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Codex rollout 会话 → Obsidian Markdown 归档

把 Codex（CLI / 桌面版）的会话记录（rollout *.jsonl）转换成可读的 Markdown，
归档到 Obsidian 知识库，并生成索引。

用法:
    python codex_rollout_to_obsidian.py              # 全量归档
    python codex_rollout_to_obsidian.py --dry-run    # 只预览，不写文件
    python codex_rollout_to_obsidian.py --with-reasoning   # 保留模型思考过程
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# ========== 配置 ==========
SOURCES = [
    Path.home() / ".codex" / "sessions",                               # 当前活动目录
    Path.home() / "_卸载备份_YYYY-MM-DD" / "dot-codex" / "sessions",   # 隔离备份（旧数据，按需改名）
]
VAULT = Path(os.environ.get("OBSIDIAN_VAULT") or (Path.home() / "Documents" / "Obsidian"))
ARCHIVE_DIR = VAULT / "CodexArchive"

MAX_TOOL_OUTPUT = 1500      # 工具输出截断长度
MAX_REASONING = 1200        # 思考过程截断长度（--with-reasoning 时生效）

# 需要剥离的注入噪声（Codex 每轮自动塞进上下文，不属于真实对话）
NOISE_BLOCKS = [
    r"<environment_context>.*?</environment_context>",
    r"<app-context>.*?</app-context>",
    r"<user_instructions>.*?</user_instructions>",
    r"<turn_context>.*?</turn_context>",
    r"<skills_instructions>.*?</skills_instructions>",
    r"<INSTRUCTIONS>.*?</INSTRUCTIONS>",
    r"# AGENTS\.md instructions.*?(?=\n\n|\Z)",
    r"<permissions.*?</permissions>",
    r"<filesystem.*?</filesystem>",
    r"<workspace_roots>.*?</workspace_roots>",
]
NOISE_RE = re.compile("|".join(NOISE_BLOCKS), re.DOTALL)
ILLEGAL_FN = re.compile(r'[\\/:*?"<>|\r\n\t]+')


def clean_user_text(text: str) -> str:
    """剥离注入噪声，返回真实用户输入（可能为空）"""
    t = NOISE_RE.sub("", text or "").strip()
    # 剥完只剩零散的 XML 残片或空行，就丢弃
    t = re.sub(r"</?[a-z_\-]+[^>]*>", "", t).strip()
    return t


def truncate(s: str, n: int) -> str:
    s = s or ""
    return s if len(s) <= n else s[:n].rstrip() + f"\n\n_…（已截断，原文 {len(s)} 字）_"


def parse_rollout(path: Path) -> dict | None:
    """解析单个 rollout jsonl，返回结构化会话"""
    meta, items = {}, []
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = obj.get("type")
                p = obj.get("payload") or {}
                if t == "session_meta":
                    meta = p
                elif t == "response_item":
                    items.append((obj.get("ordinal", 0), p))
    except OSError as e:
        print(f"  [跳过] 读取失败 {path.name}: {e}", file=sys.stderr)
        return None

    if not meta:
        return None

    # 按 ordinal 排序，保证时间顺序
    items.sort(key=lambda x: x[0])

    turns, user_count, asst_count, tool_count = [], 0, 0, 0
    pending_calls: dict[str, dict] = {}

    for _, p in items:
        ptype = p.get("type")
        role = p.get("role")

        if ptype == "message" and role == "user":
            texts = [clean_user_text(c.get("text", "")) for c in (p.get("content") or [])]
            text = "\n\n".join(x for x in texts if x)
            if text:
                user_count += 1
                turns.append({"kind": "user", "text": text})

        elif ptype == "message" and role == "assistant":
            text = "\n\n".join(
                c.get("text", "") for c in (p.get("content") or []) if c.get("text")
            ).strip()
            if text:
                asst_count += 1
                turns.append({"kind": "assistant", "text": text})

        elif ptype == "reasoning":
            text = "\n\n".join(
                c.get("text", "") for c in (p.get("content") or []) if c.get("text")
            ).strip()
            if text:
                turns.append({"kind": "reasoning", "text": text})

        elif ptype == "function_call":
            tool_count += 1
            name = p.get("name", "tool")
            try:
                args = json.loads(p.get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {"raw": p.get("arguments")}
            summary = args.get("cmd") or args.get("command") or json.dumps(
                args, ensure_ascii=False
            )
            node = {"kind": "tool", "name": name, "arg": truncate(str(summary), 400), "output": ""}
            turns.append(node)
            pending_calls[p.get("call_id")] = node

        elif ptype == "function_call_output":
            node = pending_calls.pop(p.get("call_id"), None)
            if node is not None:
                node["output"] = truncate(str(p.get("output", "")), MAX_TOOL_OUTPUT)

        elif ptype == "web_search_call":
            tool_count += 1
            action = p.get("action") or {}
            qs = action.get("queries") or []
            turns.append(
                {
                    "kind": "tool",
                    "name": "web_search",
                    "arg": " / ".join(str(q) for q in qs if q),
                    "output": "",
                }
            )

    if not turns:
        return None

    # 标题：取首条真实用户输入
    title = next((t["text"] for t in turns if t["kind"] == "user"), "（无用户提问）")
    title = re.sub(r"\s+", " ", title).strip()

    ts_raw = meta.get("timestamp") or ""
    try:
        dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00")).astimezone()
    except (ValueError, AttributeError):
        dt = datetime.now(timezone.utc).astimezone()

    return {
        "path": path,
        "id": meta.get("id") or meta.get("session_id") or path.stem,
        "dt": dt,
        "cwd": meta.get("cwd", ""),
        "cli_version": meta.get("cli_version", ""),
        "provider": meta.get("model_provider", ""),
        "originator": meta.get("originator", ""),
        "turns": turns,
        "stats": Counter(
            user=user_count, assistant=asst_count, tool=tool_count
        ),
        "title": title[:60],
        "size": path.stat().st_size,
    }


def render_md(s: dict, with_reasoning: bool) -> str:
    conv = s["id"][:8]
    lines = [
        "---",
        f'title: "{s["title"].replace(chr(34), chr(39))}"',
        f"date: {s['dt'].strftime('%Y-%m-%d %H:%M')}",
        f"session: {s['id']}",
        f"cwd: '{s['cwd']}'",
        f"provider: {s['provider']}",
        f"cli: {s['cli_version']}",
        "tags:",
        "  - codex",
        "  - codex-archive",
        "---",
        "",
        f"# {s['title']}",
        "",
        "> [!info] 会话信息",
        f"> **会话 ID**：`{s['id']}`  ",
        f"> **时间**：{s['dt'].strftime('%Y-%m-%d %H:%M')}  ",
        f"> **工作目录**：`{s['cwd']}`  ",
        f"> **模型供应商**：{s['provider']} ｜ **客户端**：{s['originator']} `{s['cli_version']}`  ",
        f"> **规模**：{s['stats']['user']} 轮提问 ｜ {s['stats']['assistant']} 条回复 ｜ {s['stats']['tool']} 次工具调用",
        "",
        "---",
        "",
    ]
    for t in s["turns"]:
        k = t["kind"]
        if k == "user":
            lines += ["## 👤 用户", "", t["text"], ""]
        elif k == "assistant":
            lines += ["## 🤖 Codex", "", t["text"], ""]
        elif k == "reasoning":
            if with_reasoning:
                lines += [
                    "<details>",
                    "<summary>💭 思考过程</summary>",
                    "",
                    truncate(t["text"], MAX_REASONING),
                    "",
                    "</details>",
                    "",
                ]
        elif k == "tool":
            lines += [
                f"<details>",
                f"<summary>🔧 工具调用 · <code>{t['name']}</code></summary>",
                "",
            ]
            if t["arg"]:
                lines += ["```", t["arg"], "```", ""]
            if t["output"]:
                lines += ["**输出：**", "", "```", t["output"], "```", ""]
            lines += ["</details>", ""]

    lines += ["---", "", f"*归档自 `{s['path']}`（{s['size']/1024:.0f} KB）*", ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只预览，不写文件")
    ap.add_argument("--with-reasoning", action="store_true", help="保留模型思考过程")
    ap.add_argument("--keep-all", action="store_true", help="保留连通性测试之类的琐碎会话")
    ap.add_argument("--min-chars", type=int, default=160,
                    help="会话总字数低于该值视为测试，跳过（默认 160）")
    args = ap.parse_args()

    files: list[Path] = []
    for src in SOURCES:
        if src.exists():
            files += list(src.rglob("*.jsonl"))
        else:
            print(f"[提示] 来源不存在，跳过: {src}")

    if not files:
        print("没有找到任何 rollout 文件。")
        return 1

    print(f"扫描到 {len(files)} 个会话文件\n")

    sessions, seen_ids = [], set()
    for f in sorted(files):
        s = parse_rollout(f)
        if not s:
            continue
        if s["id"] in seen_ids:      # 多来源去重，保留首次遇到的
            continue
        seen_ids.add(s["id"])
        sessions.append(s)

    sessions.sort(key=lambda x: x["dt"])

    if not args.keep_all:
        # 只统计用户提问 + 模型回复的正文（不含思考过程与工具输出）
        def body_len(s: dict) -> int:
            return sum(len(t.get("text", "")) for t in s["turns"]
                       if t["kind"] in ("user", "assistant"))

        trivial = [s for s in sessions if body_len(s) < args.min_chars]
        if trivial:
            print(f"跳过 {len(trivial)} 个琐碎/测试会话（--keep-all 可保留）：")
            for s in trivial:
                print(f"  · {s['dt'].strftime('%m-%d %H:%M')}  {s['title'][:34]}")
            print()
        sessions = [s for s in sessions if s not in trivial]

    print(f"有效会话 {len(sessions)} 个\n")

    if args.dry_run:
        for s in sessions:
            print(f"  {s['dt'].strftime('%Y-%m-%d %H:%M')}  {s['id'][:8]}  "
                  f"{s['stats']['user']}问/{s['stats']['assistant']}答  {s['title'][:40]}")
        print("\n（--dry-run 模式，未写入任何文件）")
        return 0

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    index_rows, written = [], 0

    for s in sessions:
        day_dir = ARCHIVE_DIR / s["dt"].strftime("%Y-%m-%d")
        day_dir.mkdir(parents=True, exist_ok=True)
        fname = f"{s['dt'].strftime('%H%M')}-{s['id'][:8]}-{ILLEGAL_FN.sub('_', s['title'])[:40]}.md"
        out = day_dir / fname
        out.write_text(render_md(s, args.with_reasoning), encoding="utf-8")
        written += 1
        rel = f"CodexArchive/{s['dt'].strftime('%Y-%m-%d')}/{out.stem}"
        index_rows.append(
            f"| {s['dt'].strftime('%Y-%m-%d %H:%M')} | {s['title'][:38]} | "
            f"{s['stats']['user']}/{s['stats']['assistant']}/{s['stats']['tool']} | "
            f"[[{rel}\\|打开]] |"
        )
        print(f"  ✓ {out.relative_to(VAULT)}")

    index = [
        "# Codex 会话归档索引",
        "",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}　｜　"
        f"共 **{written}** 个会话",
        "",
        "| 时间 | 主题 | 提问/回复/工具 | 链接 |",
        "|------|------|------|------|",
        *index_rows,
        "",
    ]
    (ARCHIVE_DIR / "_索引.md").write_text("\n".join(index), encoding="utf-8")
    print(f"\n索引已生成: {(ARCHIVE_DIR / '_索引.md').relative_to(VAULT)}")
    print(f"归档完成，共 {written} 个会话 → {ARCHIVE_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
