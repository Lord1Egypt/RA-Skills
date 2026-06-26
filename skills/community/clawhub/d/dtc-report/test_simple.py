#!/usr/bin/env python3
"""
简单的报告生成测试 - 只测试 warehouse 数据
"""

import sys
import json
sys.path.insert(0, r'C:\Users\wwl\.openclaw\workspace-跨境电商\skills\dtc-report\scripts')

from warehouse import read_warehouse_data

print('读取仓库数据...')
result = read_warehouse_data('2026-Q1')

print('\n月份列表 (%d 个月):' % len(result['months']))
print(json.dumps(result['months']))

print('\n美西自营仓 (USCAEA02) 出库件数:')
uscaea02_outbound = result['self_run_trend']['USCAEA02']['outbound']
for i, m in enumerate(result['months']):
    print('  %s: %s 件' % (m, uscaea02_outbound[i]))

print('\n验证 2026 年 Q1 数据:')
for i, m in enumerate(result['months']):
    if m.startswith('2026-'):
        print('  %s: USCAEA02=%s 件，USNJHM01=%s 件' % (
            m, 
            uscaea02_outbound[i],
            result['self_run_trend']['USNJHM01']['outbound'][i]
        ))

print('\n完成！')
