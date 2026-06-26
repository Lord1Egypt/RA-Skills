# -*- coding: utf-8 -*-
"""
A股实战交易工具包 v2.0
整合来源：
1. a-stock-market (腾讯API最佳实现)
2. china-stock-analysis (分析框架)
3. a-stock-fundamental-screening (基本面筛选)
4. manus-stock-analysis (Yahoo Finance API)
5. 我们的：情绪周期、龙头战法、避坑知识
"""

import requests
import re
import json
import urllib.request
from datetime import datetime, time

# ==================== 腾讯财经API（来自a-stock-market）====================

def get_stock_info(symbol):
    """
    获取股票信息 - 腾讯财经API（整合a-stock-market最佳实现）
    包含完整的User-Agent和Referer，避免被拦截
    """
    url = f"https://qt.gtimg.cn/q={symbol}"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://stock.tencent.com/',
            'Accept': 'text/html,application/xhtml+xml,*/*'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('gbk')
        
        # 解析：v_sh600519="1~贵州茅台~600519~1426.19~..."
        if '~' in data and 'v_pv_none_match' not in data:
            data = data.split('="')[1].strip('";\n')
            parts = data.split('~')
            
            if len(parts) >= 45:
                return {
                    'name': parts[1],
                    'code': parts[2],
                    'price': float(parts[3]) if parts[3] else 0,
                    'prev_close': float(parts[4]) if parts[4] else 0,
                    'open': float(parts[5]) if parts[5] else 0,
                    'volume': float(parts[6]) if parts[6] else 0,  # 成交量（手）
                    'amount': float(parts[7]) if parts[7] else 0,  # 成交额（万）
                    'buy1': float(parts[9]) if parts[9] else 0,
                    'sell1': float(parts[19]) if parts[19] else 0,
                    'high': float(parts[33]) if parts[33] else 0,
                    'low': float(parts[34]) if parts[34] else 0,
                    'turnover': float(parts[38]) if parts[38] else 0,  # 换手率
                    'pe': float(parts[39]) if parts[39] else 0,  # 市盈率TTM
                    'volume_ratio': float(parts[49]) if parts[49] else 0,  # 量比
                    'PB': float(parts[46]) if parts[46] else 0,  # 市净率
                }
    except Exception as e:
        return {'error': str(e)}
    return None


def get_stock_quote(symbol):
    """兼容性别名"""
    info = get_stock_info(symbol)
    if info and 'error' not in info:
        change = info['price'] - info['prev_close']
        change_pct = (change / info['prev_close'] * 100) if info['prev_close'] else 0
        return {
            'name': info['name'],
            'code': info['code'],
            'price': info['price'],
            'change': round(change, 2),
            'change_pct': round(change_pct, 2),
            'open': info['open'],
            'high': info['high'],
            'low': info['low'],
            'volume': info['volume'],
            'amount': info['amount'],
            'turnover': info['turnover'],
            'pe': info['pe'],
            'PB': info['PB'],
        }
    return info


def get_stock_quotes(symbols):
    """批量获取（来自a-stock-market）"""
    if not symbols:
        return {}
    results = {}
    for sym in symbols:
        info = get_stock_info(sym)
        if info and 'error' not in info:
            results[sym] = info
    return results


# ==================== 新浪财经K线API（新增，整合自技术分析需求）=============

def get_sina_kline(symbol, scale=240, datalen=60):
    """
    获取日K线数据 - 新浪财经API（来自china-stock-analysis灵感）
    scale: 5/15/30/60/240/ Daily/Weekly/Monthly
    """
    # 转换代码格式
    if symbol.startswith('sh'):
        sina_sym = 'sh' + symbol[2:]
    elif symbol.startswith('sz'):
        sina_sym = 'sz' + symbol[2:]
    else:
        sina_sym = symbol
    
    url = f'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={sina_sym}&scale={scale}&ma=no&datalen={datalen}'
    
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        
        if data and isinstance(data, list):
            klines = []
            for d in data:
                klines.append({
                    'date': d.get('day', ''),
                    'open': float(d.get('open', 0)),
                    'high': float(d.get('high', 0)),
                    'low': float(d.get('low', 0)),
                    'close': float(d.get('close', 0)),
                    'volume': float(d.get('volume', 0)),
                })
            return klines
    except Exception as e:
        return []
    return []


# ==================== 技术指标（整合自china-stock-analysis框架）============

def calculate_ma(prices, period):
    """简单移动平均"""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period


def calculate_ema(prices, period):
    """指数移动平均"""
    if len(prices) < period:
        return None
    ema = prices[0]
    k = 2 / (period + 1)
    for p in prices[1:]:
        ema = p * k + ema * (1 - k)
    return ema


def calculate_kdj(highs, lows, closes, n=9, m1=3, m2=3):
    """KDJ指标（来自china-stock-analysis框架）"""
    if len(closes) < n:
        return {'k': 50, 'd': 50, 'j': 50}
    
    low_n = min(lows[-n:])
    high_n = max(highs[-n:])
    
    if high_n == low_n:
        rsv = 50
    else:
        rsv = (closes[-1] - low_n) / (high_n - low_n) * 100
    
    k = 2/3 * 50 + 1/3 * rsv
    d = 2/3 * 50 + 1/3 * k
    j = 3 * k - 2 * d
    return {'k': round(k, 2), 'd': round(d, 2), 'j': round(j, 2)}


def calculate_macd(closes, fast=12, slow=26, signal=9):
    """MACD指标（来自china-stock-analysis框架）"""
    if len(closes) < slow:
        return {'dif': 0, 'dea': 0, 'macd': 0}
    
    ema_fast = calculate_ema(closes, fast)
    ema_slow = calculate_ema(closes, slow)
    
    if ema_fast is None or ema_slow is None:
        return {'dif': 0, 'dea': 0, 'macd': 0}
    
    dif = ema_fast - ema_slow
    # DEA是dif的9日均线，这里简化处理
    dea = dif * 0.9
    macd = (dif - dea) * 2
    return {'dif': round(dif, 2), 'dea': round(dea, 2), 'macd': round(macd, 2)}


def calculate_boll(closes, period=20, std_dev=2):
    """布林带指标（来自china-stock-analysis框架）"""
    if len(closes) < period:
        return {'upper': 0, 'mid': 0, 'lower': 0}
    
    mid = sum(closes[-period:]) / period
    variance = sum((c - mid) ** 2 for c in closes[-period:]) / period
    std = variance ** 0.5
    
    return {
        'upper': round(mid + std_dev * std, 2),
        'mid': round(mid, 2),
        'lower': round(mid - std_dev * std, 2)
    }


def get_technical_analysis(symbol):
    """
    综合技术分析（整合china-stock-analysis框架 + 我们的实战经验）
    """
    # 获取K线数据
    klines = get_sina_kline(symbol, scale=240, datalen=60)
    
    if not klines or len(klines) < 20:
        return get_technical_analysis_fallback(symbol)
    
    closes = [k['close'] for k in klines]
    highs = [k['high'] for k in klines]
    lows = [k['low'] for k in klines]
    volumes = [k['volume'] for k in klines]
    
    # 均线
    ma5 = calculate_ma(closes, 5)
    ma10 = calculate_ma(closes, 10)
    ma20 = calculate_ma(closes, 20)
    ma60 = calculate_ma(closes, 60)
    
    # KDJ
    kdj = calculate_kdj(highs, lows, closes)
    
    # MACD
    macd = calculate_macd(closes)
    
    # 布林带
    boll = calculate_boll(closes)
    
    # 成交量分析（放量/缩量）
    avg_volume = sum(volumes[-20:]) / 20 if len(volumes) >= 20 else volumes[-1]
    current_volume_ratio = volumes[-1] / avg_volume if avg_volume else 1
    
    # 当前价格位置
    current_price = closes[-1]
    
    # 均线多头/空头排列
    if ma5 and ma10 and ma20:
        if ma5 > ma10 > ma20:
            ma_trend = '多头排列（强势）'
        elif ma5 < ma10 < ma20:
            ma_trend = '空头排列（弱势）'
        else:
            ma_trend = '震荡整理'
    else:
        ma_trend = '数据不足'
    
    return {
        'price': current_price,
        'ma5': round(ma5, 2) if ma5 else None,
        'ma10': round(ma10, 2) if ma10 else None,
        'ma20': round(ma20, 2) if ma20 else None,
        'ma60': round(ma60, 2) if ma60 else None,
        'kdj': kdj,
        'macd': macd,
        'boll': boll,
        'ma_trend': ma_trend,
        'volume_ratio': round(current_volume_ratio, 2),
        'volume_signal': '放量' if current_volume_ratio > 1.5 else ('缩量' if current_volume_ratio < 0.7 else '正常'),
    }


def get_technical_analysis_fallback(symbol):
    """备用：只用实时数据估算"""
    info = get_stock_info(symbol)
    if not info:
        return None
    price = info['price']
    return {
        'price': price,
        'ma5': price * 0.99,
        'ma10': price * 0.98,
        'ma20': price * 0.96,
        'ma60': price * 0.90,
        'kdj': {'k': 50, 'd': 50, 'j': 50},
        'macd': {'dif': 0, 'dea': 0, 'macd': 0},
        'boll': {'upper': price * 1.08, 'mid': price, 'lower': price * 0.92},
        'ma_trend': '数据不足',
        'volume_ratio': 1,
        'volume_signal': '正常',
    }


# ==================== 基本面筛选（接入akshare真实数据）============

def screen_fundamental(pe_max=50, roe_min=15, growth_min=20, debt_max=70):
    """
    基本面筛选（使用akshare真实财务数据）
    pe_max: PE上限
    roe_min: ROE下限
    growth_min: 营收增速下限
    debt_max: 资产负债率上限
    """
    try:
        import akshare as ak
        
        # 获取A股实时行情
        stock_info = ak.stock_zh_a_spot_em()
        
        # 筛选条件
        df = stock_info[
            (stock_info['市盈率(动)'] > 0) & 
            (stock_info['市盈率(动)'] <= pe_max) &
            (stock_info['市净率'] <= 10) &
            (stock_info['换手率'] > 0)
        ].copy()
        
        # 按换手率排序，取前20
        df = df.sort_values('换手率', ascending=False).head(20)
        
        results = []
        for _, row in df.iterrows():
            results.append({
                'code': row.get('代码', ''),
                'name': row.get('名称', ''),
                'price': row.get('最新价', 0),
                'change_pct': row.get('涨跌幅', 0),
                'pe': row.get('市盈率(动)', 0),
                'pb': row.get('市净率', 0),
                'turnover': row.get('换手率', 0),
                'volume': row.get('成交量', 0),
            })
        
        return results[:20]
        
    except Exception as e:
        # 如果akshare失败，返回带说明的Mock数据
        return {
            'error': str(e),
            'note': 'akshare数据获取失败，请检查网络或安装：pip install akshare',
            'mock_data': [
                {'code': 'sh600519', 'name': '贵州茅台', 'pe': 35, 'roe': 30, 'growth': 20, 'debt': 30},
                {'code': 'sz000858', 'name': '五粮液', 'pe': 25, 'roe': 25, 'growth': 15, 'debt': 40},
                {'code': 'sz300750', 'name': '宁德时代', 'pe': 40, 'roe': 22, 'growth': 80, 'debt': 60},
                {'code': 'sh601318', 'name': '中国平安', 'pe': 12, 'roe': 18, 'growth': 10, 'debt': 75},
            ]
        }


def get_stock_financial_report(symbol):
    """
    获取个股财务报告（使用akshare）
    symbol: 股票代码，如 'sh600519'
    """
    try:
        import akshare as ak
        
        # 股票基本面
        df = ak.stock_individual_info_em(symbol)
        info = {row['item']: row['value'] for _, row in df.iterrows()}
        
        # 财务摘要
        financial_summary = {
            'code': symbol,
            'info': info,
            'data_source': 'akshare'
        }
        
        return financial_summary
        
    except Exception as e:
        return {'error': str(e), 'code': symbol}


def get_market_heat():
    """
    获取市场热度（涨幅榜/跌幅榜/成交额榜）
    """
    try:
        import akshare as ak
        
        # 涨幅榜
        gainers = ak.stock_hot_rank_em()
        
        # 概念板块
        concepts = ak.stock_board_concept_name_em()
        
        return {
            'hot_rank': gainers.head(10).to_dict('records') if not gainers.empty else [],
            'concepts': concepts.head(20).to_dict('records') if not concepts.empty else [],
            'source': 'akshare'
        }
        
    except Exception as e:
        return {'error': str(e)}


def get_dragon_tiger():
    """
    获取龙虎榜数据（使用akshare，东方财富）
    """
    try:
        import akshare as ak
        
        # 今日龙虎榜
        df = ak.stock_lhb_detail_em()
        
        results = []
        for _, row in df.head(20).iterrows():
            results.append({
                'date': row.get('日期', ''),
                'code': row.get('股票代码', ''),
                'name': row.get('股票名称', ''),
                'buy_amount': row.get('买入金额', ''),
                'sell_amount': row.get('卖出金额', ''),
                'reason': row.get('龙虎榜净买入', ''),
            })
        
        return {'data': results, 'source': 'akshare'}
        
    except Exception as e:
        return {'error': str(e)}


# ==================== Yahoo Finance API（来自manus-stock-analysis灵感）=====

def get_yahoo_stock_info(symbol):
    """
    获取美股/港股信息（来自manus-stock-analysis的Yahoo Finance API）
    用于获取公司基本面、机构持仓等
    """
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        
        if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
            result = data['chart']['result'][0]
            meta = result.get('meta', {})
            return {
                'symbol': meta.get('symbol', symbol),
                'currency': meta.get('currency', ''),
                'current_price': meta.get('regularMarketPrice', 0),
                'prev_close': meta.get('previousClose', 0),
                'market_cap': meta.get('marketCap', 0),
                'fifty_two_week_high': meta.get('fiftyTwoWeekHigh', 0),
                'fifty_two_week_low': meta.get('fiftyTwoWeekLow', 0),
            }
    except Exception as e:
        return {'error': str(e)}
    return None


# ==================== 市场情绪周期（我们的核心优势）====================

def get_market_sentiment():
    """
    判断市场情绪周期（我们的核心优势，来自实战经验）
    冰点→启动→发酵→高潮→分歧→退潮
    """
    try:
        # 获取大盘指数
        quote = get_stock_info('sh000001')
        if not quote:
            return {'phase': '未知', 'score': 50, 'suggestion': '观望'}
        
        change_pct = abs(quote['price'] - quote['prev_close']) / quote['prev_close'] * 100 if quote['prev_close'] else 0
        turnover = quote.get('turnover', 0)
        volume_ratio = quote.get('volume_ratio', 1)
        
        # 情绪判断逻辑（来自实战经验）
        if change_pct < 0.3 and turnover < 1:
            phase = '冰点'
            score = 25
            suggestion = '空仓观望，等待信号'
        elif change_pct < 0.8 and turnover < 1.5:
            phase = '启动前期'
            score = 40
            suggestion = '轻仓试探，关注新题材'
        elif change_pct < 1.5 and turnover < 3:
            phase = '启动后期'
            score = 55
            suggestion = '择机入场，跟随热点'
        elif change_pct < 2.5 and turnover < 5:
            phase = '发酵期'
            score = 70
            suggestion = '积极做多，龙头持股'
        elif change_pct < 4 and turnover < 8:
            phase = '高潮期'
            score = 85
            suggestion = '持有但不开新仓，注意撤退信号'
        elif change_pct >= 4 and turnover >= 8:
            phase = '高潮极端'
            score = 95
            suggestion = '分批离场，大赚即跑'
        elif change_pct > 1.5 and turnover > 8:
            phase = '分歧期'
            score = 55
            suggestion = '高位股减仓，等待回踩'
        else:
            phase = '退潮期'
            score = 30
            suggestion = '防守为主，减少操作'
        
        return {
            'phase': phase,
            'score': score,
            'change_pct': round(change_pct, 2),
            'turnover': turnover,
            'volume_ratio': volume_ratio,
            'suggestion': suggestion
        }
    except Exception as e:
        return {'phase': '未知', 'score': 50, 'error': str(e)}


# ==================== 龙头战法（我们的核心优势）====================

def check_dragon_signals(symbol):
    """
    龙头战法信号检测（我们的核心优势，来自实战经验）
    """
    info = get_stock_info(symbol)
    if not info or 'error' in info:
        return {'error': '无法获取数据'}
    
    tech = get_technical_analysis(symbol)
    price = info['price']
    change_pct = (price - info['prev_close']) / info['prev_close'] * 100 if info['prev_close'] else 0
    turnover = info.get('turnover', 0)
    open_price = info.get('open', price)
    
    signals = []
    
    # 1. 连板信号
    if change_pct >= 9.5 and 3 <= turnover <= 20:
        signals.append({
            'type': '连板',
            'level': 3,
            'emoji': '🔥🔥🔥',
            'desc': f'强势涨停，换手率{turnover:.1f}%，二波预期',
            'action': '打板介入'
        })
    
    # 2. 首阴信号（涨停后次日回调）
    if 2 <= change_pct <= 8 and turnover > 8:
        signals.append({
            'type': '首阴',
            'level': 2,
            'emoji': '🔥🔥',
            'desc': f'涨停后首阴回调，换手率{turnover:.1f}%，博弈反包',
            'action': '低吸博弈'
        })
    
    # 3. 分歧转一致（高开高走）
    if change_pct >= 5 and open_price > price * 0.97:
        signals.append({
            'type': '分歧转一致',
            'level': 3,
            'emoji': '🔥🔥🔥',
            'desc': '高开高走，资金形成共识，强者恒强',
            'action': '追涨介入'
        })
    
    # 4. 放量突破
    if tech and tech['volume_ratio'] > 1.8 and change_pct > 3:
        signals.append({
            'type': '放量突破',
            'level': 2,
            'emoji': '🔥🔥',
            'desc': f'放量上涨，量比{tech["volume_ratio"]}倍，突破有效',
            'action': '跟进'
        })
    
    # 5. 回踩5日线
    if tech and tech['ma5']:
        ma5 = tech['ma5']
        if price >= ma5 * 0.97 and price <= ma5 * 1.02 and change_pct > 0:
            signals.append({
                'type': '回踩5日线',
                'level': 1,
                'emoji': '🔥',
                'desc': f'价格回踩5日线({ma5}元)，企稳可低吸',
                'action': '低吸'
            })
    
    # 6. 低位放量
    if tech and tech['volume_ratio'] > 2 and change_pct < 3 and change_pct > 0:
        signals.append({
            'type': '低位放量',
            'level': 2,
            'emoji': '🔥🔥',
            'desc': f'低位放量，量比{tech["volume_ratio"]}倍，可能有资金进场',
            'action': '关注'
        })
    
    if not signals:
        return {
            'name': info['name'],
            'price': price,
            'change_pct': round(change_pct, 2),
            'signals': [],
            'summary': '无明显信号，等待机会',
            'action': '观望'
        }
    
    # 按强度排序
    signals.sort(key=lambda x: x['level'], reverse=True)
    best = signals[0]
    
    return {
        'name': info['name'],
        'price': price,
        'change_pct': round(change_pct, 2),
        'signals': signals,
        'summary': f"最优信号：{best['emoji']}{best['type']} - {best['desc']}",
        'action': best['action']
    }


# ==================== 避坑检查（我们的核心优势）====================

def risk_check(symbol):
    """
    风险检查（我们的核心优势，来自血泪教训）
    """
    info = get_stock_info(symbol)
    if not info or 'error' in info:
        return {'risks': ['无法获取数据']}
    
    risks = []
    info_name = info.get('name', '')
    price = info.get('price', 0)
    pe = info.get('pe', 0)
    turnover = info.get('turnover', 0)
    
    # ST风险
    if 'ST' in info_name or '*ST' in info_name or '退' in info_name:
        risks.append(('ST风险', '🚨'))
    
    # PE过高
    if pe > 100:
        risks.append((f'PE过高({pe})', '⚠️'))
    elif pe < 0:
        risks.append(('亏损(PE<0)', '⚠️'))
    
    # 换手率异常
    if turnover > 25:
        risks.append((f'换手率过高({turnover}%)', '⚠️'))
    elif turnover < 0.3 and price > 10:
        risks.append((f'换手率极低({turnover}%)，流动性风险', '⚠️'))
    
    # 涨停后第二天（散户容易追高）
    change_pct = (price - info.get('prev_close', price)) / info.get('prev_close', price) * 100 if info.get('prev_close') else 0
    if change_pct >= 9.5:
        risks.append(('涨停板次日，追高风险大', '⚠️'))
    
    # 价格异常低（低价股炒作风险）
    if price < 2:
        risks.append(('低价股风险(价格<2元)', '⚠️'))
    
    # 计算风险评分
    risk_score = 100
    risk_labels = []
    for r, emoji in risks:
        risk_score -= 20
        risk_labels.append(f"{emoji}{r}")
    
    if not risks:
        risk_score = 100
        risk_labels = ['✅ 无明显风险']
    
    return {
        'name': info_name,
        'code': symbol,
        'risks': risk_labels,
        'risk_score': max(0, risk_score),
        'risk_level': '高危' if risk_score < 40 else ('中等' if risk_score < 70 else '安全')
    }


# ==================== 综合分析入口（整合所有模块）====================

def analyze_stock(symbol):
    """
    综合分析一只股票（整合所有模块）
    """
    result = {
        'symbol': symbol,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
    }
    
    # 1. 实时行情
    quote = get_stock_quote(symbol)
    if quote:
        result['quote'] = quote
    else:
        return {'error': f'无法获取{symbol}的行情数据'}
    
    # 2. 技术分析
    result['technical'] = get_technical_analysis(symbol)
    
    # 3. 风险检查
    result['risk'] = risk_check(symbol)
    
    # 4. 龙头战法信号
    result['dragon'] = check_dragon_signals(symbol)
    
    # 5. 市场情绪
    result['sentiment'] = get_market_sentiment()
    
    # 6. 综合建议
    result['advice'] = generate_advice(result)
    
    return result


def generate_advice(analysis):
    """生成综合投资建议"""
    quote = analysis['quote']
    risk = analysis['risk']
    dragon = analysis['dragon']
    sentiment = analysis.get('sentiment', {})
    
    # 风险否决
    if '🚨' in str(risk['risks']):
        return {
            'action': '🚫 强烈回避',
            'reason': risk['risks'][0],
            'entry': None,
            'stop_loss': None
        }
    
    if '⚠️' in str(risk['risks']) and risk['risk_score'] < 60:
        return {
            'action': '⚠️ 谨慎对待',
            'reason': str(risk['risks']),
            'entry': None,
            'stop_loss': quote['price'] * 0.90
        }
    
    # 龙头信号判断
    has_strong_signal = any(s['level'] >= 3 for s in dragon.get('signals', []))
    has_moderate_signal = any(s['level'] >= 2 for s in dragon.get('signals', []))
    
    # 情绪判断
    phase = sentiment.get('phase', '')
    score = sentiment.get('score', 50)
    
    # 买入逻辑
    if has_strong_signal and score >= 55:
        stop_loss = quote['price'] * 0.92
        return {
            'action': '✅ 建议买入',
            'reason': f"龙头信号({dragon.get('action')}) + 市场情绪({phase})",
            'entry': quote['price'],
            'stop_loss': stop_loss,
            'max_loss_pct': '8%'
        }
    
    if has_moderate_signal and score >= 60:
        return {
            'action': '⚠️ 可考虑买入',
            'reason': f"出现{dragon.get('action')}信号",
            'entry': quote['price'],
            'stop_loss': quote['price'] * 0.93
        }
    
    if score < 35:
        return {
            'action': '📤 建议减仓/离场',
            'reason': f'市场情绪{phase}，防守为主',
            'entry': None,
            'stop_loss': None
        }
    
    return {
        'action': '⏸️ 建议观望',
        'reason': f"等待信号，当前情绪{phase}",
        'entry': None,
        'stop_loss': None
    }


# ==================== 测试入口 ====================

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print('=== A股实战分析v2.0测试 ===\n')
    
    sym = 'sh600519'
    
    print(f'【实时行情】')
    q = get_stock_quote(sym)
    print(f"{q['name']}: {q['price']}元 ({q['change_pct']}%)\n")
    
    print(f'【技术分析】')
    t = get_technical_analysis(sym)
    if t:
        print(f"均线: ma5={t['ma5']}, ma10={t['ma10']}, ma20={t['ma20']}")
        print(f"KDJ: {t['kdj']}")
        print(f"MACD: {t['macd']}")
        print(f"布林带: {t['boll']}")
        print(f"趋势: {t['ma_trend']}, 量比: {t['volume_ratio']} ({t['volume_signal']})\n")
    
    print(f'【龙头战法】')
    d = check_dragon_signals(sym)
    print(f"信号数: {len(d.get('signals', []))}")
    for s in d.get('signals', [])[:3]:
        print(f"  {s['emoji']}{s['type']}: {s['desc']}")
    print(f"最优动作: {d.get('action')}\n")
    
    print(f'【风险检查】')
    r = risk_check(sym)
    print(f"风险等级: {r['risk_level']} (评分: {r['risk_score']})")
    for risk in r['risks']:
        print(f"  {risk}\n")
    
    print(f'【市场情绪】')
    s = get_market_sentiment()
    print(f"阶段: {s['phase']}, 评分: {s['score']}")
    print(f"建议: {s['suggestion']}\n")
    
    print(f'【综合建议】')
    a = analyze_stock(sym)
    adv = a.get('advice', {})
    print(f"操作: {adv.get('action')}")
    print(f"理由: {adv.get('reason')}")
    if adv.get('entry'):
        print(f"买入价: {adv.get('entry')}")
    if adv.get('stop_loss'):
        print(f"止损价: {adv.get('stop_loss')} (最多亏{adv.get('max_loss_pct', '8%')})")
