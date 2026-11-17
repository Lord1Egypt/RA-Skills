#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""安装算量 -> lis-skill-bus 可选接线（薄壳）。

实现已抽到共享模块 cad_statesync_core.py（cad-file-reader/scripts），
本文件只传本技能参数；行为与原 424 行实现逐函数等价（2026-10-30 抽共享）。
push  : 输出契约包装成 cad-contract/v1 发到 lis-skill-bus（未装 bus 降级直写本机）
pull  : 从 bus 拉取最近契约并按本专业 target sections 命中判定

用法：
  python3 anzhuang_statesync.py push --entry-file 输出.json --project 项目 \
          [--building 楼栋] [--floor 楼层] [--specialty 安装] [--skill anzhuang]
  python3 anzhuang_statesync.py pull --project 项目 [--building 楼栋] [--floor 楼层] \
          [--out 落盘.json] [--out-dir 输出目录] [--entry-id xxx] [--require-core|--require-all]

纯 stdlib、不联网、不读云；公司数据只落本机。
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def _load_core():
    """多候选定位 cad_statesync_core（融合包/技能根/环境变量/家目录）。"""
    import os
    candidates = []
    env = os.environ.get("CAD_FILE_READER_SCRIPTS")
    if env:
        candidates.append(Path(env))
    here = SCRIPT_DIR
    # 融合包布局：modules/<本技能>/scripts -> modules/cad-file-reader/scripts
    candidates.append(here.parent.parent / "cad-file-reader" / "scripts")
    # 技能根布局：<skills>/<本技能>/scripts -> <skills>/cad-file-reader/scripts
    candidates.append(here.parent.parent.parent / "cad-file-reader" / "scripts")
    for home in (Path.home() / ".workbuddy" / "skills" / "cad-file-reader" / "scripts",
                 Path.home() / ".codex" / "skills" / "cad-file-reader" / "scripts"):
        candidates.append(home)
    for c in candidates:
        if (c / "cad_statesync_core.py").is_file():
            if str(c) not in sys.path:
                sys.path.insert(0, str(c))
            return True
    return False


if not _load_core():
    print("[anzhuang statesync] 找不到共享模块 cad_statesync_core.py"
          "（试过 CAD_FILE_READER_SCRIPTS / 融合包 modules / 技能根）", file=sys.stderr)
    raise SystemExit(2)

from cad_statesync_core import run_cli  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(run_cli(
        skill="anzhuang",
        specialty="安装",
        sections=['route_segments', 'circuits', 'systems', 'equipment', 'labels', 'measurements'],
        core_sections=['circuits', 'route_segments'],
        argv=sys.argv[1:],
        script_dir=SCRIPT_DIR,
    ))
