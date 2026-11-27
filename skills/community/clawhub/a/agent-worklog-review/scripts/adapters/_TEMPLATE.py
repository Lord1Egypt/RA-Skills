#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""适配器模板：复制本文件为 <agent名>.py 即可接入新 Agent。

只需：
1. 改类名和 name
2. 实现 extract_tasks()：返回 task(...) 记录列表
3. 实现 collect_tokens()：返回 token(...) 记录列表（拿不到 token 就返回 [] 并设 token_available=False）
4. 用 all_homes() / appdata_roots() / find_files(roots, "*.jsonl") 找文件，勿写死用户名和路径

save 后无需改任何核心脚本，run_all.py 会自动发现。
"""
import os, json
from .base import BaseAdapter, task, token, all_homes, appdata_roots, find_files


class MyAgentAdapter(BaseAdapter):
    name = "MyAgent"                 # 报告里显示的名字
    token_available = False          # 该 Agent 是否暴露 token
    token_note = "该 Agent 的会话不含 token 字段"

    def extract_tasks(self):
        rows = []
        for h in all_homes():
            base = os.path.join(h, ".myagent", "sessions")
            for fp in find_files([base], "*.jsonl"):
                try:
                    d = json.load(open(fp, encoding="utf-8"))
                except Exception:
                    continue
                prompt = d.get("prompt", "")
                if not prompt:
                    continue
                rows.append(task(prompt[:80], prompt, d.get("id", ""),
                                 d.get("created_at", ""), d.get("cwd", ""),
                                 "", "myagent-jsonl", self.name))
        return rows

    def collect_tokens(self):
        rows = []
        # 若该 Agent 暴露 token，示例：
        # for fp in self._files():
        #     d = json.load(...)
        #     rows.append(token(sid, title, ts, cwd, model, inp, out, cache,
        #                       fresh_rule="subtract",  # cached 已含在 input 时用 subtract
        #                       source="myagent-jsonl", agent=self.name))
        return rows
