#!/usr/bin/env python
"""build_result_card 命令行入口"""

import argparse

from _errors import SkillError
from _output import print_output, print_error, configure_windows_stdio

from capabilities.build_result_card import service


COMMAND_NAME = "build_result_card"
COMMAND_DESC = "生成执行结果展示卡参数（进度 + 逐任务结果 + 应用入口）"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cli.py build_result_card",
        description="从台账生成执行结果展示卡参数（route=batch-result-view）",
    )
    p.add_argument("--item_ids", default=None, nargs="+",
                   help="只展示指定商品的任务（默认全部）")
    p.add_argument("--base_dir", default=None, help="台账根目录（默认当前工作目录）")
    return p


def main():
    configure_windows_stdio()
    args = build_parser().parse_args()

    try:
        result = service.build_result_card(base_dir=args.base_dir, item_ids=args.item_ids)
    except SkillError as e:
        print_error(e)
        return
    except Exception as e:
        print_error(e)
        return

    card = result["card"]
    md = "✅ 已生成执行结果展示卡参数（批次 {}，共 {} 个任务，{} 个可应用）。".format(
        result["batch_id"], card["progress"]["total"], result["appliable_count"])
    md += "\n请把 data.card 作为 `offer_select_card --json` 弹出结果展示卡。"

    print_output(True, md, result)


if __name__ == "__main__":
    main()
