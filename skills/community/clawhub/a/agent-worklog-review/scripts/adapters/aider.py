#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aider 适配器：~/.aider.chat.history.md（Markdown 对话历史）。

注意：Aider 历史文件散落在项目目录，但不能全 home 无限递归（会扫到
node_modules / WSL UNC 导致卡死）。限制深度 3 + 跳过噪声目录。
"""
import os, re
from .base import BaseAdapter, task, all_homes

SKIP = {"node_modules", ".git", "AppData", "Library", "venv", ".venv",
        "site-packages", "dist", "build", "__pycache__", ".cache"}


class AiderAdapter(BaseAdapter):
    name = "Aider"
    token_available = False
    token_note = "Aider 的 .aider.chat.history.md 不含 token 用量字段"

    def _find_histories(self):
        seen = set()
        for h in all_homes():
            # home 顶层
            for name in (".aider.chat.history.md",):
                fp = os.path.join(h, name)
                if os.path.isfile(fp):
                    k = os.path.normcase(fp)
                    if k not in seen:
                        seen.add(k)
                        yield fp
            # 有限深度子目录
            try:
                base_depth = h.rstrip("\\/").count(os.sep)
                for dp, dns, fns in os.walk(h, topdown=True, onerror=lambda e: None):
                    dns[:] = [d for d in dns if d not in SKIP and not d.startswith(".")]
                    if dp.count(os.sep) - base_depth >= 3:
                        dns[:] = []
                    for fn in (".aider.chat.history.md",):
                        if fn in fns:
                            fp = os.path.join(dp, fn)
                            k = os.path.normcase(fp)
                            if k not in seen:
                                seen.add(k)
                                yield fp
            except Exception:
                pass

    def extract_tasks(self):
        rows = []
        for fp in self._find_histories():
            try:
                text = open(fp, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            # Aider 历史里用户消息通常以 "####" 标题或 "USER" / "> " 开头
            parts = re.split(r"(?m)^#{2,4}\s+|(?m)^USER\s*:?\s*|(?m)^>\s+", text)
            cnt = 0
            for part in parts:
                part = part.strip()
                if not part or len(part) < 8 or part.startswith("#"):
                    continue
                if part.lower().startswith(("aider", "model", "added", "tokens", "token")):
                    continue
                prompt = re.sub(r"\s+", " ", part)[:400]
                cnt += 1
                rows.append(task(prompt[:80], prompt, f"aider-{os.path.basename(fp)}-{cnt}",
                                 "", os.path.dirname(fp), cnt, "chat-history", self.name))
        return rows
