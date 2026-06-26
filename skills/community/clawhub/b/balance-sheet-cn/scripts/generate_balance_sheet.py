#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资产负债表生成 - 命令行入口
"""

import sys
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from balance_sheet_generator import BalanceSheetGenerator


def main():
    if len(sys.argv) < 2:
        print('用法：python3 generate_balance_sheet.py <源文件路径> [输出文件路径]')
        print()
        print('示例:')
        print('  python3 generate_balance_sheet.py 财务报表 202511-t.xlsx')
        print('  python3 generate_balance_sheet.py 财务报表 202511-t.xlsx 资产负债表.xlsx')
        sys.exit(1)
    
    src_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else '资产负债表.xlsx'
    
    try:
        generator = BalanceSheetGenerator(src_path)
        generator.generate(output_path)
        print()
        print('生成完成！')
        print(f'  银行余额：招商={generator.cmb_balance}, 交通={generator.comm_balance}')
        print(f'  分类统计：应收={generator.receivable_total}, 预收={generator.advance_total}, 应付={generator.payable_total}')
        print(f'  经营利润：{generator.operating_profit}')
    except Exception as e:
        print(f'错误：{e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
