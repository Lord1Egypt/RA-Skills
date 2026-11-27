#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ZCode（智谱 z.ai）适配器。

路径与表结构来自 ccusage 源码 rust/adapters/zcode/（ZCode 0.16.3）：
  ~/.zcode/cli/db/db.sqlite
  表 model_usage: id, session_id, started_at, model_id, input_tokens, output_tokens,
                  [cache_creation_input_tokens], [cache_read_input_tokens],
                  [computed_total_tokens], [provider_id], status
  表 session:     id, directory, [version]
  SELECT ... FROM model_usage m LEFT JOIN session s ON s.id = m.session_id
         WHERE m.status = 'completed'

本机未安装 ZCode，未用真实会话验证；但路径与字段名不再是猜测。
token 可统计；用户 prompt 不在该库中，任务提取返回空（诚实标注）。
"""
import os, sqlite3
from .base import BaseAdapter, token, all_homes


class ZCodeAdapter(BaseAdapter):
    name = "ZCode"
    verified = False
    token_available = True

    def _db_paths(self):
        out = []
        for h in all_homes():
            p = os.path.join(h, ".zcode", "cli", "db", "db.sqlite")
            if os.path.isfile(p):
                out.append(p)
        return out

    def _usage_rows(self):
        rows = []
        for fp in self._db_paths():
            try:
                c = sqlite3.connect(f"file:{fp}?mode=ro", uri=True)
                cols_mu = {r[1] for r in c.execute("pragma table_info(model_usage)")}
                cols_s = {r[1] for r in c.execute("pragma table_info(session)")}
                if not cols_mu:
                    c.close()
                    continue

                def col(name):
                    return f"m.{name}" if name in cols_mu else "NULL"

                def scol(name):
                    return f"s.{name}" if name in cols_s else "NULL"

                sel = ", ".join([
                    col("session_id"), col("started_at"), col("model_id"),
                    col("input_tokens"), col("output_tokens"),
                    col("cache_creation_input_tokens"), col("cache_read_input_tokens"),
                    col("computed_total_tokens"), scol("directory"),
                ])
                where = " AND m.status = 'completed'" if "status" in cols_mu else ""
                sql = (f"SELECT {sel} FROM model_usage m "
                       f"LEFT JOIN session s ON s.id = m.session_id WHERE 1=1{where}")
                for r in c.execute(sql):
                    rows.append((fp, r))
                c.close()
            except Exception as e:
                print(f"  zcode: {str(e)[:80]}")
        return rows

    def collect_tokens(self):
        out = []
        for fp, r in self._usage_rows():
            sid = str(r[0] or "")
            try:
                inp = int(r[3] or 0)
                outp = int(r[4] or 0)
                cw = int(r[5] or 0)
                cr = int(r[6] or 0)
                cache = cw + cr
                total = int(r[7] or 0) or (inp + outp + cache)
                if not (inp or outp or cache or total):
                    continue
                out.append(token(sid, "", r[1], r[8] or "", r[2] or "",
                                 inp, outp, cache, 0, source="zcode-sqlite",
                                 total=total, fresh_rule="add", agent=self.name))
            except Exception:
                continue
        return out

    def note(self):
        return ("按 ccusage 披露的 ~/.zcode/cli/db/db.sqlite 编写，本机未装 ZCode，"
                "未用真实会话验证；用户 prompt 不在库中，任务提取为空属正常。")

    def extract_tasks(self):
        return []
