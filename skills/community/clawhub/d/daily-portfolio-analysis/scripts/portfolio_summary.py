#!/usr/bin/env python3
"""
持仓分析汇总脚本
从 portfolio.json 读取持仓配置，合并所有账户，按股票/市场/行业分析仓位占比
包含当日涨跌幅计算和实时汇率
"""

import json
import os
import sys
import urllib.request
from datetime import datetime
from futu import OpenQuoteContext, RET_OK

# 导入飞书通知模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from feishu_notifier import send_feishu_text_message

# 缓存文件路径
EXCHANGE_RATE_CACHE_PATH = os.path.expanduser("~/.openclaw/workspace/memory/exchange_rate_cache.json")

def load_portfolio():
    """加载持仓配置"""
    config_path = os.path.expanduser("~/.openclaw/workspace/memory/portfolio.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_rate_cache():
    """加载缓存的汇率数据"""
    if os.path.exists(EXCHANGE_RATE_CACHE_PATH):
        try:
            with open(EXCHANGE_RATE_CACHE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return None

def save_rate_cache(data):
    """保存汇率数据到缓存"""
    os.makedirs(os.path.dirname(EXCHANGE_RATE_CACHE_PATH), exist_ok=True)
    with open(EXCHANGE_RATE_CACHE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_exchange_rates():
    """从 Yahoo Finance API 获取实时汇率，带缓存和失败回退"""
    # 默认汇率
    default_usd_hkd = 7.85
    default_usd_cny = 7.25
    
    # 加载缓存
    cache = load_rate_cache()
    
    api_success = True
    warning_msg = None
    
    try:
        # Yahoo Finance 汇率代码
        # USD/HKD = USDHKD=X
        # USD/CNH (离岸人民币) = USDCNH=X
        
        # 获取 USD/HKD
        url_hkd = 'https://query1.finance.yahoo.com/v8/finance/chart/USDHKD=X?interval=1d&range=1d'
        req = urllib.request.Request(url_hkd, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        usd_hkd = None
        usd_hkd_prev = None
        if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
            result = data['chart']['result'][0]
            meta = result.get('meta', {})
            usd_hkd = meta.get('regularMarketPrice')
            usd_hkd_prev = meta.get('previousClose')
        
        # 获取 USD/CNH (离岸人民币，更接近港币市场的人民币汇率)
        url_cny = 'https://query1.finance.yahoo.com/v8/finance/chart/USDCNH=X?interval=1d&range=1d'
        req = urllib.request.Request(url_cny, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        usd_cny = None
        usd_cny_prev = None
        if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
            result = data['chart']['result'][0]
            meta = result.get('meta', {})
            usd_cny = meta.get('regularMarketPrice')
            usd_cny_prev = meta.get('previousClose')
        
        # 检查是否获取成功
        if usd_hkd is None or usd_cny is None:
            api_success = False
            warning_msg = "⚠️ Yahoo 汇率 API 部分获取失败"
            if usd_hkd is None:
                warning_msg += "（USD/HKD）"
            if usd_cny is None:
                warning_msg += "（USD/CNY）"
        
        # 如果 API 失败，使用缓存
        if not api_success and cache:
            warning_msg += f"，已使用缓存汇率（{cache.get('timestamp', '未知时间')})"
            usd_hkd = cache.get('usd_hkd', default_usd_hkd)
            usd_cny = cache.get('usd_cny', default_usd_cny)
            usd_hkd_prev = cache.get('usd_hkd_prev', usd_hkd)
            usd_cny_prev = cache.get('usd_cny_prev', usd_cny)
        elif not api_success:
            warning_msg += f"，使用默认汇率"
            usd_hkd = default_usd_hkd
            usd_cny = default_usd_cny
            usd_hkd_prev = usd_hkd
            usd_cny_prev = usd_cny
        
        # 计算 HKD/USD
        hkd_usd = 1 / usd_hkd
        
        # 计算汇率当日波动
        usd_hkd_change = ((usd_hkd - usd_hkd_prev) / usd_hkd_prev * 100) if usd_hkd_prev else 0
        usd_cny_change = ((usd_cny - usd_cny_prev) / usd_cny_prev * 100) if usd_cny_prev else 0
        
        # 保存缓存
        cache_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'usd_hkd': usd_hkd,
            'usd_cny': usd_cny,
            'usd_hkd_prev': usd_hkd_prev,
            'usd_cny_prev': usd_cny_prev,
            'hkd_usd': hkd_usd
        }
        save_rate_cache(cache_data)
        
        return hkd_usd, usd_cny, usd_hkd, usd_cny, usd_hkd_change, usd_cny_change, api_success, warning_msg
    
    except Exception as e:
        # API 调用失败
        if cache:
            warning_msg = f"⚠️ 汇率 API 连接失败：{e}，已使用缓存汇率（{cache.get('timestamp', '未知时间')})"
            usd_hkd = cache.get('usd_hkd', default_usd_hkd)
            usd_cny = cache.get('usd_cny', default_usd_cny)
            usd_hkd_prev = cache.get('usd_hkd_prev', usd_hkd)
            usd_cny_prev = cache.get('usd_cny_prev', usd_cny)
        else:
            warning_msg = f"⚠️ 汇率 API 连接失败：{e}，使用默认汇率"
            usd_hkd = default_usd_hkd
            usd_cny = default_usd_cny
            usd_hkd_prev = usd_hkd
            usd_cny_prev = usd_cny
        
        hkd_usd = 1 / usd_hkd
        usd_hkd_change = 0
        usd_cny_change = 0
        
        return hkd_usd, usd_cny, usd_hkd, usd_cny, usd_hkd_change, usd_cny_change, False, warning_msg

def get_us_price(symbol):
    """从 Yahoo API 获取美股股价和昨日收盘价"""
    ticker = symbol.replace('US.', '') if symbol.startswith('US.') else symbol
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=5m&range=1d'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
        if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
            meta = data['chart']['result'][0]['meta']
            price = meta.get('regularMarketPrice')
            prev_close = meta.get('previousClose')
            return price, prev_close
    except Exception as e:
        print(f'获取 {ticker} 失败：{e}')
    return None, None

def get_hk_price(code):
    """从富途 API 获取港股股价和昨日收盘价"""
    try:
        quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        ret_code, ret_data = quote_ctx.get_market_snapshot([code])
        quote_ctx.close()
        if ret_code == RET_OK and ret_data is not None and not ret_data.empty:
            price = float(ret_data['last_price'][0])
            prev_close = float(ret_data['prev_close_price'][0]) if 'prev_close_price' in ret_data else None
            return price, prev_close
    except Exception as e:
        print(f'获取 {code} 失败：{e}')
    return None, None

def merge_holdings(portfolio):
    """合并所有账户的持仓，按公司实际注册地/运营地分类"""
    merged = {}
    
    # 按公司实际归属地分类（不是按上市地点）
    # 中国公司：腾讯、拼多多、理想、美团、阿里、移动、电信、富途
    # 美国公司：Meta (Facebook)
    china_companies = ['腾讯控股', '拼多多', '理想汽车', '理想汽车-W', '美团-W', '阿里巴巴-W', 
                       '中国移动', '中国电信', '富途控股']
    
    for account_id, account in portfolio['accounts'].items():
        for symbol, holding in account['holdings'].items():
            name = holding['name']
            shares = holding['shares']
            market = holding['market']
            
            if name not in merged:
                merged[name] = {
                    'name': name,
                    'symbol': symbol,
                    'shares': 0,
                    'market': market,
                    # 按公司实际归属地，不是上市地点
                    'country': '中国' if name in china_companies else '美国',
                }
            
            merged[name]['shares'] += shares
    
    return merged

def generate_summary():
    """生成持仓分析汇总"""
    portfolio = load_portfolio()
    merged = merge_holdings(portfolio)
    
    # 获取实时汇率
    hkd_usd, usd_cny, usd_hkd, usd_cny_rate, usd_hkd_change, usd_cny_change, api_success, warning_msg = get_exchange_rates()
    
    # 显示汇率信息
    print()
    print('=' * 170)
    print(f"💱 实时汇率")
    print('=' * 170)
    
    # 汇率涨跌 emoji
    hkd_change_emoji = "📈" if usd_hkd_change > 0 else "📉" if usd_hkd_change < 0 else "➖"
    cny_change_emoji = "📈" if usd_cny_change > 0 else "📉" if usd_cny_change < 0 else "➖"
    
    print(f"  1 USD = {usd_hkd:.4f} HKD  {hkd_change_emoji} {usd_hkd_change:+.4f}% (当日)")
    print(f"  1 USD = {usd_cny_rate:.4f} CNY  {cny_change_emoji} {usd_cny_change:+.4f}% (当日)")
    print(f"  1 HKD = {hkd_usd:.6f} USD")
    
    if warning_msg:
        print(f"\n  {warning_msg}")
    
    print()
    
    # 获取股价并计算市值和当日涨跌
    for h in merged.values():
        if h['market'] == 'US':
            price, prev_close = get_us_price(h['symbol'])
            h['price'] = price
            h['prev_close'] = prev_close
            h['value_usd'] = price * h['shares'] if price else 0
            h['value_hkd'] = 0
            h['is_hk'] = False
            h['price_display'] = f'${price:.2f}' if price else 'N/A'
            
            # 计算当日涨跌
            if price and prev_close:
                h['change'] = (price - prev_close) * h['shares']
                h['change_pct'] = (price - prev_close) / prev_close * 100
            else:
                h['change'] = 0
                h['change_pct'] = 0
        else:
            price, prev_close = get_hk_price(h['symbol'])
            h['price'] = price
            h['prev_close'] = prev_close
            h['value_hkd'] = price * h['shares'] if price else 0
            h['value_usd'] = h['value_hkd'] * hkd_usd if price else 0
            h['is_hk'] = True
            h['price_display'] = f'HK${price:.2f}' if price else 'N/A'
            
            # 计算当日涨跌
            if price and prev_close:
                h['change_hkd'] = (price - prev_close) * h['shares']
                h['change_usd'] = h['change_hkd'] * hkd_usd
                h['change_pct'] = (price - prev_close) / prev_close * 100
            else:
                h['change_hkd'] = 0
                h['change_usd'] = 0
                h['change_pct'] = 0
    
    # 总市值
    total = sum(h['value_usd'] for h in merged.values() if h.get('price'))
    
    # 总当日涨跌
    total_change = sum(h.get('change_usd', h.get('change', 0)) for h in merged.values() if h.get('price'))
    
    # 输出表格
    print('=' * 170)
    print(f"{'股票':<14} {'持仓':<12} {'现价':<18} {'市值 (USD)':<16} {'市值 (HKD)':<18} {'当日涨跌':<16} {'占比':<8} {'国籍':<8}")
    print('=' * 170)
    
    for h in sorted(merged.values(), key=lambda x: x['value_usd'], reverse=True):
        if not h.get('price'):
            continue
        pct = (h['value_usd'] / total) * 100 if total > 0 else 0
        
        if h['is_hk']:
            value_hkd_str = f"HK${h['value_hkd']:>12,.2f}"
            change_str = f"HK${h['change_hkd']:>+12,.2f}" if h.get('change_hkd') else f"${h['change_usd']:>+12,.2f}"
        else:
            value_hkd_str = f"{'-':>18}"
            change_str = f"${h['change']:>+12,.2f}" if h.get('change') else 'N/A'
        
        # 涨跌 emoji
        if h['change_pct'] > 0:
            change_emoji = f"📈 {change_str} ({h['change_pct']:+.2f}%)"
        elif h['change_pct'] < 0:
            change_emoji = f"📉 {change_str} ({h['change_pct']:+.2f}%)"
        else:
            change_emoji = f"➖ {change_str} ({h['change_pct']:+.2f}%)"
        
        shares_str = f"{h['shares']:>8} 股"
        print(f"{h['name']:<14} {shares_str:<12} {h['price_display']:<18} ${h['value_usd']:>12,.2f}  {value_hkd_str}  {change_emoji:<28} {pct:>6.2f}%  {h['country']:<8}")
    
    print('=' * 170)
    
    # 计算人民币市值
    total_cny = total * usd_cny_rate
    total_change_cny = total_change * usd_cny_rate
    
    # 总涨跌
    if total_change > 0:
        total_change_emoji = f"🟢 +${total_change:,.2f}"
    elif total_change < 0:
        total_change_emoji = f"🔴 ${total_change:,.2f}"
    else:
        total_change_emoji = f"⚪ ${total_change:,.2f}"
    
    print('=' * 170)
    print(f"{'总市值':<36} {'USD':>12} ${total:>12,.2f}  {'CNY':>12} ¥{total_cny:>12,.2f}  {'HKD':>12} HK${total/usd_hkd:>12,.2f}")
    print(f"{'当日涨跌':<36} {total_change_emoji:>12}      {'CNY':>8} ¥{total_change_cny:>12,.2f}      {'HKD':>8} HK${total_change/usd_hkd:>12,.2f}")
    print('=' * 170)
    print()
    
    # 按国籍分类
    china = sum(h['value_usd'] for h in merged.values() if h.get('price') and h['country'] == '中国')
    us = sum(h['value_usd'] for h in merged.values() if h.get('price') and h['country'] == '美国')
    
    print('📈 按公司国籍分类')
    print('=' * 55)
    print(f"{'🇨🇳 中国公司':<22} ${china:>12,.2f}  {china/total*100:>6.2f}%")
    print(f"{'🇺🇸 美国公司':<22} ${us:>12,.2f}  {us/total*100:>6.2f}%")
    print(f"{'合计':<22} ${total:>12,.2f}  100.00%")
    print()
    
    # 按行业分类
    print('📊 按行业分类（估算）')
    print('=' * 55)
    
    industry_map = {
        '腾讯控股': '互联网',
        '拼多多': '电商',
        'Meta': '互联网',
        '理想汽车': '新能源汽车',
        '理想汽车-W': '新能源汽车',
        '美团-W': '互联网',
        '阿里巴巴-W': '互联网',
        '中国移动': '电信',
        '中国电信': '电信',
        '富途控股': '金融',
    }
    
    industries = {}
    for h in merged.values():
        if not h.get('price'):
            continue
        industry = industry_map.get(h['name'], '其他')
        if industry not in industries:
            industries[industry] = 0
        industries[industry] += h['value_usd']
    
    for industry, value in sorted(industries.items(), key=lambda x: x[1], reverse=True):
        pct = value / total * 100 if total > 0 else 0
        print(f"{industry:<20} ${value:>12,.2f}  {pct:>6.2f}%")

if __name__ == '__main__':
    import io
    from contextlib import redirect_stdout
    
    # 捕获输出
    f = io.StringIO()
    with redirect_stdout(f):
        generate_summary()
    
    report = f.getvalue()
    
    # 发送飞书消息
    success = send_feishu_text_message(report)
    
    if success:
        print("✅ 持仓分析汇总已发送")
    else:
        print("⚠️  飞书发送失败，报告内容如下：")
        print(report)
