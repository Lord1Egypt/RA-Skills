#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hermes Agent（NousResearch）适配器。

路径与表结构来自 ccusage 源码 rust/adapters/hermes/（同时纠正了此前猜测的
~/.hermes/sessions/* 目录——实际是一个 SQLite 库）：
  ~/.hermes/state.db   （环境变量 HERMES_HOME 可覆盖）
  表 sessions: id, source, model, started_at, message_count,
               input_tokens, output_tokens, cache_read_tokens,
               cache_write_tokens, reasoning_tokens,
               estimated_cost_usd, actual_cost_usd

本机未安装，未用真实会话验证；路径与字段名来自权威实现。
"""
import os, sqlite3
from .base import BaseAdapter, token, all_homes


class HermesAdapter(BaseAdapter):
    name = "Hermes"
    verified = False
    token_available = True

    def _db_paths(self):
        out = []
        env = os.environ.get("HERMES_HOME", "")
        if env and os.path.isfile(os.path.join(env, "state.db")):
            out.append(os.path.join(env, "state.db"))
        for h in all_homes():
            p = os.path.join(h, ".hermes", "state.db")
            if os.path.isfile(p) and p not in out:
                out.append(p)
        return out

    def collect_tokens(self):
        out = []
        for fp in self._db_paths():
            try:
                c = sqlite3.connect(f"file:{fp}?mode=ro", uri=True)
                cols = {r[1] for r in c.execute("pragma table_info(sessions)")}
                if not cols:
                    c.close()
                    continue

                def col(name):
                    return name if name in cols else "NULL"

                sel = ", ".join([col(x) for x in (
                    "id", "model", "started_at", "input_tokens", "output_tokens",
                    "cache_read_tokens", "cache_write_tokens", "reasoning_tokens")])
                where = (" AND model IS NOT NULL AND TRIM(model) != ''"
                         if "model" in cols else "")
                for r in c.execute(f"SELECT {sel} FROM sessions WHERE 1=1{where}"):
                    try:
                        inp, outp = int(r[3] or 0), int(r[4] or 0)
                        cache = int(r[5] or 0) + int(r[6] or 0)
                        reason = int(r[7] or 0)
                        if not (inp or outp or cache or reason):
                            continue
                        out.append(token(str(r[0] or ""), "", r[2], "", r[1] or "",
                                         inp, outp, cache, reason,
                                         source="hermes-sqlite", fresh_rule="add",
                                         agent=self.name))
                    except Exception:
                        continue
                c.close()
            except Exception as e:
                print(f"  hermes: {str(e)[:80]}")
        return out

    def note(self):
        return ("按 ccusage 披露的 ~/.hermes/state.db → sessions 表编写，"
                "本机未装 Hermes，未用真实会话验证；表内无用户 prompt，任务提取为空属正常。")

    def extract_tasks(self):
        return []
