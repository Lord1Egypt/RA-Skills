# -*- coding: utf-8 -*-
"""测试目录级 conftest：确保 scripts/ 始终在 sys.path 上。

背景（真实 CI 缺陷）：tests/ 下多个测试直接在模块顶部 `import security_scan`，
而 security_scan.py 位于 scripts/ 子目录。原本仅靠仓库根 conftest.py 把 scripts/
注入 sys.path；但在 CI（Linux）上根 conftest 因 rootdir 探测差异未生效，导致
`ModuleNotFoundError: No module named 'security_scan'` —— 整个测试收集失败、
pytest 以 exit code 2 退出（本地 Windows 因收集顺序碰巧过关，掩盖了该脆弱性）。

本文件位于测试目录内，pytest 收集测试时必然会加载它，从而确定性地把 scripts/
加入 sys.path，彻底消除对根 conftest / 收集顺序 / 操作系统的依赖。
"""
import sys
from pathlib import Path

_SCRIPTS = str(Path(__file__).resolve().parent.parent / "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)
