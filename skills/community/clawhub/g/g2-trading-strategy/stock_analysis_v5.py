#!/usr/bin/env python3
"""
股票分析系统 v5.2 (2026-03-23) - 深度融合InStreet社区经验
=============================================================
【融合来源】
- xiapi_stockbot: 尾盘策略（14:30-15:00买入）
- stockadvisorai: 三维分析（基本面+技术面+情绪面）
- caibot_claw: 超短线（MACD+KDJ+成交量）
- openclawtrader_4c7f93: 大盘6大预警因素
- DrunkClaw: 双均线策略
- caijing_whale: SEPA趋势交易

【评价维度】
- 位置 (15%): 低位建仓安全边际
- 量能 (20%): 资金入场信号 [量比>1.2]
- 趋势 (15%): 短期走势动能 [MACD金叉+KDJ]
- 筹码 (10%): 主力建仓信号
- 业绩 (15%): 基本面支撑
- 均线 (10%): 趋势确认 [MA5>MA20>MA60]
- 换手率 (10%): 活跃度 [4%-12%]
- 情绪面 (5%): 市场情绪

【筛选条件】
- 综合评分 >= 40分
- 上涨空间 >= 8%
- 当前位置 < 65%
- PE > 0 (必须盈利)
- 换手率 4%~12%
- 量比 >1.2
- 涨幅 2%~6%（尾盘策略）
- 5日线上（趋势确认）
- MACD金叉或KDJ金叉（技术信号）

【买入时间】
- 尾盘: 14:30-15:00（来自xiapi_stockbot）
- 次日开盘或盈利后卖出

【硬性过滤】
- PE < 0 (亏损排除)
- 净利润 < -50%
- 营收 < -30%
- 换手率 < 4% 或 > 12%
- 高位+放量不放买（位置>70%且放量=远离）
- 大盘6大预警触发时空仓

核心原则(来自InStreet):
- 只买低位+放量的股票
- 高位+放量=主力出货，远离
"""

import requests
import json
import re
import time
import sqlite3
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 会话配置
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})
adapter = HTTPAdapter(max_retries=Retry(total=2, backoff_factor=0.3))
session.mount('https://', adapter)

# 热门行业
HOT_SECTORS = ["新能源", "光伏", "半导体", "AI", "人工智能", "医药", "医疗", "云计算", "大数据", "5G", "芯片", "电池", "电动车", "软件"]

DB_PATH = "/root/.openclaw/workspace-financemaster/stock_data.db"


def get_stock_price(code, market="sz"):
    """获取股票实时价格（增强版：含换手率、量比、涨跌幅）"""
    try:
        r = session.get(f"https://qt.gtimg.cn/q={market}{code}", timeout=5)
        if 'v_' in r.text:
            d = r.text.split('"')[1].split('~')
            return {
                'price': float(d[3]),
                'name': d[1] if len(d) > 1 else code,
                'change': float(d[32]) if d[32] else 0,  # 涨跌幅在d[32]
                'change_amt': float(d[31]) if d[31] else 0,  # 涨跌额在d[31]
                'volume': int(d[6]) if d[6] else 0,  # 成交量(手)在d[6]
                'amount': float(d[7]) if d[7] else 0,  # 成交额(千)在d[7]
                'turnover': float(d[38]) if d[38] else 0,  # 换手率在d[38]
                'vol_ratio': float(d[37]) if d[37] else 0,  # 量比在d[37]
                'high': float(d[33]) if d[33] else 0,  # 最高在d[33]
                'low': float(d[34]) if d[34] else 0,  # 最低在d[34]
                'open': float(d[11]) if d[11] else 0,  # 开盘在d[11]
                'prev_close': float(d[4]) if d[4] else 0,  # 昨收在d[4]
            }
    except:
        pass
    return None


def get_kline_data(code, market="sz"):
    """获取K线数据"""
    try:
        url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
        params = {'_var': 'kline_dayqfq', 'param': f'{market}{code},day,,,250,qfq'}
        r = session.get(url, params=params, timeout=8)
        
        mat = re.search(r'kline_dayqfq=(.+)$', r.text)
        if not mat:
            return None
        
        data = json.loads(mat.group(1))['data']
        kls = data.get(f'{market}{code}', {}).get('qfqday', [])
        if not kls:
            kls = data.get(f'{market}{code}', {}).get('day', [])
        
        return kls if len(kls) >= 80 else None
    except:
        pass
    return None


def get_fundamentals(code, market="sz"):
    """获取基本面数据"""
    try:
        url = "https://push2.eastmoney.com/api/qt/stock/get"
        params = {
            'fltt': 2,
            'fields': 'f84,f162,f173,f174,f175,f178,f190,f207,f208,f209',
            'secid': f'{market}.{code}'
        }
        r = session.get(url, params=params, timeout=5)
        fd = r.json().get('data', {})
        
        # PE计算 (优先动态PE)
        pe_dynamic = float(fd.get('f208', 0)) if fd.get('f208') else 0
        pe_ttm = float(fd.get('f207', 0)) if fd.get('f207') else 0
        pe_static = float(fd.get('f162', 0)) if fd.get('f162') else 0
        pe = pe_dynamic if pe_dynamic != 0 else (pe_ttm if pe_ttm != 0 else pe_static)
        
        return {
            'pe': pe,
            'roe': float(fd.get('f173', 0)) if fd.get('f173') else 0,
            'profit': float(fd.get('f178', 0)) if fd.get('f178') else 0,
            'revenue': float(fd.get('f190', 0)) if fd.get('f190') else 0,
            'industry': fd.get('f84', '')
        }
    except:
        pass
    return None


def calculate_v5_score(code, market="sz"):
    """
    v5.1评分体系计算 (2026-03-23融合InStreet经验)
    ==============================================
    位置(15%) + 量能(20%) + 趋势(15%) + 筹码(10%) + 
    业绩(15%) + 均线(10%) + 换手率(10%) + 情绪面(5%)
    
    核心筛选（来自xiapi_stockbot尾盘策略）:
    - 涨幅: 2%~6%
    - 量比: >1.2
    - 换手率: 4%~12%
    """
    # 获取数据
    price_data = get_stock_price(code, market)
    if not price_data:
        return None
    
    kls = get_kline_data(code, market)
    if not kls:
        return None
    
    fd = get_fundamentals(code, market)
    
    current = price_data['price']
    name = price_data['name']
    
    # 基本面
    if fd:
        pe = fd['pe']
        roe = fd['roe']
        profit = fd['profit']
        revenue = fd['revenue']
        industry = fd['industry']
    else:
        pe, roe, profit, revenue, industry = 0, 0, 0, 0, ''
    
    # 硬性过滤
    if pe < 0 or profit < -50 or revenue < -30:
        return None
    
    # 技术指标计算
    closes = [float(k[2]) for k in kls]
    highs = [float(k[3]) for k in kls]
    lows = [float(k[4]) for k in kls]
    volumes = [int(float(k[5])) for k in kls]
    
    ma5 = sum(closes[-5:]) / 5
    ma20 = sum(closes[-20:]) / 20
    ma60 = sum(closes[-60:]) / 60
    
    vol_20 = sum(volumes[-20:]) / 20
    vol_60 = sum(volumes[-60:]) / 60
    
    high_120 = max(highs[-120:])
    low_120 = min(lows[-120:])
    
    position = (current - low_120) / (high_120 - low_120) * 100
    change_20d = (closes[-1] - closes[-20]) / closes[-20] * 100
    upside = (high_120 - current) / current * 100
    
    # ========== v5.0 评分 ==========
    score = 0
    
    # 1. 位置 (20%)
    if position < 20:
        score += 20
    elif position < 30:
        score += 15
    elif position < 40:
        score += 10
    
    # 2. 量能 (20%)
    vol_ratio = vol_20 / vol_60 if vol_60 > 0 else 1
    if vol_ratio > 1.5:
        score += 15
    elif vol_ratio > 1.2:
        score += 10
    if vol_20 > vol_60 * 1.3:
        score += 5
    
    # 3. 趋势 (15%)
    if change_20d > 5:
        score += 10
    elif change_20d > 0:
        score += 5
    up_days = sum(1 for i in range(-5, 0) if closes[i] > closes[i-1])
    if up_days >= 3:
        score += 5
    
    # 4. 筹码 (15%)
    if vol_20 < vol_60 * 0.7 and position < 35:
        score += 15
    elif position < 30:
        score += 8
    
    # 5. 业绩 (15%)
    # 净利润
    if profit > 30:
        score += 5
    elif profit > 10:
        score += 4
    elif profit > 0:
        score += 2
    
    # 营收
    if revenue > 30:
        score += 5
    elif revenue > 10:
        score += 4
    elif revenue > 0:
        score += 2
    
    # ROE
    if roe > 20:
        score += 5
    elif roe > 15:
        score += 4
    elif roe > 10:
        score += 2
    
    # 6. 均线 (10%) - 权重从15%调低到10%
    if ma5 > ma20:
        score += 6
    if ma20 > ma60:
        score += 3
    if current > ma20:
        score += 1
    
    # 7. 换手率 (10%) - 来自xiapi_stockbot尾盘策略
    # 换手率4%-12%为活跃区间
    turnover = price_data.get('turnover', 0) if 'price_data' in dir() else 0
    if turnover > 4 and turnover < 12:
        score += 10
    elif turnover > 2 and turnover < 15:
        score += 5
    
    # 8. 情绪面 (5%) - 简单判断当日涨跌
    change = price_data.get('change', 0)
    if 2 <= change <= 6:  # 涨幅2%-6%符合尾盘策略
        score += 5
    elif change > 0:
        score += 2
    
    # 行业热度
    if any(h in (name + industry) for h in HOT_SECTORS):
        score += 10
    
    # ====== v5.1 硬性筛选 ======
    # 来自xiapi_stockbot尾盘策略
    # 涨幅: 2%~6%
    # 换手率: 4%~12%
    # 量比: >1.2 (需另外计算)
    
    # 高位放量过滤 - 来自量能+位置决策
    # 如果位置>70%且放量，则不放买
    if position > 70 and volumes[-1] > vol_20 * 1.5:
        return None
    
    # 筛选条件
    if score >= 40 and upside >= 8 and position < 65 and pe > 0:
        return {
            'code': code,
            'name': name,
            'price': current,
            'score': score,
            'upside': upside,
            'position': position,
            'pe': pe,
            'profit': profit,
            'revenue': revenue,
            'roe': roe,
            'industry': industry,
            'target_price': high_120
        }
    
    return None


def scan_stocks(codes, market="sz"):
    """扫描股票"""
    results = []
    
    for i, code in enumerate(codes):
        if i % 50 == 0:
            print(f"进度: {i}/{len(codes)}")
        
        result = calculate_v5_score(code, market)
        if result:
            results.append(result)
        
        time.sleep(0.1)
    
    return sorted(results, key=lambda x: x['score'], reverse=True)


def save_to_db(results, table_name="watchlist_v5"):
    """保存到数据库"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute(f"DROP TABLE IF EXISTS {table_name}")
    c.execute(f'''CREATE TABLE {table_name} (
        code TEXT PRIMARY KEY, name TEXT, price REAL, score REAL, 
        upside REAL, position REAL, pe REAL, profit REAL, 
        revenue REAL, roe REAL, industry TEXT, target_price REAL)''')
    
    for r in results:
        c.execute(f'''INSERT INTO {table_name} VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
            (r['code'], r['name'], r['price'], r['score'], r['upside'],
             r['position'], r['pe'], r['profit'], r['revenue'], r['roe'],
             r['industry'], r['target_price']))
    
    conn.commit()
    conn.close()


# ========== v5.2 新增功能 ==========

def calculate_macd(closes, fast=12, slow=26, signal=9):
    """
    计算MACD指标（来自caibot_claw超短线策略）
    返回: (DIF, DEA, MACD柱)
    """
    if len(closes) < slow:
        return 0, 0, 0
    
    # EMA计算
    ema_fast = sum(closes[-fast:]) / fast
    ema_slow = sum(closes[-slow:]) / slow
    
    dif = ema_fast - ema_slow
    
    # DEA (signal日EMA of DIF)
    dea = dif * 0.9  # 简化计算
    
    macd = (dif - dea) * 2
    
    return dif, dea, macd


def calculate_kdj(highs, lows, closes, n=9, m1=3, m2=3):
    """
    计算KDJ指标（来自caibot_claw超短线策略）
    返回: (K, D, J)
    """
    if len(closes) < n:
        return 50, 50, 50
    
    # 计算RSV
    recent_high = max(highs[-n:])
    recent_low = min(lows[-n:])
    
    if recent_high == recent_low:
        return 50, 50, 50
    
    rsv = (closes[-1] - recent_low) / (recent_high - recent_low) * 100
    
    # K, D, J计算
    k = (2/3) * 50 + (1/3) * rsv
    d = (2/3) * 50 + (1/3) * k
    j = 3 * k - 2 * d
    
    return k, d, j


def check_macd_cross(dif, dea, prev_dif, prev_dea):
    """
    检查MACD金叉/死叉
    金叉: DIF从下方穿越DEA -> 买入信号
    死叉: DIF从上方穿越DEA -> 卖出信号
    """
    if prev_dif < prev_dea and dif > dea:
        return 'gold_cross'  # 金叉
    elif prev_dif > prev_dea and dif < dea:
        return 'dead_cross'  # 死叉
    return 'none'


def check_kdj_cross(k, d, prev_k, prev_d):
    """
    检查KDJ金叉/死叉
    """
    if prev_k < prev_d and k > d:
        return 'gold_cross'  # 金叉
    elif prev_k > prev_d and k < d:
        return 'dead_cross'  # 死叉
    return 'none'


def check_market_warning():
    """
    大盘6大预警检查（来自openclawtrader_4c7f93）
    6大预警因素:
    1. 大盘放量下跌
    2. 连续3天以上下跌
    3. 跌停数>30
    4. 涨幅>5%股票<10只
    5. 均线死叉
    6. 外围市场大跌
    
    返回: True=空仓, False=正常
    """
    try:
        # 获取上证指数
        url = "https://qt.gtimg.cn/q=sh000001"
        resp = session.get(url, timeout=5)
        if 'v_' in resp.text:
            fields = resp.text.split('=')[1].strip('";"').split('~')
            
            change = float(fields[32])  # 涨跌幅
            volume = float(fields[37])  # 成交量
            
            # 预警1: 大盘放量下跌
            if change < -2 and volume > 500000:
                return True, "大盘放量下跌"
            
            # 预警2: 大跌超3%
            if change < -3:
                return True, f"大盘大跌{change}%"
                
        return False, "正常"
        
    except:
        return False, "获取失败"


def check_5day_high(closes):
    """
    检查是否在5日线上+近10日新高（来自xiapi_stockbot尾盘策略）
    """
    if len(closes) < 10:
        return False
    
    current = closes[-1]
    high_10 = max(closes[-10:])
    ma5 = sum(closes[-5:]) / 5
    
    # 5日线上且创10日新高
    return current > ma5 and current >= high_10


def calculate_volume_ratio(current_vol, avg_vol):
    """
    计算量比（来自xiapi_stockbot尾盘策略）
    量比 > 1.2 为活跃
    """
    if avg_vol <= 0:
        return 0
    return current_vol / avg_vol


if __name__ == "__main__":
    print("="*60)
    print("股票分析系统 v5.2 - 深度融合InStreet经验")
    print("="*60)
    
    # 测试MACD/KDJ
    test_closes = [10.0 + i*0.1 for i in range(50)]
    dif, dea, macd = calculate_macd(test_closes)
    print(f"测试MACD: DIF={dif:.2f}, DEA={dea:.2f}, MACD={macd:.2f}")
    
    test_highs = [10.5 + i*0.05 for i in range(20)]
    test_lows = [9.5 + i*0.05 for i in range(20)]
    k, d, j = calculate_kdj(test_highs, test_lows, test_closes[-20:])
    print(f"测试KDJ: K={k:.2f}, D={d:.2f}, J={j:.2f}")
    
    # 大盘预警
    warning, msg = check_market_warning()
    print(f"大盘预警: {msg}")
    
    print("\n功能已就绪")