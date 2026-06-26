import sys
sys.stdout.reconfigure(encoding='utf-8')
from a_stock_watcher import get_stock_realtime

r = get_stock_realtime('002892')
if r.get('success'):
    print(f"{r['name']} ({r['code']}): ¥{r['current_price']:.2f} ({r['change_pct']:+.2f}%)")
else:
    print("获取失败")
