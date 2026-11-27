#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiro（AWS IDE Agent）适配器：~/.kiro/ 会话。

Kiro 基于 VS Code 内核，会话可能在 state.vscdb 或 ~/.kiro/sessions/。
verified=False：本机未安装，未用真实会话验证。
"""
from ._declarative import DeclarativeAdapter


class KiroAdapter(DeclarativeAdapter):
    name = "Kiro"
    dir_patterns = (".kiro/sessions/*", ".kiro/conversations/*", ".kiro/chat/*",
                    ".kiro/History/*", ".kiro/*")
    file_globs = ("*.jsonl", "*.json", "conversation.json")
    data_style = "jsonl"
    token_spec = None
    verified = False
