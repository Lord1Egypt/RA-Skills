#!/usr/bin/env python
"""export_results 命令行入口"""

import argparse

from _errors import SkillError
from _output import print_output, print_error, configure_windows_stdio

from capabilities.export_results import service


COMMAND_NAME = "export_results"
COMMAND_DESC = "导出任务台账为 Excel 产物（xlsx/csv），非交互式展示"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cli.py export_results",
        description="把任务台账导出为 Excel/CSV 产物文件",
    )
    p.add_argument("--only_done", action="store_true", default=False,
                   help="只导出已处理完成的任务（成功/失败/跳过/取消）")
    p.add_argument("--base_dir", default=None, help="台账根目录（默认当前工作目录）")
    return p


def main():
    configure_windows_stdio()
    args = build_parser().parse_args()

    try:
        result = service.export_results(base_dir=args.base_dir, only_done=args.only_done)
    except SkillError as e:
        print_error(e)
        return
    except Exception as e:
        print_error(e)
        return

    md = "✅ 已导出批量任务结果（{} 行）：`{}`".format(
        result["row_count"], result["file_path"])
    if result.get("package_path"):
        md += "\n✅ 已打包全部产物图：`{}`（含 {} 个文件，表格 + images/ 图片）".format(
            result["package_path"], result.get("package_file_count"))
    md += "\n请用 present_files 把表格与 zip 包作为产物展示给用户（非交互式）。"

    print_output(True, md, result)


if __name__ == "__main__":
    main()
