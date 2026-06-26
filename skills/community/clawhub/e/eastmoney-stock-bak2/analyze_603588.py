#!/usr/bin/env python3
"""
603588 股票数据分析
"""

import requests

def get_stock_data(code):
    """获取股票行情"""
    code = code.strip().upper()
    
    # 添加市场前缀
    if code.startswith('6') or code.startswith('5'):
        code = f"sh{code}"
    elif code.startswith('0') or code.startswith('3'):
        code = f"sz{code}"
    
    url = f"https://hq.sinajs.cn/list={code}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'http://finance.sina.com.cn',
    }
    
    try:
        response = requests.get(url, timeout=10, headers=headers)
        
        if response.status_code != 200:
            print(f"❌ HTTP 错误：{response.status_code}")
            return None
        
        data = response.text.strip()
        
        if '=' not in data:
            print("❌ 数据格式错误")
            return None
        
        # 解析数据
        parts = data.split('=')
        if len(parts) < 2:
            print("❌ 数据解析失败")
            return None
        
        content = parts[1].strip().strip('";')
        values = content.split(',')
        
        if len(values) < 10:
            print("❌ 数据不完整")
            return None
        
        name = values[0]
        open_price = float(values[1]) if values[1] else 0
        yesterday_close = float(values[2]) if values[2] else 0
        current_price = float(values[3]) if values[3] else 0
        high_price = float(values[4]) if values[4] else 0
        low_price = float(values[5]) if values[5] else 0
        
        # 计算涨跌
        change = current_price - yesterday_close
        if yesterday_close > 0:
            change_percent = (change / yesterday_close) * 100
        else:
            change_percent = 0
        
        # 成交量和成交额
        try:
            volume = int(float(values[8])) if len(values) > 8 and values[8] else 0
        except:
            volume = 0
        
        try:
            amount = float(values[9]) if len(values) > 9 and values[9] else 0
        except:
            amount = 0
        
        # 买盘卖盘
        try:
            bid1 = float(values[11]) if values[11] else 0  # 买一价
            bid1_vol = int(values[10]) if values[10] else 0  # 买一量
            ask1 = float(values[13]) if values[13] else 0  # 卖一价
            ask1_vol = int(values[12]) if values[12] else 0  # 卖一量
        except:
            bid1 = bid1_vol = ask1 = ask1_vol = 0
        
        print()
        print("=" * 60)
        print(f"📈 {name} ({code.upper()})")
        print("=" * 60)
        print(f"当前价格：¥{current_price:.2f}")
        print(f"涨跌额：{change:+.2f}")
        print(f"涨跌幅：{change_percent:+.2f}%")
        print()
        print("💹 【今日行情】")
        print(f"开盘：¥{open_price:.2f}")
        print(f"昨收：¥{yesterday_close:.2f}")
        print(f"最高：¥{high_price:.2f}")
        print(f"最低：¥{low_price:.2f}")
        print()
        print("📊 【成交情况】")
        print(f"成交量：{volume/10000:.2f}万手")
        print(f"成交额：¥{amount/100000000:.2f}亿元")
        print()
        print("📋 【买卖盘口】")
        print(f"卖一：¥{ask1:.2f} ({ask1_vol}手)")
        print(f"买一：¥{bid1:.2f} ({bid1_vol}手)")
        print()
        
        # 分析建议
        print("🎯 【简要分析】")
        print("-" * 60)
        
        if change_percent > 5:
            print("🟢 大涨 - 强势上涨")
        elif change_percent > 2:
            print("🟡 上涨 - 走势偏强")
        elif change_percent > -2:
            print("🟠 震荡 - 窄幅整理")
        elif change_percent > -5:
            print("🟡 下跌 - 走势偏弱")
        else:
            print("🔴 大跌 - 弱势下跌")
        
        print()
        
        # 买卖建议
        print("💡 【操作建议】")
        print("-" * 60)
        
        if change_percent > 3:
            print("⚠️  涨幅较大，不建议追高")
            print("   等待回调企稳")
        elif change_percent > 0:
            print("🟡 温和上涨，可以关注")
            print("   如有持仓可继续持有")
        elif change_percent > -3:
            print("🟠 小幅下跌，观望为主")
            print("   等待企稳信号")
        else:
            print("🔴 跌幅较大，谨慎操作")
            print("   不要盲目抄底")
        
        print()
        print("⚠️  风险提示：")
        print("   以上分析仅供参考，不构成投资建议")
        print("   股市有风险，投资需谨慎")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

print("分析 603588...")
get_stock_data("603588")
