#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dev_scan.py - 已停用：本技能不再内置 DWG 直读层。

正式链路固定：cad-file-reader → lis-skill-bus → 算量技能。
历史开发直读实现只保留在 $HOME/.codex/backups/suanliang-s9/ 的改动前备份里，
不随技能发布，也不提供环境变量或隐藏参数重启生产直读。
"""
from __future__ import annotations


class DevDirectDisabled(RuntimeError):
    pass


_MESSAGE = (
    "[dev_scan] 本技能已删除 DWG 直读层，生产脚本不再加载 CAD 直读库。\n"
    "正式链路：cad-file-reader 产出 cad-contract/v1 → lis-skill-bus → mep_scan --contract。"
)


def read_dwg(path: str):
    raise DevDirectDisabled(_MESSAGE)


def raw_layers(path: str):
    raise DevDirectDisabled(_MESSAGE)


__all__ = ["DevDirectDisabled", "read_dwg", "raw_layers"]

if __name__ == "__main__":
    import sys
    sys.stderr.write(_MESSAGE + "\n")
    raise SystemExit(23)
