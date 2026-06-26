# arXiv Search Skill
# 用于检索、下载和分析 arXiv 论文的工具集

__version__ = "1.0.0"
__author__ = "ArXiv Search Skill"

# 延迟导入，避免循环依赖和未安装依赖时的问题
__all__ = ["search", "download", "metadata", "batch_search", "summarize", "utils"]

def __getattr__(name):
    if name in __all__:
        import importlib
        return importlib.import_module(f'.{name}', __name__)
    raise AttributeError(f"module {__name__} has no attribute {name}")
