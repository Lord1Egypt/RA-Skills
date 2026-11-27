#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Qwen Code 适配器（路径与字段来自 ccusage 源码 rust/adapters/qwen/）。

  ~/.qwen/projects/<project>/chats/*.jsonl
  归档：~/.qwen/projects/<project>/chats/archive/*.jsonl
  （环境变量 QWEN_DATA_DIR 可覆盖；归档单层，不递归更深层）

  assistant 消息：{"type":"assistant", "model":"...", "sessionId":"...",
                   "usageMetadata":{"promptTokenCount":...,
                                    "candidatesTokenCount":...,
                                    "cachedContentTokenCount":...,
                                    "thoughtsTokenCount":...,
                                    "totalTokenCount":...}}
本机未安装 Qwen Code，未用真实会话验证；路径与字段名来自权威实现。
"""
from ._declarative import DeclarativeAdapter


class QwenAdapter(DeclarativeAdapter):
    name = "Qwen Code"
    dir_patterns = (".qwen/projects/*/chats", ".qwen/projects/*/chats/archive")
    file_globs = ("*.jsonl",)
    data_style = "jsonl"
    token_spec = {
        "input": ("promptTokenCount",),
        "output": ("candidatesTokenCount",),
        "cache": ("cachedContentTokenCount",),
        "reason": ("thoughtsTokenCount",),
        "total": ("totalTokenCount",),
        "model": ("model",),
    }
    verified = False
    verification_note = "按 ccusage 披露的 ~/.qwen/projects/*/chats/*.jsonl 编写，本机未装，未用真实会话验证"
