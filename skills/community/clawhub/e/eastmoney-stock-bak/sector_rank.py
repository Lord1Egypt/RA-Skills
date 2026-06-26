#!/usr/bin/env python3
"""
查看 A 股热门板块排行
"""

import requests

def get_sector_rank():
    """获取板块涨幅排行"""
    
    # 使用东方财富 API 获取板块排行
    url = "http://push2.eastmoney.com/api/qt/clist/get"
    
    params = {
        'pn': '1',
        'pz': '20',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:90 t:3',
        'fields': 'f1,f2,f3,f4,f12,f13,f14,f15,f16,f17,f18,f20,f21,f24,f25,f22,f11,f62,f128,f136,f115,f152'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'http://quote.eastmoney.com',
    }
    
    try:
        response = requests.get(url, params=params, timeout=10, headers=headers)
        
        if response.status_code != 200:
            print(f"❌ HTTP 错误：{response.status_code}")
            return None
        
        data = response.json()
        
        if data['data'] is None or 'diff' not in data['data']:
            print("❌ 数据获取失败")
            return None
        
        sectors = data['data']['diff']
        
        print()
        print("=" * 70)
        print("🔥 A 股板块涨幅排行（前 20 名）")
        print("=" * 70)
        print()
        
        print(f"{'排名':<4} {'板块名称':<15} {'涨幅':<10} {'涨跌额':<10} {'领涨股':<15}")
        print("-" * 70)
        
        for i, sector in enumerate(sectors[:20], 1):
            name = sector.get('f14', 'N/A')
            change_percent = sector.get('f3', 0)
            change = sector.get('f4', 0)
            leader = sector.get('f20', 'N/A')  # 领涨股代码
            
            # 根据涨幅显示颜色标记
            if change_percent > 5:
                flag = "🔥"
            elif change_percent > 3:
                flag = "🟡"
            elif change_percent > 0:
                flag = "🟢"
            else:
                flag = "🔴"
            
            print(f"{i:<4} {flag} {name:<15} {change_percent:+.2f}%{'':<5} {change:+.2f}{'':<6} {leader:<15}")
        
        print("-" * 70)
        print()
        
        # 分析热门板块
        print("📊 【热门板块分析】")
        print("-" * 70)
        
        # 找出涨幅前 5 的板块
        top5 = sectors[:5]
        
        print("\n🏆 今日最火板块 TOP5：")
        for i, sector in enumerate(top5, 1):
            name = sector.get('f14', 'N/A')
            change_percent = sector.get('f3', 0)
            print(f"  {i}. {name} ({change_percent:+.2f}%)")
        
        print()
        print("💡 【操作建议】")
        print("-" * 70)
        print("1. 热门板块可以关注，但不要盲目追高")
        print("2. 选择板块内的龙头股，安全性更高")
        print("3. 设置止损，控制仓位")
        print("4. 注意板块轮动，不要死守一个板块")
        print()
        print("⚠️  风险提示：")
        print("   板块轮动快，今日热门明日可能回调")
        print("   以上分析仅供参考，不构成投资建议")
        print("=" * 70)
        
        return sectors
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        print("\n建议：")
        print("1. 检查网络连接")
        print("2. 使用交易软件查看实时板块排行")
        print("3. 推荐 APP：同花顺、东方财富、雪球")
        return None

print("获取 A 股板块排行...")
get_sector_rank()
