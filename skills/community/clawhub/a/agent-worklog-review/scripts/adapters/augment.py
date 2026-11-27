#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Augment Code 适配器：~/.augment/ 会话缓存。

Augment 主要是 IDE 插件，会话多在云端；本地缓存可能只有少量元数据。
verified=False：本机未安装，未用真实会话验证。
"""
from ._declarative import DeclarativeAdapter


class AugmentAdapter(DeclarativeAdapter):
    name = "Augment Code"
    dir_patterns = (".augment/sessions/*", ".augment/history/*", ".augment/chat/*",
                    ".augment/*", "augment-code/sessions/*")
    file_globs = ("*.jsonl", "*.json", "chat.json")
    data_style = "jsonl"
    token_spec = None
    verified = False
