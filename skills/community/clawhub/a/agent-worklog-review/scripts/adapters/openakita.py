#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenAkita 适配器：.openakita/workspaces/*/data/memory/conversation_history/*.jsonl。"""
import os, json
from .base import BaseAdapter, task, all_homes, find_files


class OpenAkitaAdapter(BaseAdapter):
    name = "OpenAkita"
    token_available = False
    token_note = "OpenAkita 会话文件不含 token 用量字段"

    def extract_tasks(self):
        rows = []
        for h in all_homes():
            base = os.path.join(h, ".openakita", "workspaces")
            if not os.path.isdir(base):
                continue
            for fp in find_files([base], "conversation_history/*.jsonl"):
                prompt = ts0 = ""
                try:
                    for line in open(fp, encoding="utf-8", errors="replace"):
                        try:
                            d = json.loads(line)
                        except Exception:
                            continue
                        if d.get("role") == "user" and not prompt:
                            prompt = (d.get("content", "") or "")[:400]
                            ts0 = d.get("timestamp", "")
                except Exception:
                    pass
                if prompt:
                    rows.append(task(prompt[:60], prompt, os.path.basename(fp), ts0, "", "",
                                     "conversation_history", self.name))
        return rows
