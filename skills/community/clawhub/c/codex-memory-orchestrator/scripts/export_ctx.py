#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 Codex rollout jsonl 转成 ctxcompress 可消费的 messages 数组。

兼容真实 rollout 结构：桌面/App 的 rollout-*.jsonl 中消息存放在顶层
"response_item"."payload"（payload.type == "message"，role 可为
developer / user / assistant）；同时保留旧式顶层 response_item / message
/ role 三类格式，向前兼容历史上的 CLI 导出。
只保留 user / assistant 交换轮（跳过 developer / system 指令），避免把
系统提示灌进压缩内容。
"""


try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import argparse
import glob
import json
import os
import sys
from pathlib import Path

_INTERESTING_ROLES = {"user", "assistant"}


def _text(item):
    c = item.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        parts = []
        for p in c:
            if not isinstance(p, dict):
                parts.append(str(p))
                continue
            t = p.get("type", "")
            if t in ("text", "input_text", "output_text"):
                parts.append(p.get("text", "") or "")
            else:
                parts.append(p.get("text") or p.get("content") or "")
        return "".join(parts)
    return ""


def _as_message_obj(obj):
    """从一条 rollout 行里取出 message 本体；不是消息则返回 None。"""
    if not isinstance(obj, dict):
        return None
    # 真实 App 格式：{"type":"response_item","payload":{"type":"message",...}}
    pl = obj.get("payload")
    if isinstance(pl, dict) and pl.get("type") == "message":
        return pl
    # 旧式/静态对象格式
    ri = obj.get("response_item")
    if isinstance(ri, dict):
        return ri
    m = obj.get("message")
    if isinstance(m, dict):
        return m
    if obj.get("role") in _INTERESTING_ROLES:
        return obj
    return None


def _append_message(msgs, item, limit):
    if not isinstance(item, dict):
        return
    role = item.get("role", "assistant")
    if role not in _INTERESTING_ROLES:
        return
    txt = _text(item)
    if not txt.strip():
        return
    msgs.append({"role": role, "content": txt})
    return bool(limit and len(msgs) >= limit)


def extract(path, limit=0):
    msgs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            item = _as_message_obj(obj)
            if item is None:
                continue
            try:
                if _append_message(msgs, item, limit):
                    break
            except TypeError:
                # limit None 兼容调用方式
                if _append_message(msgs, item, 0):
                    break
    return msgs


def _cwd_matches_project(file, project):
    """真实 rollout 文件名只含 thread id，项目名在 session_meta.payload.cwd 里。"""
    try:
        with open(file, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= 300:
                    break
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if not isinstance(obj, dict) or obj.get("type") != "session_meta":
                    continue
                pl = obj.get("payload") or {}
                return project in str(pl.get("cwd") or "")
    except OSError:
        return False
    return False


def _matches_project(file, project):
    fp = str(file)
    if project in fp:
        return True
    if file.parent.name and project in file.parent.name:
        return True
    return _cwd_matches_project(file, project)


def main():
    ap = argparse.ArgumentParser(description="将 Codex rollout jsonl 转成 messages 数组（兼容真实 payload 结构）")
    ap.add_argument("--input", "-i", required=True, help="rollout jsonl 文件或 glob")
    ap.add_argument("--output", "-o", default="-")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--project", "-p", default="", help="必填项目/会话标识，用于限定读取范围（匹配文件名/父目录/session_meta cwd）")
    ap.add_argument("--allow-all-sessions", action="store_true",
                    help="仅在用户明确确认读取全部会话时使用；否则拒绝全目录通配")
    args = ap.parse_args()

    project = args.project.strip()
    if "**" in args.input and not project and not args.allow_all_sessions:
        sys.stderr.write("拒绝全目录通配：请使用 --project/-p 指定项目并用项目限定路径；确需全量读取时加 --allow-all-sessions 且已获用户明确确认。\n")
        sys.exit(2)

    files = [Path(f) for f in (glob.glob(args.input, recursive=True) or [args.input])]
    files = [f for f in files if f.exists()]
    project = args.project.strip()
    if project:
        keep = [f for f in files if _matches_project(f, project)]
        if not keep:
            sys.stderr.write("未找到与项目标识匹配的 rollout 文件。请核对 --project 与 --input 范围（也会按 session_meta.payload.cwd 匹配）。\n")
            sys.exit(2)
        files = keep

    msgs = []
    for fp in files:
        msgs.extend(extract(str(fp), 0 if args.limit == 0 else args.limit - len(msgs)))
        if args.limit and len(msgs) >= args.limit:
            break

    text = json.dumps(msgs, ensure_ascii=False, indent=2)
    if args.output == "-":
        sys.stdout.write(text + "\n")
    else:
        Path(args.output).write_text(text, encoding="utf-8")
    print(f"# exported {len(msgs)} messages", file=sys.stderr)


if __name__ == "__main__":
    main()
