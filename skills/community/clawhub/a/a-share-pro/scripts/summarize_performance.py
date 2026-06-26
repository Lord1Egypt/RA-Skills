#!/usr/bin/env python3
"""
获取自选股行情汇总
自动使用 monitor 模块查询所有股票的实时行情
"""
import sys
sys.path.insert(0, '/Users/wangrx/.openclaw/workspace/skills/a-share-pro/scripts')

import os
from config import WATCHLIST_FILE, DEFAULT_WATCHLIST


def summarize() -> bool:
    """获取并显示所有自选股的行情汇总"""
    
    from monitor import AShareMonitor
    
    # 读取自选股
    if not os.path.exists(WATCHLIST_FILE):
        print("📭 自选股列表为空")
        print("\n💡 提示：还没有自选股，可以使用 add_stock.py 添加")
        return False
    
    with open(WATCHLIST_FILE, 'r', encoding='utf-8') as f:
        stocks = [line.strip() for line in f if line.strip()]
    
    if not stocks:
        print("📭 自选股列表为空")
        return False
    
    # 初始化监控器
    monitor = AShareMonitor(delay=1.0)
    
    # 打印标题
    print("=" * 70)
    print("💼 A-Share Pro - 自选股实时行情")
    print("=" * 70)
    
    # 查询并显示
    positive_count = 0
    total_change_pct = 0
    
    for stock in stocks:
        parts = stock.split('|')
        code = parts[0] if len(parts) >= 1 else "未知"
        name = parts[1] if len(parts) >= 2 else ""
        
        result = monitor.get_quote(code)
        
        if 'error' not in result:
            price = result.get('现价', 'N/A')
            change = result.get('涨跌额', 'N/A')
            change_pct = result.get('涨跌幅', 'N/A')
            source = result.get('source', '')
            
            # 颜色标记（终端支持时）
            color_up = '\033[92m'  # 绿色（A 股上涨用红/绿根据地区不同）
            color_down = '\033[91m'
            reset = '\033[0m'
            
            # 统计
            try:
                pct_val = float(change_pct.replace('%', ''))
                total_change_pct += pct_val
                if pct_val > 0:
                    positive_count += 1
                    print(f"{color_up}✅{reset} {code} - {name}")
                elif pct_val < 0:
                    print(f"{color_down}⬇️{reset} {code} - {name}")
                else:
                    print(f"➖ {code} - {name}")
            except:
                print(f"❔ {code} - {name}")
            
            print(f"   💰 ¥{price}  {change:10} ({change_pct:>10}) [{source}]")
        else:
            print(f"❌ {code} - {name or ''}")
            print(f"   错误：{result['error']}")
    
    # 总体统计
    print("\n" + "=" * 70)
    avg_change = total_change_pct / len(stocks) if stocks else 0
    
    if positive_count > len(stocks) / 2:
        trend = "📈 整体偏强"
    elif positive_count < len(stocks) / 2:
        trend = "📉 整体偏弱"
    else:
        trend = "⚖️ 震荡整理"
    
    print(f"📊 持仓概览：{len(stocks)}只 | 上涨:{positive_count}只 | 下跌:{len(stocks)-positive_count}只")
    print(f"📉 平均涨跌幅：{avg_change:+.2f}%")
    print(f"💡 整体趋势：{trend}")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    summarize()
