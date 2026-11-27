#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Claude Code 适配器：~/.claude/projects/**/*.jsonl。"""
import os, json
from .base import BaseAdapter, task, token, pick_task, load_noise_markers, all_homes, find_files


class ClaudeAdapter(BaseAdapter):
    name = "ClaudeCode"

    def _files(self):
        seen = set()
        for h in all_homes():
            loc = "WSL" if ("wsl.localhost" in h or "wsl$" in h) else "Win"
            for sub in ("projects", "transcripts"):
                base = os.path.join(h, ".claude", sub)
                if not os.path.isdir(base):
                    continue
                for fp in find_files([base], "*.jsonl", exclude=("/subagents/", "\\subagents\\")):
                    k = os.path.normcase(os.path.abspath(fp))
                    if k not in seen:
                        seen.add(k)
                        yield fp, f"{loc}/{sub}"

    def extract_tasks(self):
        rows = []
        noise = load_noise_markers()
        for fp, loc in self._files():
            sid = os.path.splitext(os.path.basename(fp))[0]
            first_ts = cwd = ""
            user_cnt = 0
            candidates = []
            try:
                for line in open(fp, encoding="utf-8", errors="replace"):
                    try:
                        d = json.loads(line)
                    except Exception:
                        continue
                    t = d.get("type")
                    msg = d.get("message") or {}
                    content = msg.get("content") if isinstance(msg, dict) else d.get("content")
                    if t == "user" and isinstance(content, str):
                        user_cnt += 1
                        if not first_ts:
                            first_ts = d.get("timestamp", "")
                        if not cwd:
                            cwd = d.get("cwd", "")
                        if "tool_result" not in content[:100]:
                            candidates.append(content)
                    elif t == "user" and isinstance(content, list):
                        for c in content:
                            if isinstance(c, dict) and c.get("type") == "text":
                                candidates.append(c.get("text", ""))
                    elif t not in ("queue-operation",) and not first_ts and d.get("timestamp"):
                        first_ts = d.get("timestamp")
            except Exception:
                pass
            prompt = pick_task(candidates, "", noise)
            if not prompt and not user_cnt:
                continue
            rows.append(task(prompt[:80] or "(自动化/无标题)", prompt, sid, first_ts, cwd,
                             user_cnt, loc, self.name))
        return rows

    def collect_tokens(self):
        rows = []
        for fp, loc in self._files():
            if "/transcripts/" in fp.replace("\\", "/"):
                continue  # transcripts 无 token 字段
            seen_ids = set()
            sid = os.path.splitext(os.path.basename(fp))[0]
            inp = out = cache = reason = 0
            model = tsv = cwd = title = ""
            try:
                for line in open(fp, encoding="utf-8", errors="replace"):
                    try:
                        d = json.loads(line)
                    except Exception:
                        continue
                    if not tsv and d.get("timestamp"):
                        tsv = d["timestamp"]
                    if not cwd and d.get("cwd"):
                        cwd = d["cwd"]
                    msg = d.get("message")
                    if not isinstance(msg, dict) or msg.get("role") != "assistant":
                        continue
                    u = msg.get("usage")
                    if not isinstance(u, dict):
                        continue
                    mid = msg.get("id")
                    if mid and mid in seen_ids:
                        continue
                    if mid:
                        seen_ids.add(mid)
                    inp += u.get("input_tokens", 0) or 0
                    out += u.get("output_tokens", 0) or 0
                    cache += (u.get("cache_creation_input_tokens", 0) or 0) + (u.get("cache_read_input_tokens", 0) or 0)
                    if not model and msg.get("model"):
                        model = msg["model"]
                    if not title:
                        for c in (msg.get("content") or []):
                            if isinstance(c, dict) and c.get("type") == "text" and c.get("text", "").strip():
                                title = c["text"].strip().split("\n")[0][:120]
                                break
            except Exception:
                pass
            if inp or out or cache:
                rows.append(token(sid, title, tsv, cwd, model, inp, out, cache, reason,
                                  source=f"projects/{loc}", agent=self.name))
        return rows
