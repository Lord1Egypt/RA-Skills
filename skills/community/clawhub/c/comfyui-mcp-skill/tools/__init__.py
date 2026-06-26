"""
工具模块包
"""

import pkgutil
import importlib


def register_all_tools(mcp):
    """自动扫描 tools 目录"""

    from . import __path__ as tools_path

    for _, module_name, _ in pkgutil.iter_modules(tools_path):
        module = importlib.import_module(f"{__name__}.{module_name}")

        if hasattr(module, "register_tools"):
            module.register_tools(mcp)
