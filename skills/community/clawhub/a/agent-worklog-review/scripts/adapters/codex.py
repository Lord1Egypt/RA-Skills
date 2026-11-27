#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Codex 适配器：~/.codex/sessions/**/rollout-*.jsonl。"""
import os, json
from .base import BaseAdapter, task, token, pick_task, load_noise_markers, all_homes, find_files, HOME


class CodexAdapter(BaseAdapter):
    name = "Codex"

    def _bases(self):
        out = []
        for h in all_homes():
            for sub in (".codex", ".codex-wsl"):
                b = os.path.join(h, sub, "sessions")
                if os.path.isdir(b):
                    loc = "WSL" if ("wsl.localhost" in b or "wsl$" in b) else "Win"
                    out.append((b, loc))
        return out

    def _index(self):
        idx = {}
        for h in all_homes():
            for sub in (".codex", ".codex-wsl"):
                ip = os.path.join(h, sub, "session_index.jsonl")
                if os.path.isfile(ip):
                    for line in open(ip, encoding="utf-8", errors="replace"):
                        try:
                            d = json.loads(line)
                            idx[d.get("id")] = d
                        except Exception:
                            pass
        return idx

    def _files(self):
        seen = set()
        for base, loc in self._bases():
            for fp in find_files([base], "rollout-*.jsonl",
                                 exclude=("backup", "debug", "archived")):
                k = os.path.normcase(os.path.abspath(fp))
                if k not in seen:
                    seen.add(k)
                    yield fp, loc

    def extract_tasks(self):
        rows = []
        idx = self._index()
        noise = load_noise_markers()
        for fp, loc in self._files():
            sid = first_ts = cwd = ""
            candidates, user_cnt = [], 0
            try:
                with open(fp, encoding="utf-8", errors="replace") as f:
                    for line in f:
                        try:
                            d = json.loads(line)
                        except Exception:
                            continue
                        typ = d.get("type")
                        p = d.get("payload") or {}
                        if typ == "session_meta":
                            sid = p.get("id", "")
                            cwd = p.get("cwd", "")
                            first_ts = p.get("timestamp", "")
                        elif typ == "response_item" and p.get("type") == "message" and p.get("role") == "user":
                            for cc in p.get("content", []):
                                if isinstance(cc, dict) and cc.get("type") in ("input_text", "text"):
                                    if cc.get("text"):
                                        user_cnt += 1
                                        candidates.append(cc["text"])
                        elif typ == "event_msg" and p.get("type") == "user_message":
                            if p.get("message"):
                                user_cnt += 1
                                candidates.append(p["message"])
            except Exception:
                pass
            meta = idx.get(sid, {})
            prompt = pick_task(candidates, meta.get("thread_name", ""), noise)
            rows.append(task(prompt[:80] or "(无任务描述)", prompt,
                             sid or os.path.basename(fp)[8:44], first_ts or meta.get("updated_at"),
                             cwd or meta.get("cwd", ""), user_cnt, f"rollout/{loc}", self.name))
        return rows

    def collect_tokens(self):
        rows = []
        idx = self._index()
        for fp, loc in self._files():
            sid = os.path.basename(fp)[8:44]
            last = None
            tsv = cwd = model = title = ""
            try:
                for line in open(fp, encoding="utf-8", errors="replace"):
                    try:
                        d = json.loads(line)
                    except Exception:
                        continue
                    if not tsv and d.get("timestamp"):
                        tsv = d["timestamp"]
                    p = d.get("payload") or {}
                    if d.get("type") == "session_meta":
                        if p.get("id"):
                            sid = p["id"]
                        cwd = p.get("cwd", "")
                        tsv = tsv or p.get("timestamp", "")
                        model = p.get("model", "") or ""
                        title = (p.get("git") or {}).get("branch", "") or ""
                    elif d.get("type") == "turn_context" and not cwd:
                        cwd = p.get("cwd", "")
                    elif d.get("type") == "event_msg" and p.get("type") == "token_count":
                        info = p.get("info")
                        if isinstance(info, dict) and info.get("total_token_usage"):
                            last = info["total_token_usage"]
                    elif d.get("type") == "event_msg" and p.get("type") == "user_message" and not title:
                        title = (p.get("message") or "")[:120]
            except Exception:
                pass
            meta = idx.get(sid, {})
            title = title or meta.get("thread_name", "")
            cwd = cwd or meta.get("cwd", "")
            if not last:
                continue
            rows.append(token(sid, title, tsv, cwd, model,
                              inp=last.get("input_tokens", 0), out=last.get("output_tokens", 0),
                              cache=last.get("cached_input_tokens", 0),
                              reason=last.get("reasoning_output_tokens", 0),
                              total=last.get("total_tokens"),
                              fresh_rule="subtract", source=f"rollout/{loc}", agent=self.name))
        return rows
