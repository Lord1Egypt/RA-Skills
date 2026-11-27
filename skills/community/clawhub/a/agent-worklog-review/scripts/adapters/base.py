#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""适配器公共基类与工具函数。

设计要点：
1. 每个 Agent 一个适配器文件，放在 scripts/adapters/ 下，类名任意，
   只要继承 BaseAdapter 并声明 name / extract_tasks / collect_tokens 即可被自动发现。
2. 适配器只负责「把自己的会话格式翻译成统一记录」，不做分类、不做报告。
3. token 拿不到就返回空列表，并在 note() 中说明原因，报告会如实展示，绝不伪造。
"""
import os, sys, json, re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import clean, ts, find_files, all_homes, appdata_roots, under, IS_WIN, HOME

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_DIR = os.path.join(ROOT, "config")

# 通用系统注入标记（跨 agent 通用，不含任何个人/项目私有样本）
DEFAULT_NOISE_MARKERS = [
    "<environment_context>", "<recommended_plugins>", "<permissions instructions>",
    "# AGENTS.md instructions", "<INSTRUCTIONS>", "<system-reminder",
    "You are Claude Code", "You are completing a recurring task",
    "The following is the Codex agent history", "Use the workspace files to solve the task",
    "You are mining a user's past AI-assistant sessions", "<ultrawork-mode>",
]
# 本机特有的误判样本不写死在代码里，放 config/noise_filters.local.json（分发包不含）


def load_noise_markers():
    """加载噪音过滤词：内置通用 + 可选本地配置。"""
    markers = list(DEFAULT_NOISE_MARKERS)
    candidates = [
        os.environ.get("WORKLOG_NOISE_FILTERS", ""),
        os.path.join(CONFIG_DIR, "noise_filters.json"),
        os.path.join(CONFIG_DIR, "local", "noise_filters.local.json"),
    ]
    for p in candidates:
        if not p or not os.path.isfile(p):
            continue
        try:
            d = json.load(open(p, encoding="utf-8"))
            for m in (d.get("markers") or []):
                if isinstance(m, str) and m:
                    markers.append(m)
        except Exception:
            pass
    return list(dict.fromkeys(markers))


def task(title, prompt, sid, tsv, cwd, turns, source, agent=None):
    """构造统一任务记录。"""
    return {
        "agent": agent or "", "session_id": str(sid or ""),
        "title": clean(title or "", 200), "prompt": clean(prompt or "", 600),
        "timestamp": ts(tsv), "cwd": str(cwd or ""), "turns": turns,
        "source": source,
    }


def token(sid, title, tsv, cwd, model, inp=0, out=0, cache=0, reason=0,
          source="", total=None, fresh_rule="add", agent=None):
    """构造统一 token 记录。

    fresh_rule:
      - "add"    : 非缓存 = input + output（缓存字段另计，不与 input 重叠）
      - "subtract": 非缓存 = (input - cached) + output（缓存已含在 input 内）
    """
    inp, out, cache = int(inp or 0), int(out or 0), int(cache or 0)
    total = int(total) if total is not None else inp + out + cache
    fresh = max(0, inp - cache) + out if fresh_rule == "subtract" else inp + out
    return {
        "agent": agent or "", "session_id": str(sid or ""),
        "title": clean(title or "", 120), "timestamp": str(tsv or ""),
        "cwd": str(cwd or ""), "model": model or "",
        "input_tokens": inp, "output_tokens": out, "cache_tokens": cache,
        "reasoning_tokens": int(reason or 0), "total_tokens": total,
        "fresh_tokens": fresh, "source": source,
    }


def pick_task(candidates, fallback="", noise=None):
    """从用户消息候选中挑一条有效任务描述。"""
    noise = noise if noise is not None else load_noise_markers()
    for c in candidates:
        s = clean(c, 300)
        if not s or len(s) < 4:
            continue
        low = s.lower()
        if any(m.lower() in low for m in noise):
            continue
        if s.startswith(("for C:\\", "for D:\\", "<", "# ")):
            continue
        return s
    fb = clean(fallback, 200)
    if fb and len(fb) >= 4 and not any(m.lower() in fb.lower() for m in noise):
        return fb
    return ""


class BaseAdapter:
    """所有适配器的基类。子类按需覆盖 extract_tasks / collect_tokens。"""
    name = "Unnamed"
    # 该 agent 的 token 数据是否可由本机记录统计；False 时 note() 会给出原因
    token_available = True
    token_note = ""

    def extract_tasks(self):
        return []

    def collect_tokens(self):
        return []

    def note(self):
        if not self.token_available:
            return self.token_note or "该 Agent 的会话记录不暴露 token 用量"
        return ""


def discover():
    """自动发现 adapters/ 目录下的所有 BaseAdapter 子类，返回实例列表。"""
    import importlib, inspect
    here = os.path.dirname(os.path.abspath(__file__))
    found = []
    for fn in sorted(os.listdir(here)):
        if not fn.endswith(".py") or fn in ("base.py", "__init__.py") or fn.startswith("_"):
            continue
        modname = "adapters." + fn[:-3]
        try:
            mod = importlib.import_module(modname)
        except Exception as e:
            print(f"  [adapter] {fn} 加载失败: {str(e)[:100]}")
            continue
        for nm, obj in inspect.getmembers(mod, inspect.isclass):
            if issubclass(obj, BaseAdapter) and obj is not BaseAdapter and obj.__module__ == modname:
                try:
                    found.append(obj())
                except Exception:
                    pass
    # L2 声明式通用适配器：从 config/adapter_rules.json 动态生成（延迟导入避免循环）
    try:
        from .generic import get_dynamic_adapters
        found.extend(get_dynamic_adapters())
    except Exception as e:
        print(f"  [generic] 动态规则加载失败: {str(e)[:80]}")
    return found


def all_session_roots():
    """所有可能的会话根目录，供通用/未知 agent 适配器使用。"""
    roots = []
    for h in all_homes() + appdata_roots():
        for name in os.listdir(h) if os.path.isdir(h) else []:
            p = os.path.join(h, name)
            if os.path.isdir(p):
                roots.append(p)
    return roots
