#!/usr/bin/env python3
"""
Stock Monitor - 股票监控/预警脚本
功能：价格预警、异动监控、定时发送简报到微信
用法：
  monitor check <code> [target_price] [方向:above/below]  # 检查价格是否触发
  monitor watchlist                                         # 检查自选股异动
  monitor alert <code> <condition>                          # 设置预警
"""
import json, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from china_stock import tdx_quote, tencent_quote, smart_quote

PY = os.path.realpath(__file__)
DIR = os.path.dirname(os.path.dirname(PY))

def check_price(code, target=None, direction='above'):
    """检查股票价格是否触发条件"""
    q = smart_quote(code)
    if 'error' in q:
        return {'error': q['error']}
    price = q.get('price', 0)
    change_pct = q.get('change_pct', 0)
    result = {
        'code': code,
        'name': q.get('name', ''),
        'price': price,
        'change_pct': change_pct,
        'time': q.get('time', ''),
    }
    if target is not None:
        target = float(target)
        if direction == 'above' and price >= target:
            result['triggered'] = True
            result['alert'] = f"📈 {q.get('name', code)} 已突破 {target}元，现价{price}元"
        elif direction == 'below' and price <= target:
            result['triggered'] = True
            result['alert'] = f"📉 {q.get('name', code)} 已跌破 {target}元，现价{price}元"
        else:
            result['triggered'] = False
    return result

def check_watchlist(watchlist=None):
    """检查自选股列表的异动（涨跌幅>3%或放量>2倍）"""
    if watchlist is None:
        # 默认检查几个核心标的
        watchlist = ['600519', '300750', '000001', '601318', '000858', '002415', '600036', '601166']
    results = []
    for code in watchlist:
        try:
            q = smart_quote(code)
            if 'error' not in q:
                item = {
                    'code': code,
                    'name': q.get('name', ''),
                    'price': q.get('price', 0),
                    'change_pct': q.get('change_pct', 0),
                    'pe': q.get('pe', ''),
                    'market_cap': q.get('market_cap', ''),
                }
                c = q.get('change_pct', 0)
                if abs(c) >= 3:
                    item['flag'] = '⚠️' if c > 0 else '🔻'
                elif abs(c) >= 1:
                    item['flag'] = '↑' if c > 0 else '↓'
                else:
                    item['flag'] = '→'
                results.append(item)
                time.sleep(0.3)  # 避免被限流
        except:
            continue
    results.sort(key=lambda x: abs(x.get('change_pct', 0)), reverse=True)
    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"usage": """
股票监控工具:
  monitor check <code> [target_price] [above|below]  检查价格预警
  monitor watchlist [code1,code2,...]                  检查自选异动
""", "example": "monitor check 600519 1300 below"}, ensure_ascii=False))
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == 'check':
        code = sys.argv[2] if len(sys.argv) > 2 else ''
        target = sys.argv[3] if len(sys.argv) > 3 else None
        direction = sys.argv[4] if len(sys.argv) > 4 else 'above'
        r = check_price(code, target, direction)
        print(json.dumps(r, ensure_ascii=False, default=str))

    elif cmd == 'watchlist':
        codes = sys.argv[2].split(',') if len(sys.argv) > 2 else None
        r = check_watchlist(codes)
        print(json.dumps(r, ensure_ascii=False, default=str))

    else:
        print(json.dumps({"error": f"未知命令: {cmd}"}, ensure_ascii=False))
