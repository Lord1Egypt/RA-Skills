#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kimi Code CLI 适配器。

支持以下两种会话布局：
1) context.jsonl      每行 {"role":"user"|"assistant"|..., "content":...}
   user-history/*.jsonl 每行 {"content":...}（无 role，纯用户输入）
2) wire.jsonl（公开的会话布局）
   - 用户消息：{"message":{"type":"TurnBegin",
                 "payload":{"user_input":[{"type":"text","text":"..."}]}}}
   - token：{"message":{"type":"StatusUpdate",
              "payload":{"token_usage":{"input_other":...,"output":...,
                         "input_cache_read":...,"input_cache_creation":...},
                         "message_id":"..."}}}

此前误判「Kimi 不含 token」——token 在 wire.jsonl 而非 context.jsonl，已修正。
"""
import os
from .base import BaseAdapter, task, token, pick_task, all_homes
from ._jsonutil import open_jsonl, expand_dirs

DIR_PATTERNS = (
    ".kimi/sessions/*/*", ".kimi/sessions/*/*/agents/*",
    ".kimi/user-history",
    ".kimi-code/sessions/*/*", ".kimi-code/sessions/*/*/agents/*",
    ".kimi-code/user-history",
)


class KimiAdapter(BaseAdapter):
    name = "Kimi Code"
    token_available = True
    verified = True

    def _files(self):
        dirs = expand_dirs(all_homes(), DIR_PATTERNS)
        seen, out = set(), []
        import glob
        for d in dirs:
            for g in ("context.jsonl", "wire.jsonl", "*.jsonl"):
                for fp in glob.glob(os.path.join(d, g)):
                    k = os.path.normcase(os.path.abspath(fp))
                    if k not in seen and os.path.isfile(fp):
                        seen.add(k)
                        out.append(fp)
        return out

    def extract_tasks(self):
        rows = []
        for fp in self._files():
            cnt = 0
            for i, obj in enumerate(open_jsonl(fp)):
                if not isinstance(obj, dict):
                    continue
                sid = f"kimi-{os.path.basename(os.path.dirname(fp))}-{i}"
                text = ""
                ts0 = obj.get("timestamp", "")
                # wire.jsonl: TurnBegin.payload.user_input[]
                msg = obj.get("message") if isinstance(obj.get("message"), dict) else {}
                if msg.get("type") == "TurnBegin":
                    for part in (msg.get("payload") or {}).get("user_input") or []:
                        if isinstance(part, dict) and part.get("type") == "text":
                            text = str(part.get("text") or "")
                            break
                else:
                    role = str(obj.get("role", ""))
                    is_user = role == "user"
                    is_history = (role == "" and "content" in obj)
                    if is_user or is_history:
                        text = str(obj.get("content") or "")
                text = text.strip()
                if len(text) < 3 or text.startswith("/"):
                    continue
                t = pick_task([text])
                if not t:
                    continue
                cnt += 1
                rows.append(task(t[:80], t, sid, ts0, "", cnt,
                                 "kimi-wire" if os.path.basename(fp) == "wire.jsonl" else "kimi-jsonl",
                                 self.name))
        return rows

    def collect_tokens(self):
        """StatusUpdate 是会话累计快照（同会话多条递增），每会话只取最后一条，
        否则逐条累加会把同一份用量计 20 次。"""
        rows = []
        for fp in self._files():
            if os.path.basename(fp) != "wire.jsonl":
                continue
            last = None
            for i, obj in enumerate(open_jsonl(fp)):
                msg = obj.get("message") if isinstance(obj, dict) else None
                if not isinstance(msg, dict) or msg.get("type") != "StatusUpdate":
                    continue
                payload = msg.get("payload") or {}
                u = payload.get("token_usage") or {}
                if not isinstance(u, dict):
                    continue
                other = int(u.get("input_other") or 0)
                cr = int(u.get("input_cache_read") or 0)
                cw = int(u.get("input_cache_creation") or 0)
                outp = int(u.get("output") or 0)
                inp = other + cr + cw
                if not (inp or outp):
                    continue
                last = {
                    "mid": str(payload.get("message_id") or
                               f"{os.path.basename(os.path.dirname(fp))}-{i}"),
                    "ts": obj.get("timestamp", ""), "inp": inp, "out": outp,
                    "cache": cr + cw,
                }
            if last:
                rows.append(token(last["mid"], "", last["ts"], "", "",
                                  last["inp"], last["out"], last["cache"], 0,
                                  source="kimi-wire", total=last["inp"] + last["out"],
                                  fresh_rule="subtract", agent=self.name))
        return rows
