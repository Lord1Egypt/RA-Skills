#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Amp（Sourcegraph）适配器：~/.amp/ 或 ~/.local/share/amp/ 会话。

verified=False：本机未安装，未用真实会话验证。
"""
from ._declarative import DeclarativeAdapter


class AmpAdapter(DeclarativeAdapter):
    name = "Amp"
    dir_patterns = (".amp/threads/*", ".amp/sessions/*", ".amp/*",
                    ".local/share/amp/threads/*", ".local/share/amp/sessions/*")
    file_globs = ("*.jsonl", "*.json", "messages.json")
    data_style = "jsonl"
    token_spec = None
    verified = False
