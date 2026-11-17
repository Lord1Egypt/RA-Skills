#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""钢结构算量 -> lis-skill-bus 强制契约接线（薄壳）。

实现已抽到共享模块 cad_statesync_core.py（cad-file-reader/scripts），
本文件只传本技能参数；行为与其他算量技能的 statesync 逐函数等价（2026-10-30 抽共享）。
push  : 输出契约包装成 cad-contract/v1 发到 lis-skill-bus
pull  : 从 bus 拉取最近契约并按本专业 target sections 命中判定

正式识图链路要求 bus 可用；缺 bus 时退出码 2，不降级为本地识图。

用法：
  python3 gangjiegou_statesync.py push --entry-file 输出.json --project 项目 \
          [--building 楼栋] [--floor 楼层] [--specialty 钢结构] [--skill gangjiegou]
  python3 gangjiegou_statesync.py pull --project 项目 [--building 楼栋] [--floor 楼层] \
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
    print("[gangjiegou statesync] 找不到共享模块 cad_statesync_core.py"
          "（试过 CAD_FILE_READER_SCRIPTS / 融合包 modules / 技能根）", file=sys.stderr)
    raise SystemExit(2)

from cad_statesync_core import Core  # noqa: E402


class BusRequiredCore(Core):
    """钢结构的正式识图链路要求 bus，仅保留共享核心的命中判定。"""

    def find_bus_client(self):
        if not hasattr(self, "_required_bus_client"):
            self._required_bus_client = super().find_bus_client()
        return self._required_bus_client

    def _ensure_bus(self) -> bool:
        if self.find_bus_client() is not None:
            return True
        self.log_err(
            "正式识图链路要求 lis-skill-bus>=0.1.11；请先安装总线。"
            "本技能不会降级为本地识图，图纸必须由 cad-file-reader 解析。"
        )
        return False

    def cmd_push(self, args):
        if not self._ensure_bus():
            return 2
        return super().cmd_push(args)

    def cmd_pull(self, args):
        if not self._ensure_bus():
            return 2
        return super().cmd_pull(args)


def run_required_bus_cli(argv=None):
    core = BusRequiredCore(
        skill="gangjiegou",
        specialty="钢结构",
        sections=['members', 'sections', 'steel_geometry', 'connections', 'materials', 'finishes'],
        core_sections=['members', 'sections'],
    )
    core.SCRIPT_DIR = SCRIPT_DIR
    return core.run_cli(argv)

if __name__ == "__main__":
    raise SystemExit(run_required_bus_cli(sys.argv[1:]))
