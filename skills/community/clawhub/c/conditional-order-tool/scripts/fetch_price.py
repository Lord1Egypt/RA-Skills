#!/usr/bin/env python3
"""
获取股票/ETF 实时价格
数据源：东方财富 API（免费、无需 key）
"""

import json
import sys
import urllib.request
import urllib.parse


def fetch_east_money_price(code: str) -> dict:
    """
    通过东方财富 API 获取实时行情（多源备用）
    code: 6 位代码，如 518880, 600519
    返回: {code, name, price, change_pct, volume, amount, time, market}
    """
    # 判断市场：沪市 51/60 开头，深市 00/15/16/3 开头
    if code.startswith(('51', '60', '68')):
        market = 1  # 沪市
        secid = f"1.{code}"
    else:
        market = 0  # 深市
        secid = f"0.{code}"

    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f44,f45,f46,f47,f48,f50,f51,f52,f57,f58,f60,f170,f171"

    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://quote.eastmoney.com/',
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        if data.get('data'):
            d = data['data']
            return {
                'code': code,
                'name': d.get('f58', ''),
                'price': d.get('f43') / 100 if d.get('f43') else None,
                'change_pct': d.get('f170', 0) / 100 if d.get('f170') else None,
                'volume': d.get('f47', 0),  # 手
                'amount': d.get('f46', 0),  # 元
                'time': d.get('f171', ''),
                'market': 'SH' if market == 1 else 'SZ',
                'high': d.get('f44', 0) / 100 if d.get('f44') else None,
                'low': d.get('f45', 0) / 100 if d.get('f45') else None,
                'open': d.get('f47', 0) / 100 if d.get('f47') else None,
                'pre_close': d.get('f60', 0) / 100 if d.get('f60') else None,
            }
        else:
            return {'code': code, 'error': '未找到该代码，请检查'}
    except Exception as e:
        # 东方财富失败，尝试腾讯财经
        tencent_result = fetch_tencent_price(code)
        if tencent_result:
            return tencent_result
        return {'code': code, 'error': str(e)}


def fetch_tencent_price(code: str) -> dict:
    """
    通过腾讯财经 API 获取实时行情（备用源）
    code: 6 位代码
    返回: 同上
    """
    if code.startswith(('51', '60', '68')):
        prefix = 'sh'
    else:
        prefix = 'sz'
    
    url = f'https://qt.gtimg.cn/q={prefix}{code}'
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://finance.qq.com/'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode('gbk')
        
        parts = raw.split('~')
        if len(parts) > 35:
            return {
                'code': code,
                'name': parts[1],
                'price': float(parts[3]) if parts[3] else None,
                'change_pct': float(parts[32]) if len(parts) > 32 and parts[32] else None,
                'volume': float(parts[5]) * 100 if parts[5] else None,
                'amount': float(parts[37]) * 10000 if len(parts) > 37 and parts[37] else None,
                'market': prefix.upper(),
                'high': float(parts[33]) if len(parts) > 33 and parts[33] else None,
                'low': float(parts[34]) if len(parts) > 34 and parts[34] else None,
                'open': float(parts[35]) if len(parts) > 35 and parts[35] else None,
                'pre_close': float(parts[4]) if parts[4] else None,
            }
    except:
        pass
    
    return None


def fetch_qdii_premium(code: str) -> dict:
    """
    获取跨境 ETF 溢价率
    需要 IOPV 数据的品种
    """
    if code.startswith(('51', '60', '68')):
        market = 1
    else:
        market = 0

    secid = f"{market}.{code}"
    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f127,f170"

    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://quote.eastmoney.com/'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        if data.get('data'):
            d = data['data']
            price = d.get('f43', 0) / 100 if d.get('f43') else 0
            iopv = d.get('f127', 0) / 1000 if d.get('f127') else 0  # f127 是 IOPV，单位通常是千分之一

            if iopv > 0 and price > 0:
                premium = (price - iopv) / iopv * 100
            else:
                premium = None

            return {
                'code': code,
                'price': price,
                'iopv': iopv,
                'premium_pct': round(premium, 2) if premium is not None else None,
            }
    except:
        pass

    return {'code': code, 'error': '无法获取溢价数据'}


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'error': '请提供代码'}, ensure_ascii=False))
        sys.exit(1)

    code = sys.argv[1]
    result = fetch_east_money_price(code)
    print(json.dumps(result, ensure_ascii=False, indent=2))
