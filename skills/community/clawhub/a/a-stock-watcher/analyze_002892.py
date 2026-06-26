import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')

from a_stock_watcher import get_stock_realtime, get_technical_analysis

print("=" * 60)
print("科力尔 (002892) 股票分析")
print("=" * 60)

# 实时行情
print("\n【实时行情】")
realtime = get_stock_realtime('002892')
if realtime.get('success'):
    print(f"股票：{realtime['name']} ({realtime['code']})")
    print(f"现价：{realtime['current_price']:.2f} 元")
    print(f"涨跌：{realtime['change']:+.2f} ({realtime['change_pct']:+.2f}%)")
    print(f"成交：{realtime.get('volume', 0):,}手")
    print(f"成交额：{realtime.get('amount', 0):.2f}万元")

# 技术分析
print("\n【技术分析】")
analysis = get_technical_analysis('002892')
print(analysis)
