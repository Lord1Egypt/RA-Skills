#!/usr/bin/env python3
"""
arXiv 检索与分析 Skill - 主入口
便捷的统一命令行接口
"""

import sys
import argparse
from pathlib import Path


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="arXiv 检索与分析 Skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
子命令:
  search      - 检索论文
  download    - 下载论文
  metadata    - 元数据处理
  batch       - 批量检索
  summarize   - 论文总结

使用示例:
  arxiv_search.py search --query "deep learning"
  arxiv_search.py download --id 2301.01234
  arxiv_search.py metadata --input results.json --format bibtex
        """
    )

    parser.add_argument("subcommand", help="子命令 (search, download, metadata, batch, summarize)")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="子命令参数")

    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    # 解析子命令
    args = parser.parse_args()

    # 导入并运行相应的模块
    script_dir = Path(__file__).parent / "scripts"
    sys.path.insert(0, str(Path(__file__).parent))

    subcommand_map = {
        "search": "search",
        "download": "download",
        "metadata": "metadata",
        "batch": "batch_search",
        "summarize": "summarize",
    }

    if args.subcommand not in subcommand_map:
        print(f"未知的子命令: {args.subcommand}")
        parser.print_help()
        return 1

    module_name = subcommand_map[args.subcommand]

    # 构建新的 argv
    module_path = script_dir / f"{module_name}.py"
    new_argv = [str(module_path)] + args.args

    # 执行模块
    import subprocess

    return subprocess.call([sys.executable] + new_argv)


if __name__ == "__main__":
    sys.exit(main())
