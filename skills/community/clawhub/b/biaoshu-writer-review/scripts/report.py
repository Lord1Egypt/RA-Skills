#!/usr/bin/env python3
"""把百炼®标书结果 JSON 渲染成报告（HTML / Word .docx）。

核心渲染逻辑在 report_lib 中；本文件只保留兼容旧调用方式的 CLI 入口。
"""
from __future__ import annotations

from report_lib.generator import generate, main


if __name__ == "__main__":
    main()
