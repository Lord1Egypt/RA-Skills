#!/usr/bin/env python3
"""content_formatter.py - orchestrator调用入口(wrapper)

orchestrator的_is_skill_tool()和call_skill()使用命名约定:
  script_name = tool_name.replace('-', '_') + ".py"  →  content_formatter.py

实际排版逻辑在format_engine.py中,本文件仅作为命名适配入口。
"""
import sys
from pathlib import Path

# 添加项目根目录到sys.path(format_engine.py依赖mcps.shared)
_script_dir = Path(__file__).resolve().parent
_project_root = _script_dir.parent.parent.parent  # d:\JueJin
for p in [str(_script_dir), str(_project_root), str(_project_root / "scripts")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from format_engine import main

if __name__ == "__main__":
    main()
