import requests, re, sys

def get_a_stock(code):
    """获取A股行情"""
    code = code.strip()
    
    # 判断市场
    if code.startswith('6'):
        market = 'sh' + code
    elif code.startswith('0') or code.startswith('3'):
        market = 'sz' + code
    else:
        market = 'sh' + code
    
    url = f'https://qt.gtimg.cn/q={market}'
    r = requests.get(url, timeout=8)
    text = r.text
    
    match = re.search(r'"([^"]+)"', text)
    if not match:
        return None
    
    parts = match.group(1).split('~')
    
    # A股字段解析
    name = parts[1]
    current = float(parts[3])
    high = float(parts[5])
    low = float(parts[4])
    volume = float(parts[6])
    open_p = float(parts[9])
    change_pct = float(parts[31]) if parts[31] else 0
    change = current - open_p
    
    return {
        'market': 'A股',
        'code': code,
        'name': name,
        'current': current,
        'high': high,
        'low': low,
        'open': open_p,
        'volume': volume,
        'change': change,
        'change_pct': change_pct
    }

def get_hk_stock(code):
    """获取港股行情"""
    code = code.strip().upper()
    for suffix in ['.HK', 'HK', '.H']:
        code = code.replace(suffix, '')
    
    # 补齐到5位
    if len(code) == 4:
        code = '0' + code
    
    url = f'https://qt.gtimg.cn/q=hk{code}'
    r = requests.get(url, timeout=8)
    text = r.text.strip()
    
    if 'none_match' in text:
        return None
    
    match = re.search(r'"([^"]+)"', text)
    if not match:
        return None
    
    parts = match.group(1).split('~')
    
    name = parts[1]
    current = float(parts[3])
    high = float(parts[4])
    low = float(parts[5])
    volume = float(parts[6])
    open_p = float(parts[9])
    change_pct = ((current - open_p) / open_p) * 100 if open_p else 0
    change = current - open_p
    
    return {
        'market': '港股',
        'code': code,
        'name': name,
        'current': current,
        'high': high,
        'low': low,
        'open': open_p,
        'volume': volume,
        'change': change,
        'change_pct': change_pct
    }

def get_us_stock(code):
    """获取美股行情"""
    FINNHUB_KEY = 'd6nucg1r01qse5qn5e90d6nucg1r01qse5qn5e9g'
    
    code = code.strip().upper()
    url = f'https://finnhub.io/api/v1/quote?symbol={code}&token={FINNHUB_KEY}'
    
    try:
        r = requests.get(url, timeout=10).json()
        if r.get('c'):
            return {
                'market': '美股',
                'code': code,
                'name': code,
                'current': r['c'],
                'high': r['h'],
                'low': r['l'],
                'open': r['o'],
                'volume': r.get('v', 0),
                'change': r['d'],
                'change_pct': r['dp']
            }
    except:
        pass
    return None

def analyze(code):
    """全面分析"""
    # 尝试获取数据
    data = get_a_stock(code) or get_hk_stock(code) or get_us_stock(code)
    
    if not data:
        print(f"无法获取 {code} 的行情数据")
        return
    
    # 打印行情
    currency = 'CNY' if data['market'] == 'A股' else ('HKD' if data['market'] == '港股' else 'USD')
    
    print("="*65)
    print(f"  {data['name']} ({data['code']}) {data['market']}全面分析")
    print("="*65)
    
    print(f"\n【基本信息】")
    print(f"  股票名称: {data['name']}")
    print(f"  股票代码: {data['code']}")
    print(f"  上市市场: {data['market']}")
    
    print(f"\n【实时行情】")
    print(f"  当前价格:  {data['current']:.2f} {currency}")
    print(f"  涨跌额:    {data['change']:+.2f} ({data['change_pct']:+.2f}%)")
    print(f"  开盘:      {data['open']:.2f}")
    print(f"  最高:      {data['high']:.2f}")
    print(f"  最低:      {data['low']:.2f}")
    print(f"  成交量:    {data['volume']/10000:.2f}万")
    
    # 技术分析
    print(f"\n【技术分析】")
    
    # 振幅
    today_range = data['high'] - data['low']
    amplitude = (today_range / data['open']) * 100 if data['open'] else 0
    print(f"  今日振幅:  {amplitude:.2f}%")
    
    # 距高点/低点
    dist_high = ((data['high'] - data['current']) / data['high']) * 100 if data['high'] else 0
    dist_low = ((data['current'] - data['low']) / data['low']) * 100 if data['low'] else 0
    print(f"  距今日高点: {dist_high:.1f}%")
    print(f"  距今日低点: {dist_low:.1f}%")
    
    # 趋势判断
    print(f"\n  走势判断:")
    if data['change_pct'] > 3:
        trend = "  [强势上涨]"
    elif data['change_pct'] > 1:
        trend = "  [明显上涨]"
    elif data['change_pct'] > 0:
        trend = "  [小幅上涨]"
    elif data['change_pct'] > -1:
        trend = "  [小幅回调]"
    elif data['change_pct'] > -3:
        trend = "  [明显下跌]"
    else:
        trend = "  [大幅下跌]"
    print(trend)
    
    # 支撑/压力位
    print(f"\n  支撑/压力:")
    print(f"    支撑位1: {data['low']:.2f}")
    print(f"    阻力位1: {data['high']:.2f}")
    print(f"    5日均线: {(data['open'] + data['current'])/2:.2f} (估算)")
    
    # 综合分析
    print(f"\n【综合分析】")
    
    # 基于数据的分析
    if amplitude < 1:
        amplitude_desc = "振幅较小，市场观望情绪浓"
    elif amplitude < 3:
        amplitude_desc = "振幅适中，交易活跃度正常"
    else:
        amplitude_desc = "振幅较大，多空分歧明显"
    
    if data['change_pct'] > 0:
        direction = "多方略占优势"
    elif data['change_pct'] < 0:
        direction = "空方略占优势"
    else:
        direction = "多空力量平衡"
    
    print(f"  1. {amplitude_desc}")
    print(f"  2. {direction}")
    print(f"  3. 收盘价{('高于' if data['current'] > data['open'] else '低于')}开盘价，{'显示多方力量较强' if data['current'] > data['open'] else '显示空方压力较大'}")
    
    # 风险提示
    print(f"\n【风险提示】")
    if data['change_pct'] > 5:
        print(f"  ! 短期涨幅较大，注意回调风险")
    elif data['change_pct'] < -5:
        print(f"  ! 短期跌幅较大，注意止损风险")
    else:
        print(f"  = 走势相对平稳")
    
    # 建议
    print(f"\n【操作建议】")
    if data['change_pct'] > 3:
        print(f"  建议: 可考虑部分止盈，锁定利润")
    elif data['change_pct'] > 0:
        print(f"  建议: 可以继续持有，关注上方阻力位")
    elif data['change_pct'] > -3:
        print(f"  建议: 可考虑逢低吸纳，注意止损位")
    else:
        print(f"  建议: 建议止损观望，等待企稳")
    
    print("\n" + "="*65)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: analyze_stock.py <股票代码>")
        sys.exit(1)
    analyze(sys.argv[1])
