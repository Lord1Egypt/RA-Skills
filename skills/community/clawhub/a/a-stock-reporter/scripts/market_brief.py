#!/usr/bin/env python3
"""
A股市场简报生成脚本
生成大盘概览 + 板块表现 + 热门个股
"""

import sys
import json
from datetime import datetime

try:
    import easyquotation
except ImportError:
    print("❌ 请先安装依赖: pip install easyquotation")
    sys.exit(1)


def get_market_indices() -> dict:
    """获取大盘指数数据"""
    quotation = easyquotation.use('sina')
    indices = {
        'sh000001': '上证指数',
        'sz399001': '深证成指', 
        'sz399006': '创业板指',
        'sh000688': '科创50'
    }
    
    data = quotation.stocks(list(indices.keys()))
    result = {}
    
    for code, name in indices.items():
        if code in data:
            d = data[code]
            price = d.get('now', 0)
            close = d.get('close', price)
            if close and close != 0:
                change_pct = (price - close) / close * 100
            else:
                change_pct = 0
            
            result[name] = {
                'price': price,
                'change_pct': change_pct,
                'trend': '📈' if change_pct > 0 else '📉' if change_pct < 0 else '➡️'
            }
    
    return result


def get_hot_stocks(limit: int = 10) -> list:
    """获取热门股票（成交额最高）"""
    quotation = easyquotation.use('sina')
    
    # 获取全部A股快照
    all_stocks = quotation.market_snapshot(prefix=True)
    
    # 按成交额排序
    sorted_stocks = sorted(
        all_stocks.items(),
        key=lambda x: x[1].get('amount', 0),
        reverse=True
    )
    
    return sorted_stocks[:limit]


def analyze_market_stance(indices: dict) -> str:
    """根据指数表现判断市场立场"""
    changes = [v['change_pct'] for v in indices.values()]
    avg_change = sum(changes) / len(changes) if changes else 0
    
    if avg_change > 1.5:
        return "🔥 强势上涨，积极做多"
    elif avg_change > 0.5:
        return "📈 震荡上行，适度参与"
    elif avg_change > -0.5:
        return "➡️ 横盘震荡，精选个股"
    elif avg_change > -1.5:
        return "📉 震荡偏弱，控制仓位"
    else:
        return "❄️ 明显下跌，观望为主"


def format_market_brief() -> str:
    """格式化市场简报"""
    now = datetime.now().strftime("%m-%d %H:%M")
    
    # 获取数据
    indices = get_market_indices()
    hot_stocks = get_hot_stocks(5)
    stance = analyze_market_stance(indices)
    
    # 构建输出
    lines = [
        f"📊 A股市场简报 - {now}",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "【大盘概况】",
    ]
    
    for name, data in indices.items():
        sign = "+" if data['change_pct'] >= 0 else ""
        lines.append(f"{name}: {data['price']:.2f} ({sign}{data['change_pct']:.2f}%) {data['trend']}")
    
    lines.extend([
        "",
        "【成交热门】",
    ])
    
    for code, data in hot_stocks:
        name = data.get('name', '未知')
        amount = data.get('amount', 0) / 100000000  # 转亿元
        change = data.get('percentage', 0)
        sign = "+" if change >= 0 else ""
        lines.append(f"{name}({code}): {amount:.1f}亿 | {sign}{change:.2f}%")
    
    lines.extend([
        "",
        "【市场立场】",
        stance,
    ])
    
    return "\n".join(lines)


def main():
    try:
        brief = format_market_brief()
        print(brief)
    except Exception as e:
        print(f"❌ 生成简报失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
