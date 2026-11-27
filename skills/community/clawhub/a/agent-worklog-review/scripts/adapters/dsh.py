#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dsh 适配器：元数据 session_projcache.json + 压缩正文 *.zstd（流式解压）。"""
import os, json
from .base import BaseAdapter, task, token, all_homes, find_files

try:
    import zstandard as zstd
    HAS_ZSTD = True
except ImportError:
    zstd = None
    HAS_ZSTD = False


class DshAdapter(BaseAdapter):
    name = "dsh"

    def note(self):
        if not HAS_ZSTD:
            return "当前解释器无 zstandard 模块，dsh 压缩会话未统计（用带 zstd 的 Python 重跑）"
        return ""

    def _session_files(self, root):
        """每个会话目录只取最新一代（ccusage 口径）：
        session.jsonl = gen0，session.vN.jsonl[.zstd] = genN；旧版本是同一会话的副本。
        """
        import re
        best = {}
        for fp in find_files([root], "*"):
            name = os.path.basename(fp)
            if not name.startswith("session") or ".jsonl" not in name:
                continue
            m = re.search(r"\.v(\d+)\.jsonl", name)
            gen = int(m.group(1)) if m else 0
            d = os.path.dirname(fp)
            if d not in best or gen > best[d][0]:
                best[d] = (gen, fp)
        return [v[1] for v in best.values()]

    def extract_tasks(self):
        """元数据 projcache + zstd 压缩正文两条路互补：
        元数据给标题/目标，zstd 给真实用户 prompt（34 条真实任务靠它补回）。
        """
        rows = []
        by_sid = {}
        for h in all_homes():
            p = os.path.join(h, ".dsh", "storages", "session_projcache.json")
            if not os.path.isfile(p):
                continue
            try:
                d = json.load(open(p, encoding="utf-8"))
                sessions = d.get("tables", {}).get("sessions", {})
                for k, v in sessions.items():
                    ident = v.get("identity", {})
                    rr = v.get("rows", {})

                    def val(x):
                        return x.get("val") if isinstance(x, dict) and "val" in x else x

                    goal = val(rr.get("goal", {}))
                    objective = ""
                    if isinstance(goal, dict):
                        g2 = val(goal.get("goal", {}))
                        if isinstance(g2, dict):
                            objective = str(val(g2.get("objective", "")) or "")
                    sid = k.replace("session-", "")
                    r = task(clean_title(val(rr.get("title", ""))), objective,
                             sid, ident.get("createdAt"), ident.get("cwd", ""),
                             (val(rr.get("sessionStats", {})) or {}).get("turns", ""),
                             "projcache", self.name)
                    by_sid[sid] = r
                    rows.append(r)
            except Exception as e:
                print(f"  dsh extract: {str(e)[:80]}")
        # zstd 正文：用真实用户 prompt 覆盖/补充元数据
        if HAS_ZSTD:
            for h in all_homes():
                root = os.path.join(h, ".dsh", "sessions")
                if not os.path.isdir(root):
                    continue
                for fp in self._session_files(root):
                    if not fp.endswith(".zstd"):
                        continue
                    sid = os.path.basename(os.path.dirname(fp))
                    prompt, ts0, cwd = self._zstd_prompt(fp)
                    if not prompt:
                        continue
                    if sid in by_sid:
                        by_sid[sid]["prompt"] = clean_title(prompt, 600)
                        if not by_sid[sid]["title"] or by_sid[sid]["title"] == "(无任务描述)":
                            by_sid[sid]["title"] = clean_title(prompt, 80)
                    else:
                        r = task(clean_title(prompt, 80), prompt, sid, ts0, cwd,
                                 "", "zstd", self.name)
                        by_sid[sid] = r
                        rows.append(r)
        return rows

    def _zstd_prompt(self, fp):
        """从单个 zstd 会话提取真实用户任务 (prompt, ts, cwd)。"""
        prompt = ts0 = cwd = ""
        dctx = zstd.ZstdDecompressor()
        try:
            with open(fp, "rb") as f:
                with dctx.stream_reader(f) as reader:
                    raw = reader.read().decode("utf-8", errors="replace")
            for line in raw.splitlines():
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                typ = d.get("type", "")
                data = d.get("data") or {}
                if typ == "session":
                    cwd = cwd or d.get("cwd", "")
                    ts0 = ts0 or str(d.get("createdAt", ""))
                if not ts0 and d.get("time"):
                    ts0 = str(d["time"])
                # dsh 事件流：用户消息在 agent/inbox/spliced 的 data.inserted[].content[].text
                if typ == "agent/inbox/spliced":
                    for item in data.get("inserted", []):
                        if item.get("role") == "user":
                            for c in item.get("content", []):
                                if isinstance(c, dict) and c.get("type") == "text":
                                    t = clean_title(c.get("text", ""))
                                    if t and not t.lower().startswith(("you are", "system", "# agents.md")):
                                        prompt = t
                                    break
                        if prompt:
                            break
                if prompt:
                    break
        except Exception:
            pass
        return prompt, ts0, cwd

    def collect_tokens(self):
        rows = []
        if not HAS_ZSTD:
            return rows
        dctx = zstd.ZstdDecompressor()
        for h in all_homes():
            root = os.path.join(h, ".dsh", "sessions")
            if not os.path.isdir(root):
                continue
            for fp in self._session_files(root):
                if not fp.endswith(".zstd"):
                    continue
                sid = os.path.basename(os.path.dirname(fp))
                inp = out = cache = reason = 0
                model = tsv = cwd = ""
                try:
                    with open(fp, "rb") as f:
                        with dctx.stream_reader(f) as reader:
                            raw = reader.read().decode("utf-8", errors="replace")
                    for line in raw.splitlines():
                        try:
                            d = json.loads(line)
                        except Exception:
                            continue
                        t = d.get("type")
                        data = d.get("data") or {}
                        if d.get("time") and not tsv:
                            tsv = d["time"]
                        if t == "request/header":
                            cfg = ((data.get("header") or {}).get("config") or {})
                            if cfg.get("model") and not model:
                                model = cfg["model"]
                            if data.get("header", {}).get("cwd") and not cwd:
                                cwd = data["header"]["cwd"]
                        if t == "assistant/chunk" and (data.get("chunk") or {}).get("type") == "usage":
                            u = data["chunk"].get("usage") or {}
                            inp += u.get("inputTokens", 0) or 0
                            out += u.get("outputTokens", 0) or 0
                            cache += u.get("cacheReadTokens", 0) or 0
                            reason += u.get("reasoningTokens", 0) or 0
                except Exception:
                    pass
                if inp or out or cache:
                    rows.append(token(sid, "", tsv, cwd, model, inp, out, cache, reason,
                                      source="zstd", agent=self.name))
        return rows


def clean_title(x, limit=200):
    if not isinstance(x, str):
        return ""
    import re
    return re.sub(r"\s+", " ", x).strip()[:limit]
