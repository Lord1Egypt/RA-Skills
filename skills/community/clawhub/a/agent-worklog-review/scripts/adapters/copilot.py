#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GitHub Copilot CLI 适配器（路径来自 ccusage 源码 rust/adapters/copilot/）。

  ~/.copilot/otel/*.jsonl                       OpenTelemetry 用量导出
  ~/.copilot/session-state/<session>/events.jsonl   CLI 会话事件
  （环境变量 COPILOT_HOME / COPILOT_OTEL_FILE_EXPORTER_PATH 可覆盖）

此前猜测的 ~/.copilot/sessions/* 不存在；本机 ~/.copilot/ 仅有 config + logs。
token_spec=None：本地事件不暴露可靠 token 字段，不伪造。
"""
from ._declarative import DeclarativeAdapter


class CopilotAdapter(DeclarativeAdapter):
    name = "GitHub Copilot"
    dir_patterns = (".copilot/otel", ".copilot/session-state/*")
    file_globs = ("*.jsonl",)
    data_style = "jsonl"
    token_spec = None
    verified = False
    verification_note = ("按 ccusage 披露的 ~/.copilot/otel 与 ~/.copilot/session-state/*/events.jsonl "
                         "编写；本机仅存配置/日志，未用真实会话验证")
