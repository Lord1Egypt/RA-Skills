#!/usr/bin/env python
"""build_apply_card 命令行入口"""

import argparse

from _errors import SkillError
from _output import print_output, print_error, configure_windows_stdio

from capabilities.build_apply_card import service


COMMAND_NAME = "build_apply_card"
COMMAND_DESC = "合并逐条目应用参数为批量应用卡（route=batch-apply）"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cli.py build_apply_card",
        description="把逐任务的应用参数合并为单张批量应用确认卡参数",
    )
    p.add_argument("--items", required=True,
                   help='JSON 数组：[{"task_id":"T001","card_params":{...执行技能单条目应用参数原样...}}, ...]')
    p.add_argument("--base_dir", default=None, help="台账根目录（默认当前工作目录）")
    return p


def main():
    configure_windows_stdio()
    args = build_parser().parse_args()

    try:
        result = service.build_apply_card(items_json=args.items, base_dir=args.base_dir)
    except SkillError as e:
        print_error(e)
        return
    except Exception as e:
        print_error(e)
        return

    md = "✅ 已生成批量应用卡参数（{} 个条目，任务：{}）。".format(
        result["updated_count"], ", ".join(result["task_ids"]))
    md += "\n请把 data.card 作为 `offer_select_card --json` 弹出批量应用确认卡；" \
          "卡片回传后按各任务回执用 save_result --apply_status 落账。"

    print_output(True, md, result)


if __name__ == "__main__":
    main()
