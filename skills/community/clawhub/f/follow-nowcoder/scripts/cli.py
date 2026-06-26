#!/usr/bin/env python
"""NowCoder CLI 入口脚本

使用方法:
  python scripts/cli.py <command> [args...]
  python -m nowcoder.cli <command> [args...]
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入并运行 CLI
from src.cli import main

if __name__ == "__main__":
    main()
