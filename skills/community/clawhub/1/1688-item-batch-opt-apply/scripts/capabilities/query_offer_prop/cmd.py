"""query_offer_prop 命令入口。"""

import argparse
from pathlib import Path

from _output import configure_windows_stdio, print_error, print_output
from capabilities.query_offer_prop.service import query_offer_prop

COMMAND_NAME = "query_offer_prop"
COMMAND_DESC = "按匹配词查询商品实际属性（最多 20 个商品，只读）"


def main():
    configure_windows_stdio()
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--items", help="含 offerId/propertyNames 的 JSON 数组")
    source.add_argument("--items_file", help="保存上述数组的 UTF-8 JSON 文件")
    args = parser.parse_args()
    try:
        payload = (Path(args.items_file).read_text(encoding="utf-8-sig")
                   if args.items_file else args.items)
        result = query_offer_prop(payload)
    except Exception as exc:
        print_error(exc)
        raise SystemExit(1)
    print_output(True, "已取得查询返回，请由主 Agent 对比 CPV 并判断是否需要澄清。", result)
