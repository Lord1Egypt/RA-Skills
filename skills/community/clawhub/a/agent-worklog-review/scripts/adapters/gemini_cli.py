#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gemini CLI 适配器（路径来自 ccusage 源码 rust/adapters/gemini/）。

  ~/.gemini/tmp/<project-hash>/chats/*.json 或 *.jsonl
  （环境变量 GEMINI_DATA_DIR 可覆盖；ccusage 也接受 chats 目录之外的 .jsonl）
  token 在 assistant 消息的 usageMetadata：
    promptTokenCount / candidatesTokenCount / cachedContentTokenCount /
    thoughtsTokenCount / totalTokenCount
本机未安装，未用真实会话验证；路径与字段名来自权威实现。
"""
from ._declarative import DeclarativeAdapter


class GeminiCLIAdapter(DeclarativeAdapter):
    name = "Gemini CLI"
    dir_patterns = (".gemini/tmp/*/chats", ".gemini/tmp")
    file_globs = ("*.json", "*.jsonl")
    data_style = "jsonl"
    token_spec = {
        "input": ("promptTokenCount", "prompt_tokens", "input_tokens"),
        "output": ("candidatesTokenCount", "candidates_tokens", "output_tokens"),
        "cache": ("cachedContentTokenCount", "cached_tokens"),
        "reason": ("thoughtsTokenCount",),
        "total": ("totalTokenCount", "total_tokens"),
        "model": ("model",),
    }
    verified = False
    verification_note = "按 ccusage 披露的 ~/.gemini/tmp/*/chats/*.json 编写，本机未装，未用真实会话验证"
