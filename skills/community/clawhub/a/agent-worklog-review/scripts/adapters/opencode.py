#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""opencode 适配器：~/.local/share/opencode/storage/*/**/*.json。

opencode 的 session/message/part 分目录存 JSON；用目录启发式提取，
不强依赖具体版本 schema。token 若有则取，无则标注。
"""
import os, json
from .base import BaseAdapter, task, token, all_homes, find_files


class OpencodeAdapter(BaseAdapter):
    name = "opencode"

    def _files(self):
        roots = []
        for h in all_homes():
            for rel in (".local/share/opencode/storage", ".opencode/storage",
                        "AppData/Local/opencode/storage"):
                p = os.path.join(h, *rel.split("/"))
                if os.path.isdir(p):
                    roots.append(p)
        seen = set()
        for fp in find_files(roots, "*.json"):
            k = os.path.normcase(os.path.abspath(fp))
            if k not in seen:
                seen.add(k)
                yield fp

    def _user_text(self, obj):
        role = str(obj.get("role", "")).lower()
        if role != "user":
            return ""
        parts = obj.get("parts") or []
        texts = []
        for p in parts:
            if isinstance(p, dict) and p.get("type") == "text":
                texts.append(p.get("text", ""))
        return " ".join(t for t in texts if isinstance(t, str)).strip()

    def extract_tasks(self):
        rows = []
        for fp in self._files():
            rel = fp.replace("\\", "/").lower()
            if "/message/" not in rel and "/messages/" not in rel:
                continue  # 只从消息文件提取，避免 session 元数据重复
            try:
                d = json.load(open(fp, encoding="utf-8"))
            except Exception:
                continue
            prompt = self._user_text(d)
            if not prompt:
                continue
            sid = d.get("sessionID") or os.path.basename(os.path.dirname(os.path.dirname(fp)))
            rows.append(task(prompt[:80], prompt, sid,
                             d.get("time", {}).get("created") if isinstance(d.get("time"), dict) else d.get("created_at"),
                             "", "", "opencode-storage", self.name))
        return rows

    def collect_tokens(self):
        rows = []
        for fp in self._files():
            rel = fp.replace("\\", "/").lower()
            if "/message/" not in rel and "/assistant/" not in rel:
                continue
            try:
                d = json.load(open(fp, encoding="utf-8"))
            except Exception:
                continue
            u = d.get("tokens") or d.get("usage") or {}
            if not isinstance(u, dict):
                continue
            inp = u.get("input", u.get("input_tokens", 0)) or 0
            out = u.get("output", u.get("output_tokens", 0)) or 0
            cache = u.get("cache", {}).get("read", 0) if isinstance(u.get("cache"), dict) else (u.get("cached_input_tokens", 0) or 0)
            reason = u.get("reasoning", u.get("reasoning_tokens", 0)) or 0
            if not (inp or out or cache):
                continue
            sid = d.get("sessionID") or os.path.basename(os.path.dirname(os.path.dirname(fp)))
            rows.append(token(sid, "", "", "", d.get("modelID") or d.get("model", ""),
                              inp, out, cache, reason,
                              fresh_rule="subtract", source="opencode-storage", agent=self.name))
        return rows
