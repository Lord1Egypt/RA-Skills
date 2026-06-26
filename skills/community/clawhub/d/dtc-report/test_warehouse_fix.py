#!/usr/bin/env python3
"""
测试 warehouse.py 的月份排序修复
"""

import sys
sys.path.insert(0, r'C:\Users\wwl\.openclaw\workspace-跨境电商\skills\dtc-report\scripts')

from warehouse import read_warehouse_data

# 测试读取数据
print('测试 warehouse.py 月份排序修复...')
print('=' * 60)

result = read_warehouse_data('2026-Q1')

print('\n月份列表:')
print(result['months'])

print('\n美西自营仓 (USCAEA02) 出库件数趋势:')
uscaea02_outbound = result['self_run_trend']['USCAEA02']['outbound']
for i, m in enumerate(result['months']):
    print(f'  {m}: {uscaea02_outbound[i]:,} 件')

print('\n美东自营仓 (USNJHM01) 出库件数趋势:')
usnjhm01_outbound = result['self_run_trend']['USNJHM01']['outbound']
for i, m in enumerate(result['months']):
    print(f'  {m}: {usnjhm01_outbound[i]:,} 件')

# 验证 2026 年 3 月的数据
march_2026_idx = result['months'].index('2026-3') if '2026-3' in result['months'] else -1
if march_2026_idx >= 0:
    print(f'\n✓ 2026-3 索引：{march_2026_idx}')
    print(f'  USCAEA02 3 月出库件数：{uscaea02_outbound[march_2026_idx]:,}')
    print(f'  USNJHM01 3 月出库件数：{usnjhm01_outbound[march_2026_idx]:,}')
else:
    print('\n✗ 错误：2026-3 不在月份列表中')

print('\n' + '=' * 60)
print('测试完成！')
