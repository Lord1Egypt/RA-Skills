#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用会话解析工具（内部模块，下划线开头不会被 discover 当作适配器）。

提供跨 Agent 复用的：
- JSONL / JSON 文件读取
- 用户消息提取（role / type / speaker 多种字段）
- token 字段递归查找（usage / tokens / token_count 等）
- 有限深度候选目录展开（避免全 home 递归卡死）
"""
import os, json, glob

# 常见的「角色」字段名与「用户」取值
ROLE_KEYS = ("role", "type", "speaker", "author", "from", "sender", "kind")
USER_VALUES = ("user", "human", "1", 1, "USER", "User", "userMessage", "user_message")
# 常见的正文/提示词字段名
TEXT_KEYS = ("content", "text", "message", "prompt", "input", "body", "value",
             "query", "question", "user_prompt", "request")
# 常见的 token 字段名（递归查找时用）
TOKEN_KEYS = {
    "input": ("input_tokens", "prompt_tokens", "inputTokens", "promptTokens",
              "input_tokens_count", "prompt_token_count", "input"),
    "output": ("output_tokens", "completion_tokens", "outputTokens", "completionTokens",
               "output_tokens_count", "candidate_token_count", "output"),
    "cache": ("cache_tokens", "cached_tokens", "cache_read_input_tokens",
              "cached_input_tokens", "cacheTokens", "cache_read_tokens"),
    "reasoning": ("reasoning_tokens", "thinking_tokens", "reasoningTokens"),
    "total": ("total_tokens", "totalTokens", "tokens", "total_token_count"),
    "model": ("model", "modelName", "model_name", "model_id"),
}


def open_jsonl(fp, limit=None):
    """逐行解析 JSONL；limit 限制返回行数（避免超大文件卡死）。"""
    out = []
    try:
        with open(fp, encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                if limit and i >= limit:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        pass
    return out


def open_json(fp):
    try:
        with open(fp, encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return None


def as_text(v):
    """把 content 字段（str / list[dict] / dict）压成纯文本。"""
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        for k in TEXT_KEYS:
            if k in v and isinstance(v[k], str):
                return v[k]
        return ""
    if isinstance(v, list):
        parts = []
        for it in v:
            if isinstance(it, str):
                parts.append(it)
            elif isinstance(it, dict):
                t = as_text(it)
                if t:
                    parts.append(t)
        return "\n".join(parts)
    return ""


def is_user(obj, role_keys=ROLE_KEYS, user_values=USER_VALUES):
    """判断一条消息是否为用户输入。"""
    if not isinstance(obj, dict):
        return False
    for k in role_keys:
        if k in obj:
            v = obj[k]
            if v in user_values or (isinstance(v, str) and v.lower() in ("user", "human")):
                return True
            # 有些 agent 用 {"role":{"type":"user"}}
            if isinstance(v, dict) and any(x in v.values() for x in ("user", "human", 1)):
                return True
    return False


def message_text(obj, text_keys=TEXT_KEYS):
    if isinstance(obj, str):
        return obj
    if not isinstance(obj, dict):
        return ""
    for k in text_keys:
        if k in obj:
            t = as_text(obj[k])
            if t:
                return t
    # 兼容 {"message":{"content":...}} 嵌套
    for k in ("message", "content", "data"):
        if isinstance(obj.get(k), dict):
            t = message_text(obj[k], text_keys)
            if t:
                return t
    return ""


def find_token(obj, key_group, default=0):
    """在 dict 中递归查找指定 token 字段；返回第一个非零值。"""
    keys = TOKEN_KEYS.get(key_group, ())
    if not isinstance(obj, dict):
        return default
    # 优先浅层
    for k in keys:
        v = obj.get(k)
        if isinstance(v, (int, float)) and v:
            return int(v)
    # 递归一层常见容器
    for container in ("usage", "token_usage", "tokens", "token_count", "metrics",
                      "usage_metadata", "tokenUsage", "cost", "statistics"):
        sub = obj.get(container)
        if isinstance(sub, dict):
            for k in keys:
                v = sub.get(k)
                if isinstance(v, (int, float)) and v:
                    return int(v)
    return default


def expand_dirs(roots, rel_patterns):
    """展开候选目录：root/rel_pattern，支持单层 * 通配，不做深度递归。

    rel_patterns 形如 ["zcode/sessions", ".kimi/sessions/*"]。
    """
    seen, out = set(), []
    for root in roots:
        for rel in rel_patterns:
            pattern = os.path.join(root, *rel.replace("/", "\\").split("\\"))
            if "*" in pattern:
                matches = glob.glob(pattern)
            else:
                matches = [pattern]
            for p in matches:
                if not os.path.isdir(p):
                    continue
                k = os.path.normcase(os.path.abspath(p))
                if k not in seen:
                    seen.add(k)
                    out.append(p)
    return out
