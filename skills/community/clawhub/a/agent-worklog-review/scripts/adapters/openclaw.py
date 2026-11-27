#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenClaw 适配器（路径与格式来自 ccusage 源码 rust/adapters/openclaw/）。

数据位置（纠正此前只扫 .openclaw 的猜测）：
  ~/.openclaw/、~/.clawdbot/、~/.moltbot/、~/.moldbot/（环境变量 OPENCLAW_DIR 可覆盖）
  - <root>/sessions/**/*.jsonl        会话 transcript（含 .jsonl.deleted.* / .jsonl.reset.* 归档）
  - <root>/agents/<id>/agent/openclaw-agent.sqlite
        表 transcript_events(session_id, seq, event_json, created_at)
  SQLite 优先于同名 JSONL（openclaw doctor --fix 迁移后两者共存）。
  token 字段：message.usage.{input, output, totalTokens}
"""
import os, json, sqlite3
from .base import BaseAdapter, task, token, pick_task, all_homes
from ._jsonutil import open_jsonl

DIR_NAMES = (".openclaw", ".clawdbot", ".moltbot", ".moldbot")


def _roots():
    out = []
    env = os.environ.get("OPENCLAW_DIR", "")
    if env and os.path.isdir(env):
        out.append(env)
    for h in all_homes():
        for n in DIR_NAMES:
            p = os.path.join(h, n)
            if os.path.isdir(p) and p not in out:
                out.append(p)
    return out


def _session_files(root):
    sess = os.path.join(root, "sessions")
    if not os.path.isdir(sess):
        return []
    out = []
    for dp, dns, fns in os.walk(sess):
        dns[:] = [d for d in dns if not d.startswith(".")]
        for fn in fns:
            if ".jsonl" in fn or fn == "sessions.json":
                out.append(os.path.join(dp, fn))
    return out


def _text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for x in content:
            if isinstance(x, dict) and x.get("type") == "text":
                parts.append(str(x.get("text") or ""))
            elif isinstance(x, str):
                parts.append(x)
        return " ".join(parts)
    return str(content or "")


def _msg(obj):
    """统一取 message 对象，兼容 event_json 外层包裹。"""
    if not isinstance(obj, dict):
        return {}
    m = obj.get("message")
    return m if isinstance(m, dict) else obj


class OpenClawAdapter(BaseAdapter):
    name = "OpenClaw"
    verified = False
    token_available = True

    def _events(self):
        """yield (sid, seq, obj, source_path) — SQLite 优先，JSONL 去重后补。"""
        sqlite_keys = set()
        events = []
        for root in _roots():
            # 1) SQLite transcript_events 优先（doctor --fix 迁移后的权威副本）
            for dp, dns, fns in os.walk(os.path.join(root, "agents")):
                dns[:] = [d for d in dns if not d.startswith(".")]
                for fn in fns:
                    if fn != "openclaw-agent.sqlite":
                        continue
                    fp = os.path.join(dp, fn)
                    try:
                        c = sqlite3.connect(f"file:{fp}?mode=ro", uri=True)
                        for sid, seq, ev in c.execute(
                                "select session_id, seq, event_json from transcript_events "
                                "order by session_id, seq"):
                            try:
                                obj = json.loads(ev)
                                if isinstance(obj, dict):
                                    k = (str(sid), int(seq or 0))
                                    sqlite_keys.add(k)
                                    events.append((str(sid), int(seq or 0), obj, fp))
                            except Exception:
                                continue
                        c.close()
                    except Exception as e:
                        print(f"  openclaw: {str(e)[:80]}")
            # 2) JSONL 补充（跳过 SQLite 已覆盖的 sid/seq）
            for fp in _session_files(root):
                sid = os.path.basename(fp).split(".jsonl")[0] or "unknown"
                if fp.endswith("sessions.json"):
                    try:
                        d = json.load(open(fp, encoding="utf-8", errors="replace"))
                        items = d if isinstance(d, list) else list(d.values())
                        for i, obj in enumerate(items):
                            if isinstance(obj, dict) and (sid, i) not in sqlite_keys:
                                events.append((sid, i, obj, fp))
                    except Exception:
                        pass
                    continue
                for i, obj in enumerate(open_jsonl(fp)):
                    if isinstance(obj, dict) and (sid, i) not in sqlite_keys:
                        events.append((sid, i, obj, fp))
        seen = set()
        for e in events:
            k = (e[0], e[1])
            if k in seen:
                continue
            seen.add(k)
            yield e

    def extract_tasks(self):
        rows = []
        for sid, seq, obj, fp in self._events():
            m = _msg(obj)
            role = str(m.get("role") or obj.get("role") or "")
            if role and role != "user":
                continue
            text = _text_of(m.get("content") or obj.get("content") or obj.get("text"))
            t = pick_task([text])
            if not t:
                continue
            rows.append(task(t[:80], t, f"openclaw-{sid}-{seq}",
                             m.get("timestamp") or obj.get("timestamp"), "",
                             seq, "openclaw-transcript", self.name))
        return rows

    def collect_tokens(self):
        out = []
        for sid, seq, obj, fp in self._events():
            m = _msg(obj)
            u = m.get("usage") or obj.get("usage") or {}
            if not isinstance(u, dict):
                continue
            inp = int(u.get("input") or u.get("inputTokens") or 0)
            outp = int(u.get("output") or u.get("outputTokens") or 0)
            total = int(u.get("totalTokens") or 0) or (inp + outp)
            if not (inp or outp):
                continue
            out.append(token(f"openclaw-{sid}-{seq}", "",
                             m.get("timestamp") or obj.get("timestamp"), "",
                             m.get("model") or "", inp, outp, 0, 0,
                             source="openclaw-transcript", total=total,
                             fresh_rule="add", agent=self.name))
        return out

    def note(self):
        return ("按 ccusage 披露的 ~/.openclaw|clawdbot|moltbot|moldbot 会话路径编写，"
                "本机未装 OpenClaw，未用真实会话验证。")
