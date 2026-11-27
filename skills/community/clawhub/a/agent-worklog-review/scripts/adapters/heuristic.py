#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L3 启发式兜底适配器。

对"扫描到了但 L1 专用适配器 / L2 声明式规则都没覆盖"的 Agent，
取其扫描报告里的 session_files，用通用 JSONL/JSON/MD 解析提取用户消息，
保证不再出现"扫到了却是 0 任务且无提示"。

特点：
- 只处理未覆盖的 agent，不与现有适配器重复统计。
- 提取结果标注 source="heuristic"，报告会提示人工核验。
- 限制每 agent 文件数 / 每文件行数，避免大文件卡死。
- token 一律不提取（启发式无法保证口径），如实标注。
"""
import os, json
from .base import BaseAdapter, task, pick_task, ROOT
from ._jsonutil import (ROLE_KEYS, USER_VALUES, TEXT_KEYS,
                        open_jsonl, open_json, is_user, message_text)

MAX_FILES_PER_AGENT = 60
MAX_RECORDS_PER_FILE = 300

# 扫描报告里的 agent 名 → 适配器名 的别名（与 classify_tasks 保持一致）
ALIAS = {
    "Claude Code": "claudecode", "OpenAI Codex": "codex", "DeepSeek": "dsh",
    "Trae": "cursortraecodebuddy", "CodeBuddy": "cursortraecodebuddy",
    "Cursor": "cursortraecodebuddy", "Windsurf": "cursortraecodebuddy",
    "MarsCode": "cursortraecodebuddy", "Kimi": "kimicode",
}


def _norm(s):
    s = ALIAS.get(s, s)
    return s.replace(" ", "").replace("/", "").replace("_", "").lower()


class HeuristicAdapter(BaseAdapter):
    name = "HeuristicFallback"
    token_available = False
    token_note = "启发式兜底不提取 token（无法保证口径）；若需 token 请为该 Agent 写专用适配器"
    verified = False

    def _scan_report(self):
        p = os.path.join(ROOT, "output", "agent_scan_report.json")
        try:
            return json.load(open(p, encoding="utf-8")).get("agents", {})
        except Exception:
            return {}

    def _covered(self):
        """已被其他适配器覆盖的 agent 归一化名集合。延迟 discover 避免循环导入。"""
        try:
            from .base import discover
            names = set()
            for a in discover():
                if a.name == self.name:
                    continue
                names.add(_norm(a.name))
                # 拆分别名：'Cursor/Trae/CodeBuddy' 拆成多个
                for part in a.name.replace("/", ",").split(","):
                    names.add(_norm(part.strip()))
            return names
        except Exception:
            return set()

    def _records(self, fp):
        ext = os.path.splitext(fp)[1].lower()
        if ext == ".jsonl":
            return open_jsonl(fp, limit=MAX_RECORDS_PER_FILE)
        if ext == ".json":
            d = open_json(fp)
            if isinstance(d, list):
                return d[:MAX_RECORDS_PER_FILE]
            if isinstance(d, dict):
                # 展开常见消息数组
                for k in ("messages", "conversation", "history", "turns", "events"):
                    if isinstance(d.get(k), list):
                        return d[k][:MAX_RECORDS_PER_FILE]
                return [d]
        if ext == ".md":
            try:
                return [{"content": line.strip(), "role": "user"}
                        for line in open(fp, encoding="utf-8", errors="replace")
                        if line.strip().startswith(("####", "USER", "> "))][:MAX_RECORDS_PER_FILE]
            except Exception:
                return []
        return []

    def extract_tasks(self):
        report = self._scan_report()
        if not report:
            return []
        covered = self._covered()
        rows = []
        for agent, entry in report.items():
            if _norm(agent) in covered:
                continue  # 已有专用/声明式适配器，避免重复
            files = (entry.get("session_files") or [])
            files = sorted(files, key=lambda x: -(x.get("size_kb") or 0))[:MAX_FILES_PER_AGENT]
            cnt = 0
            for f in files:
                fp = f.get("path") if isinstance(f, dict) else str(f)
                if not fp or not os.path.isfile(fp):
                    continue
                for i, obj in enumerate(self._records(fp)):
                    if isinstance(obj, dict):
                        role = str(obj.get("role", ""))
                        # 有 role 但非用户 → 跳过；无 role 则尝试按内容判断
                        if role and not is_user(obj, ROLE_KEYS, USER_VALUES):
                            continue
                        v = message_text(obj, TEXT_KEYS)
                    else:
                        v = str(obj)
                    v = (v or "").strip()
                    if len(v) < 4 or v.startswith(("<", "/", "#")):
                        continue
                    t = pick_task([v], fallback=v[:120])
                    if not t:
                        continue
                    cnt += 1
                    rows.append(task(t[:80], t, f"heuristic-{_norm(agent)}-{os.path.basename(fp)}-{i}",
                                     "", os.path.dirname(fp), cnt, "heuristic", agent))
        return rows
