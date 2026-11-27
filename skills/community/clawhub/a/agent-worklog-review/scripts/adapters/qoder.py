#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Qoder 适配器：*-session.json。"""
import os, json
from .base import BaseAdapter, task, token, all_homes, find_files

QODER_DIRS = [".qoderwork", ".qoderworkcn", ".qoder", ".qoder-cn", ".qoder-cli"]


class QoderAdapter(BaseAdapter):
    name = "Qoder"

    def _files(self):
        roots = [os.path.join(h, d) for h in all_homes() for d in QODER_DIRS]
        seen = set()
        for fp in find_files(roots, "*-session.json"):
            k = os.path.normcase(os.path.abspath(fp))
            if k not in seen:
                seen.add(k)
                yield fp

    def extract_tasks(self):
        rows = []
        seen = set()
        for fp in self._files():
            try:
                d = json.load(open(fp, encoding="utf-8"))
                sid = d.get("id", "")
                if sid in seen:
                    continue
                seen.add(sid)
                rows.append(task(d.get("title", ""), "", sid, d.get("created_at"),
                                 d.get("working_dir", ""), d.get("message_count", ""),
                                 "qoder-session-json", self.name))
            except Exception:
                pass
        return rows

    def collect_tokens(self):
        rows = []
        for fp in self._files():
            try:
                d = json.load(open(fp, encoding="utf-8"))
                inp = d.get("total_prompt_tokens") or d.get("prompt_tokens") or 0
                out = d.get("total_completed_tokens") or d.get("completion_tokens") or 0
                cache = d.get("total_cached_tokens") or 0
                calls = d.get("total_model_call_times") or 0
                sid = d.get("id") or os.path.basename(fp)[:36]
                rows.append(token(sid, d.get("title", ""), d.get("created_at"),
                                  d.get("working_dir", ""), d.get("model", ""),
                                  inp, out, cache,
                                  source="session-json" if (inp or out or cache)
                                  else f"session-json(仅调用次数={calls},无token字段)",
                                  agent=self.name))
            except Exception:
                pass
        return rows
