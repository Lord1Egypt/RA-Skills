#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VS Code 系 IDE 适配器：Cursor / Trae / CodeBuddy / Windsurf / MarsCode。

对话存在 state.vscdb（SQLite）。已验证的 Cursor 结构：
  - 表 cursorDiskKV，key = composerData:<uuid>，value 为 JSON：
      {composerId, createdAt, conversation: [ {type:1(用户)/2(AI), text, tokenDetailsUpUntilHere}, ... ]}
  - 表 ItemTable 为 UI 状态，无对话。
其他 IDE 用启发式扫描 value 找含 user 消息的 JSON 作为兜底。
token 大多不暴露（tokenDetails 常为空），如实标注。
"""
import os, json, sqlite3
from .base import BaseAdapter, task, all_homes, appdata_roots

VSCDB_HINTS = {
    "Cursor": ["Cursor/User/globalStorage/state.vscdb",
               "Cursor/User/workspaceStorage/*/state.vscdb",
               ".cursor/state.vscdb"],
    "Trae": ["Trae/User/globalStorage/state.vscdb",
             "Trae CN/User/globalStorage/state.vscdb",
             ".trae/state.vscdb"],
    "CodeBuddy": ["CodeBuddy/User/globalStorage/state.vscdb",
                  "CodeBuddy CN/User/globalStorage/state.vscdb",
                  ".codebuddy/state.vscdb"],
    "Windsurf": ["Windsurf/User/globalStorage/state.vscdb", ".windsurf/state.vscdb"],
    "MarsCode": ["MarsCode/User/globalStorage/state.vscdb", ".marscode/state.vscdb"],
}


class VscdbAdapter(BaseAdapter):
    name = "Cursor/Trae/CodeBuddy"
    token_available = False
    token_note = "state.vscdb 的 tokenDetails 字段大多为空，无法可靠统计 token"

    def _db_paths(self):
        roots = all_homes() + appdata_roots()
        seen = set()
        for agent, hints in VSCDB_HINTS.items():
            for root in roots:
                for hint in hints:
                    parts = hint.split("/")
                    if "*" in parts:
                        idx = parts.index("*")
                        base = os.path.join(root, *parts[:idx]); rest = parts[idx + 1:]
                        if not os.path.isdir(base):
                            continue
                        try:
                            for entry in os.listdir(base):
                                fp = os.path.join(base, entry, *rest)
                                if os.path.isfile(fp):
                                    k = os.path.normcase(os.path.abspath(fp))
                                    if k not in seen:
                                        seen.add(k); yield agent, fp
                        except OSError:
                            pass
                    else:
                        fp = os.path.join(root, *parts)
                        if os.path.isfile(fp):
                            k = os.path.normcase(os.path.abspath(fp))
                            if k not in seen:
                                seen.add(k); yield agent, fp

    def extract_tasks(self):
        rows = []
        seen_prompt = set()
        for agent, db in self._db_paths():
            try:
                c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
                tables = [r[0] for r in c.execute("select name from sqlite_master where type='table'")]
                # 1) Cursor 已验证结构：cursorDiskKV.composerData:*
                if "cursorDiskKV" in tables:
                    for key, val in c.execute("select key,value from cursorDiskKV where key like 'composerData:%'"):
                        try:
                            d = json.loads(val)
                        except Exception:
                            continue
                        conv = d.get("conversation") or []
                        user_texts = []
                        for it in conv:
                            if isinstance(it, dict) and it.get("type") == 1 and it.get("text"):
                                user_texts.append(str(it["text"]).strip())
                        prompt = user_texts[0] if user_texts else ""
                        if not prompt:
                            continue
                        k = agent + "|" + prompt[:100]
                        if k in seen_prompt:
                            continue
                        seen_prompt.add(k)
                        sid = d.get("composerId") or key.split(":", 1)[-1]
                        rows.append(task(prompt[:80], prompt, sid, d.get("createdAt"),
                                         "", len(user_texts), "vscdb/cursorDiskKV", agent))
                # 2) 通用兜底：扫描其他表的 JSON value 找对话
                for table in tables:
                    if table == "cursorDiskKV":
                        continue
                    try:
                        cur = c.execute(f'select * from "{table}" limit 3000')
                        colnames = [x[0] for x in cur.description]
                        for row in cur:
                            for i, val in enumerate(row):
                                if not isinstance(val, str) or not val.strip().startswith(("{", "[")):
                                    continue
                                try:
                                    obj = json.loads(val)
                                except Exception:
                                    continue
                                prompt = self._find_user_text(obj)
                                if not prompt:
                                    continue
                                k = agent + "|" + prompt[:100]
                                if k in seen_prompt:
                                    continue
                                seen_prompt.add(k)
                                rows.append(task(prompt[:80], prompt,
                                                 os.path.basename(db) + ":" + str(colnames[i]),
                                                 "", os.path.dirname(db), "",
                                                 f"vscdb/{table}", agent))
                    except Exception:
                        continue
                c.close()
            except Exception as e:
                print(f"  vscdb {agent}: {str(e)[:80]}")
        return rows

    def _find_user_text(self, obj, depth=0):
        if depth > 5:
            return ""
        if isinstance(obj, dict):
            role = str(obj.get("role", obj.get("author", obj.get("sender", "")))).lower()
            text = obj.get("content", obj.get("text", obj.get("message", "")))
            if role in ("user", "human", "me") and isinstance(text, str) and text.strip():
                return text.strip()
            for v in obj.values():
                r = self._find_user_text(v, depth + 1)
                if r:
                    return r
        elif isinstance(obj, list):
            for v in obj[:50]:
                r = self._find_user_text(v, depth + 1)
                if r:
                    return r
        return ""
