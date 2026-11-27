#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WorkBuddy 适配器：~/.workbuddy/workbuddy.db 的 sessions / session_usage 表。"""
import os, sqlite3
from .base import BaseAdapter, task, token, all_homes


class WorkBuddyAdapter(BaseAdapter):
    name = "WorkBuddy"

    def _db_paths(self):
        seen = set()
        for h in all_homes():
            p = os.path.join(h, ".workbuddy", "workbuddy.db")
            if os.path.isfile(p) and os.path.normcase(p) not in seen:
                seen.add(os.path.normcase(p))
                yield p

    def extract_tasks(self):
        rows = []
        for p in self._db_paths():
            try:
                c = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
                c.row_factory = sqlite3.Row
                cols = [r[1] for r in c.execute("pragma table_info(sessions)")]
                sel = "select id,title,created_at from sessions"
                if "cwd" in cols:
                    sel = sel.replace("created_at", "created_at,cwd")
                for r in c.execute(sel):
                    rows.append(task(r["title"] or "", "", r["id"], r["created_at"],
                                     (r["cwd"] if "cwd" in r.keys() else "") or "",
                                     "", "db.sessions", self.name))
                c.close()
            except Exception as e:
                print(f"  WorkBuddy extract: {str(e)[:80]}")
        return rows

    def collect_tokens(self):
        rows = []
        for p in self._db_paths():
            try:
                c = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
                try:
                    cols = [r[1] for r in c.execute("pragma table_info(session_usage)")]
                except Exception:
                    c.close()
                    continue
                if "used" not in cols:
                    c.close()
                    continue
                meta = {}
                try:
                    for r in c.execute("select id,title,cwd,created_at,model from sessions"):
                        meta[r[0]] = r
                except Exception:
                    pass
                for sid, used, size, updated, credit in c.execute(
                        "select session_id,used,size,updated_at,credit_json from session_usage"):
                    m = meta.get(sid, ("", "", "", "", ""))
                    rows.append(token(sid, m[1], m[3] or updated, m[2], m[4],
                                      inp=used, source=f"session_usage(size={size})",
                                      agent=self.name))
                c.close()
            except Exception as e:
                print(f"  WorkBuddy token: {str(e)[:80]}")
        return rows
