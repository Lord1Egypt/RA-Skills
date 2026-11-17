#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
extract_session.py - 读取本机 WorkBuddy 会话记录（.jsonl），判定是否具备可总结的历史对话，
并把对话抽取为一份干净的 transcript.md 供后续写作使用。

用法:
    # 前置检查：当前会话是否已有足够可读取的历史对话
    python extract_session.py --check

    # 抽取对话记录到指定目录（输出 transcript.md）
    python extract_session.py --out-dir ./_session_dump

    # 指定其它会话（默认取当前工作区对应的最新会话）
    python extract_session.py --project-slug <工作区slug> --out-dir ./dump
    python extract_session.py --session-file "/path/to/<会话ID>.jsonl" --out-dir ./dump

    # 会话记录不在默认位置时，显式指定根目录
    python extract_session.py --projects-root "D:/data/projects" --check

    # 列出最近 N 个可用会话
    python extract_session.py --list 10

会话根目录按以下优先级确定:
    --projects-root  >  环境变量 WORKBUDDY_PROJECTS  >  ~/.workbuddy/projects

判断规则（--check）:
    ok=True  需要同时满足：找到会话文件 / 用户发言 >= 1 条 / 助手回复 >= 1 条 /
             有效正文字符数 >= --min-chars（默认 200）
    ok=False 时给出 reason，调用方（SKILL.md）应据此直接结束，不启动后续流程。
"""

import argparse
import io
import json
import os
import re
import sys
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

DEFAULT_PROJECTS_ROOT = os.path.join(os.path.expanduser("~"), ".workbuddy", "projects")
PROJECTS_ROOT_ENV = "WORKBUDDY_PROJECTS"

NOISE_PREFIXES = (
    "<command-name>",
    "<local-command-stdout>",
    "<system-reminder>",
    "<user-prompt-submit-hook>",
)
TAG_RE = re.compile(
    r"<(system-reminder|command-name|local-command-stdout|user-prompt-submit-hook)"
    r"[\s\S]*?</\1>",
    re.I,
)


def resolve_projects_root(cli_value=None):
    """会话根目录：--projects-root > 环境变量 WORKBUDDY_PROJECTS > ~/.workbuddy/projects"""
    if cli_value:
        return os.path.abspath(os.path.expanduser(cli_value))
    env = os.environ.get(PROJECTS_ROOT_ENV)
    if env:
        return os.path.abspath(os.path.expanduser(env))
    return DEFAULT_PROJECTS_ROOT


def slugify_path(path):
    """把工作区绝对路径转换成会话目录名。

    例：/home/alice/Wedding/2026-01-01-09-00 -> -home-alice-wedding-2026-01-01-09-00
    规则：去掉盘符冒号，把路径分隔符换成连字符，统一小写。
    """
    p = os.path.abspath(path).replace("\\", "/")
    return p.replace(":", "").replace("/", "-").lower()


def clean_text(text):
    if not isinstance(text, str):
        return ""
    # <user_query> 只是外层包裹标签，内容要保留
    text = re.sub(r"</?user_query[^>]*>", "", text, flags=re.I)
    text = TAG_RE.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def is_noise(text):
    t = text.lstrip()
    return any(t.startswith(p) for p in NOISE_PREFIXES)


def content_to_text(content):
    """jsonl 的 content 可能是 str 或 list[dict]，这里只保留纯文本部分。"""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts = []
    for item in content:
        if not isinstance(item, dict):
            continue
        itype = item.get("type")
        if itype in ("text", "input_text", "output_text"):
            parts.append(item.get("text", "") or "")
        elif itype == "thinking":
            continue  # 思维链不进入素材
        elif itype in ("tool_use", "tool_result", "image", "file"):
            continue
    return "\n".join(parts)


def parse_session(path):
    """返回 (meta, turns)。turns = [{'role','ts','text'}]"""
    meta = {
        "session_file": path,
        "session_id": os.path.splitext(os.path.basename(path))[0],
        "title": "",
        "cwd": "",
        "first_ts": None,
        "last_ts": None,
    }
    turns = []
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue  # 会话正在写入，末尾可能有半行
            rtype = obj.get("type")
            if rtype == "ai-title":
                meta["title"] = obj.get("title") or meta["title"]
                continue
            if rtype == "session-meta":
                m = obj.get("meta") or {}
                meta["cwd"] = meta["cwd"] or m.get("cwd", "")
                meta["title"] = meta["title"] or m.get("title", "")
                continue
            if rtype != "message":
                continue
            role = obj.get("role")
            if role not in ("user", "assistant"):
                continue
            text = clean_text(content_to_text(obj.get("content")))
            if not text or is_noise(text):
                continue
            ts = obj.get("timestamp")
            if isinstance(ts, (int, float)):
                ts = ts / 1000 if ts > 1e11 else ts
            if meta["first_ts"] is None and ts:
                meta["first_ts"] = ts
            if ts:
                meta["last_ts"] = ts
            if not meta["cwd"]:
                meta["cwd"] = obj.get("cwd", "")
            turns.append({"role": role, "ts": ts, "text": text})
    return meta, turns


def find_session_files(projects_root, project_slug=None, limit=None):
    """返回 [(mtime, path)]，按修改时间倒序。"""
    root = projects_root
    if not os.path.isdir(root):
        return []
    hits = []
    if project_slug:
        pdir = os.path.join(root, project_slug)
        if os.path.isdir(pdir):
            for name in os.listdir(pdir):
                if name.endswith(".jsonl"):
                    fp = os.path.join(pdir, name)
                    hits.append((os.path.getmtime(fp), fp))
    else:
        for dirpath, _dirnames, filenames in os.walk(root):
            for name in filenames:
                if name.endswith(".jsonl"):
                    fp = os.path.join(dirpath, name)
                    try:
                        hits.append((os.path.getmtime(fp), fp))
                    except OSError:
                        pass
    hits.sort(reverse=True)
    return hits[:limit] if limit else hits


def resolve_session(args, projects_root):
    if args.session_file:
        p = os.path.abspath(args.session_file)
        return p if os.path.isfile(p) else None
    slug = args.project_slug or (slugify_path(args.cwd) if args.cwd else None)
    hits = find_session_files(projects_root, slug)
    if hits:
        return hits[0][1]
    # 指定项目没命中时，退回全局最近会话，但只在工作区推导失败时允许
    if not args.project_slug:
        hits = find_session_files(projects_root, None)
        return hits[0][1] if hits else None
    return None


def stats(turns):
    u = sum(1 for t in turns if t["role"] == "user")
    a = sum(1 for t in turns if t["role"] == "assistant")
    chars = sum(len(t["text"]) for t in turns)
    return u, a, chars


def fmt_ts(ts):
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ""


def write_transcript(meta, turns, out_dir, per_message=1600, max_chars=24000):
    os.makedirs(out_dir, exist_ok=True)
    lines = [
        "# 会话原始记录（自动抽取）",
        "",
        "- 会话文件：`%s`" % meta["session_file"],
        "- 会话 ID：`%s`" % meta["session_id"],
        "- 标题：%s" % (meta["title"] or "（未命名）"),
        "- 时间：%s ~ %s" % (fmt_ts(meta["first_ts"]), fmt_ts(meta["last_ts"])),
        "- 有效轮次：用户 %d 条 / 助手 %d 条"
        % (
            sum(1 for t in turns if t["role"] == "user"),
            sum(1 for t in turns if t["role"] == "assistant"),
        ),
        "",
        "---",
        "",
    ]
    total = 0
    idx = {"user": 0, "assistant": 0}
    for t in turns:
        idx[t["role"]] += 1
        text = t["text"]
        truncated = False
        if len(text) > per_message:
            text = text[:per_message]
            truncated = True
        if total + len(text) > max_chars:
            lines.append("（后续内容已按字符上限截断，如需完整上下文请直接读取会话 jsonl）")
            break
        total += len(text)
        who = "用户" if t["role"] == "user" else "助手"
        lines.append("## %s #%d  %s" % (who, idx[t["role"]], fmt_ts(t["ts"])))
        lines.append("")
        lines.append(text)
        if truncated:
            lines.append("")
            lines.append("> （本条原文较长，已截断至 %d 字）" % per_message)
        lines.append("")
    out = os.path.join(out_dir, "transcript.md")
    with io.open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只做前置检查，输出 JSON")
    ap.add_argument("--out-dir", help="抽取 transcript.md 的输出目录")
    ap.add_argument("--projects-root", help="会话记录根目录，默认 %s（也可用环境变量 %s 设置）" % (DEFAULT_PROJECTS_ROOT, PROJECTS_ROOT_ENV))
    ap.add_argument("--project-slug")
    ap.add_argument("--session-file")
    ap.add_argument("--cwd", default=os.getcwd())
    ap.add_argument("--min-chars", type=int, default=200)
    ap.add_argument("--min-user-turns", type=int, default=1)
    ap.add_argument("--min-assistant-turns", type=int, default=1)
    ap.add_argument("--per-message", type=int, default=1600)
    ap.add_argument("--max-chars", type=int, default=24000)
    ap.add_argument("--list", type=int, metavar="N", help="列出最近 N 个会话")
    args = ap.parse_args()
    projects_root = resolve_projects_root(args.projects_root)

    if args.list:
        rows = []
        for mtime, fp in find_session_files(projects_root, args.project_slug, args.list):
            try:
                meta, turns = parse_session(fp)
                u, a, c = stats(turns)
                rows.append(
                    {
                        "file": fp,
                        "title": meta["title"],
                        "mtime": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S"),
                        "user_turns": u,
                        "assistant_turns": a,
                        "chars": c,
                    }
                )
            except Exception as e:
                rows.append({"file": fp, "error": str(e)})
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    path = resolve_session(args, projects_root)
    if not path or not os.path.isfile(path):
        print(
            json.dumps(
                {
                    "ok": False,
                    "reason": "未找到可读的会话记录文件（已查找 %s）" % projects_root,
                    "session_file": None,
                },
                ensure_ascii=False,
            )
        )
        return 2

    meta, turns = parse_session(path)
    u, a, chars = stats(turns)

    result = {
        "ok": None,
        "session_file": path,
        "session_id": meta["session_id"],
        "title": meta["title"],
        "cwd": meta["cwd"],
        "projects_root": projects_root,
        "started_at": fmt_ts(meta["first_ts"]),
        "ended_at": fmt_ts(meta["last_ts"]),
        "user_turns": u,
        "assistant_turns": a,
        "chars": chars,
    }

    if u < args.min_user_turns:
        result["ok"] = False
        result["reason"] = "会话中尚无用户提问（user_turns=%d），没有可总结的交互内容。" % u
    elif a < args.min_assistant_turns:
        result["ok"] = False
        result["reason"] = "会话中尚无助手回复（assistant_turns=%d），交互未成闭环，暂不总结。" % a
    elif chars < args.min_chars:
        result["ok"] = False
        result["reason"] = (
            "有效对话正文仅 %d 字（阈值 %d），内容过短，不足以提炼成文章/贴图。" % (chars, args.min_chars)
        )
    else:
        result["ok"] = True
        result["reason"] = "存在可读取的历史对话，可继续。"
        result["preview"] = [t["text"][:120] for t in turns[:4]]

    if args.out_dir:
        out, written = write_transcript(meta, turns, args.out_dir, args.per_message, args.max_chars)
        result["transcript"] = out
        result["transcript_chars"] = written

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
