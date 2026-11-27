#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Roo Code（原 Roo Cline）适配器：VS Code 扩展存储目录。

Roo Code 会话在 VS Code globalStorage 的 state.vscdb（rooveterinaryinc.roo-cline），
本机若有 Cursor/VS Code 则可能与 vscdb 适配器重复；这里只补充纯 JSON 历史，
避免重复统计。verified=False。
"""
from ._declarative import DeclarativeAdapter


class RooAdapter(DeclarativeAdapter):
    name = "Roo Code"
    dir_patterns = (".roo/sessions/*", ".roo/history/*", "roo-cline/sessions/*",
                    "Code/User/globalStorage/rooveterinaryinc.roo-cline/history/*")
    file_globs = ("*.jsonl", "*.json")
    data_style = "jsonl"
    token_spec = None
    verified = False
