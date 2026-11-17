"""dnd-check 启动器：不依赖 PYTHONPATH，直接把包内引擎加进 sys.path。

为什么需要它：
    LobsterAI/嵌入式 Python 发行版会**忽略 PYTHONPATH**，只靠环境变量注入
    sys.path 会报 `No module named 'dnd_engine'`。这里显式插路径，任何解释器都能跑。

用法：
    dnd-check --actor 老白 --skill 潜行 --dc 15     # 省略子命令时默认 check
    dnd-check check --actor 老白 --skill 潜行 --dc 15
    dnd-check verify --workspace .                  # 其它子命令直接透传
"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
for candidate in (HERE / "dnd-engine" / "src", HERE / "src"):
    if candidate.is_dir():
        sys.path.insert(0, str(candidate))
        break

from dnd_engine.cli import main  # noqa: E402

argv = sys.argv[1:]
# 没写子命令（或直接给开关）时默认走 check，让「一条命令」成立
if not argv or argv[0].startswith("-"):
    argv = ["check", *argv]
sys.argv = [sys.argv[0], *argv]
main()
