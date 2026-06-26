#!/usr/bin/env python3
"""
A股板块涨幅排行榜
使用东方财富网API获取板块数据
"""

import requests
import json
import sys
from datetime import datetime

def get_sector_rank(sector_type=1, limit=20):
    """
    获取板块涨幅排行榜
    sector_type: 1=行业板块, 2=概念板块, 3=地域板块
    limit: 返回数量
    """
    # 东方财富网板块行情API
    url = "http://push2.eastmoney.com/api/qt/clist/get"

    # 板块类型参数
    # fs: m:90+t:2 (行业板块), m:90+t:3 (概念板块), m:90+t:4 (地域板块)
    fs_map = {
        1: "m:90+t:2",  # 行业板块
        2: "m:90+t:3",  # 概念板块
        3: "m:90+t:4",  # 地域板块
    }

    fs = fs_map.get(sector_type, "m:90+t:2")

    params = {
        "pn": 1,
        "pz": limit,
        "po": 1,
        "np": 1,
        "fltt": 2,
        "invt": 2,
        "fid": "f3",  # 按涨跌幅排序
        "fs": fs,
        "fields": "f12,f14,f2,f3,f5,f6,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13"
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
        'Accept': 'application/json',
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            return {'error': f'HTTP错误: {response.status_code}'}

        data = response.json()

        if data.get('rc') != 0:
            return {'error': 'API返回错误'}

        diff_list = data.get('data', {}).get('diff', [])

        sectors = []
        for item in diff_list:
            sectors.append({
                'code': item.get('f12', ''),
                'name': item.get('f14', ''),
                'current': item.get('f2', 0),
                'change_percent': item.get('f3', 0),
                'change': item.get('f4', 0),
                'open': item.get('f5', 0),
                'high': item.get('f6', 0),
                'low': item.get('f7', 0),
                'volume': item.get('f5', 0),
                'amount': item.get('f6', 0),
                'turnover': item.get('f8', 0),
                'pe': item.get('f9', 0),
                'amplitude': item.get('f10', 0),
                'rise_fall': item.get('f11', 0),
                'highest': item.get('f12', 0),
                'lowest': item.get('f13', 0),
                'avg_pe': item.get('f62', 0),
            })

        return {'type': sector_type, 'sectors': sectors}

    except Exception as e:
        return {'error': str(e)}

def format_sector_report(data, limit=15):
    """格式化板块涨幅报告"""
    if 'error' in data:
        return f"❌ 获取失败: {data['error']}"

    sectors = data.get('sectors', [])
    sector_type = data.get('type', 1)

    type_names = {
        1: "行业板块",
        2: "概念板块",
        3: "地域板块",
    }

    type_name = type_names.get(sector_type, "板块")

    if not sectors:
        return f"📊 {type_name}涨幅排行榜（暂无数据）"

    # 获取当前时间
    now = datetime.now()
    time_str = now.strftime("%m月%d日 %H:%M")

    report = f"""
📊 A股{type_name}涨幅排行榜（午间汇总）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ {time_str}
"""

    # 涨幅榜前10
    report += f"\n🔥 **涨幅TOP{min(10, len(sectors))}**\n"
    for i, sector in enumerate(sectors[:10], 1):
        name = sector.get('name', '')
        change_pct = sector.get('change_percent', 0)
        current = sector.get('current', 0)
        turnover = sector.get('turnover', 0)

        sign = '+' if change_pct >= 0 else ''
        medal = '🥇' if i == 1 else '🥈' if i == 2 else ' ' if i == 3 else ''

        report += f"{medal} {i:2d}. {name:12s} {sign}{change_pct:>6.2f}%  {current:.2f}  换手率:{turnover:.2f}%\n"

    # 跌幅榜（倒数5）
    if len(sectors) > 5:
        report += f"\n❄️ **跌幅TOP5**\n"
        fall_sectors = [s for s in sectors if s.get('change_percent', 0) < 0][:5]
        for i, sector in enumerate(fall_sectors, 1):
            name = sector.get('name', '')
            change_pct = sector.get('change_percent', 0)
            current = sector.get('current', 0)

            sign = '+' if change_pct >= 0 else ''
            report += f"   {i}. {name:12s} {sign}{change_pct:>6.2f}%  {current:.2f}\n"

    report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    report += f"\n💡 数据来源：东方财富网 | 延迟约15分钟"

    return report

def main():
    # 获取行业板块
    limit = 50

    # 获取行业板块排行
    industry_data = get_sector_rank(1, limit)
    industry_report = format_sector_report(industry_data, limit)

    # 获取概念板块排行
    concept_data = get_sector_rank(2, limit)
    concept_report = format_sector_report(concept_data, limit)

    # 合并输出
    print(industry_report)
    print("\n" + "="*50 + "\n")
    print(concept_report)

if __name__ == '__main__':
    main()
