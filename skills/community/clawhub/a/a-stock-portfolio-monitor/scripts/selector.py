# -*- coding: utf-8 -*-
"""
短线选股系统 V1 - 扩展版
- 数据获取：腾讯财经API（实时）
- 股票池：200只
"""

import urllib.request
import json
import time
from datetime import datetime
from pathlib import Path
import sys

# 扩展股票池（200只）
STOCK_POOL = [
    # 新能源/电池 (20只)
    '002594', '300750', '002460', '002466', '002709', '300014', '300073', '002074', '002812', '002340',
    '300207', '002176', '002245', '300438', '002074', '002407', '002709', '300450', '002074', '300750',
    # AI算力/科技 (20只)
    '002415', '600845', '000938', '300033', '300496', '002230', '002236', '300474', '300496', '002236',
    '300308', '300502', '002281', '300383', '300624', '300212', '300768', '300223', '300339', '300170',
    # 银行 (15只)
    '600036', '601398', '601288', '601939', '601988', '601328', '601166', '601818', '601998', '601169',
    '601229', '601838', '601997', '601577', '601128',
    # 白酒 (15只)
    '000858', '000568', '002304', '600519', '600702', '600779', '600197', '600559', '603589', '603198',
    '603369', '600199', '603919', '603027', '603156',
    # 医药 (20只)
    '600276', '000538', '600436', '300003', '002007', '000963', '600196', '300760', '300015', '300347',
    '002001', '600079', '600521', '603259', '300122', '300142', '688180', '688363', '688185', '688202',
    # 半导体/芯片 (20只)
    '603986', '603501', '002049', '300782', '300661', '603160', '600584', '002156', '300316', '600360',
    '688981', '688012', '688008', '688019', '688396', '688126', '688521', '688107', '688123', '688072',
    # 汽车 (15只)
    '601633', '601238', '000625', '002594', '600104', '600066', '000550', '600741', '002048', '002126',
    '601127', '600699', '603035', '603197', '603596',
    # 光伏 (15只)
    '601012', '600438', '002459', '300274', '688599', '600732', '603806', '002129', '601877', '688390',
    '688223', '600481', '002056', '603688', '300118',
    # 券商 (15只)
    '600030', '300059', '000776', '600837', '601688', '002736', '000166', '601211', '600999', '601377',
    '000728', '600958', '601881', '600061', '601108',
    # 军工 (15只)
    '600893', '000768', '002179', '600372', '600760', '000738', '600967', '600316', '600391', '600862',
    '002013', '002025', '300114', '300034', '300775',
    # 煤炭/能源 (15只)
    '601088', '601225', '600188', '601699', '600123', '600348', '601666', '600508', '600395', '600971',
    '601015', '600792', '603113', '600157', '600403',
    # 钢铁/有色 (15只)
    '600019', '000932', '600010', '600808', '000825', '600362', '601899', '600547', '600489', '600497',
    '000878', '000630', '601168', '600111', '600392',
]


def get_realtime_quote(code):
    """腾讯财经实时行情"""
    try:
        prefix = 'sh' if code.startswith('6') else 'sz'
        url = f"http://qt.gtimg.cn/q={prefix}{code}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=5)
        text = resp.read().decode('gbk')
        
        data = text.split('~')
        if len(data) < 45:
            return None
        
        return {
            'name': data[1],
            'price': float(data[3]),
            'open': float(data[5]),
            'high': float(data[33]),
            'low': float(data[34]),
            'pre_close': float(data[4]),
            'change_pct': float(data[32]),
            'volume': int(data[36]) * 100,
            'amount': float(data[37]) * 10000,
            'pe': float(data[52]) if data[52] else 0,
            'pb': float(data[46]) if data[46] else 0,
        }
    except:
        return None


def select_stocks():
    """选股主逻辑"""
    print("="*70)
    print("短线选股系统 V1 - 扩展版 (200只股票)")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print("\n【评分逻辑】")
    print("  1. 涨幅评分: 0-30分 (涨停30分)")
    print("  2. 量价配合: 0-25分 (成交额)")
    print("  3. 强势程度: 0-20分 (接近最高价)")
    print("  4. 估值水平: 0-15分 (PE/PB合理)")
    print("  5. 流动性: 0-10分 (成交量)")
    print("="*70)
    
    # 去重
    unique_codes = list(dict.fromkeys(STOCK_POOL))
    
    results = []
    total = len(unique_codes)
    
    print(f"\n扫描 {total} 只股票...")
    
    for i, code in enumerate(unique_codes, 1):
        progress = f"[{i}/{total}] {code}"
        sys.stdout.write(f"\r{progress:<20}")
        sys.stdout.flush()
        
        rt = get_realtime_quote(code)
        if not rt:
            continue
        
        if 'ST' in rt['name']:
            continue
        
        price = rt['price']
        change_pct = rt['change_pct']
        volume = rt['volume']
        amount = rt['amount']
        high = rt['high']
        low = rt['low']
        open_price = rt['open']
        pe = rt['pe']
        
        # 评分
        score = 0
        details = []
        
        # 1. 涨幅 (0-30分)
        if change_pct > 9.9:
            score += 30
            details.append("涨停30")
        elif change_pct > 7:
            score += 25
            details.append("大涨25")
        elif change_pct > 5:
            score += 20
            details.append("涨20")
        elif change_pct > 3:
            score += 15
            details.append("涨15")
        elif change_pct > 1:
            score += 10
        elif change_pct > 0:
            score += 5
        
        # 2. 成交额 (0-25分)
        if amount > 1000000000:
            score += 25
            details.append("巨量25")
        elif amount > 500000000:
            score += 20
            details.append("大量20")
        elif amount > 100000000:
            score += 15
            details.append("量15")
        elif amount > 50000000:
            score += 10
        
        # 3. 强势程度 (0-20分)
        if high > open_price:
            position = (price - open_price) / (high - open_price) if (high - open_price) > 0 else 0
            if position > 0.8:
                score += 20
                details.append("强势20")
            elif position > 0.6:
                score += 15
                details.append("强15")
            elif position > 0.4:
                score += 10
        
        # 4. 估值 (0-15分)
        if 0 < pe < 30:
            score += 15
            details.append("估值15")
        elif 0 < pe < 50:
            score += 10
        
        # 5. 流动性 (0-10分)
        if volume > 10000000:
            score += 10
            details.append("流动10")
        elif volume > 5000000:
            score += 7
        elif volume > 1000000:
            score += 5
        
        final_score = min(100, score)
        
        if final_score >= 50:
            results.append({
                'code': code,
                'name': rt['name'],
                'price': price,
                'change_pct': change_pct,
                'volume': volume,
                'amount': amount,
                'pe': pe,
                'score': final_score,
                'details': ','.join(details),
            })
        
        time.sleep(0.03)  # 加快扫描速度
    
    print("\n")
    
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print("\n" + "="*70)
    print(f"选中 {len(results)} 只股票 (>=50分)")
    print("="*70)
    
    for i, r in enumerate(results[:15], 1):
        amount_wan = r['amount'] / 10000
        print(f"\n{i}. {r['name']}({r['code']}) - {r['score']}分")
        print(f"   价格: {r['price']:.2f} ({r['change_pct']:+.2f}%)")
        print(f"   成交: {r['volume']/10000:.0f}万股 / {amount_wan:.0f}万元")
        print(f"   PE: {r['pe']:.1f}")
        print(f"   得分: {r['details']}")
    
    print("\n" + "="*70)
    return results


if __name__ == '__main__':
    select_stocks()
