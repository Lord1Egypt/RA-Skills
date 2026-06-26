#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from a_stock_watcher import get_stock_realtime, format_stock_info

code = '002892'
print("=" * 60)
print(f"📊 002892.SZ 科力电机 收盘报告")
print("=" * 60)

result = get_stock_realtime(code)
if result and result.get('success'):
    print(format_stock_info(result))
    
    # 简单分析
    change_pct = result.get('change_pct', 0)
    current_price = result.get('current_price', 0)
    
    print("\n📈 今日点评:")
    if change_pct > 3:
        print("  强势上涨，表现优异 ✅")
    elif change_pct > 0:
        print("  温和上涨，趋势向好 📈")
    elif change_pct > -3:
        print("  小幅调整，正常波动 ➖")
    else:
        print("  弱势下跌，注意风险 📉")
    
    print("\n⏰ 数据时间:", result.get('update_time', '未知'))
    print("=" * 60)
else:
    print("❌ 获取数据失败")
    print("=" * 60)
