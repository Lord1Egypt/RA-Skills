"""NowCoder 面经搜索 Skill - 核心模块"""

__version__ = "0.1.0"


# 支持 python -m nowcoder.cli
if __name__ == "__main__":
    from .cli import main
    main()
