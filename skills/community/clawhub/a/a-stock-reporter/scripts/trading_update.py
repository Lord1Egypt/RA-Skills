#!/usr/bin/env python3
"""
交易时段自动更新脚本
由cron定时调用，生成特定时段的市场更新
"""

import sys
import argparse
from datetime import datetime
from market_brief import get_market_indices, analyze_market_stance, get_hot_stocks


def get_time_context(time_str: str) -> str:
    """根据时间判断市场阶段"""
    contexts = {
        '0930': '🌅 开盘实况',
        '1030': '📊 早盘中场',
        '1130': '🍜 午盘收盘',
        '1330': '☕ 午后开盘',
        '1430': '🏁 尾盘前瞻',
    }
    return contexts.get(time_str, '📈 盘中更新')


def generate_trading_update(time_str: str) -> str:
    """生成交易时段更新"""
    now = datetime.now().strftime("%m-%d %H:%M")
    context = get_time_context(time_str)
    
    # 获取数据
    indices = get_market_indices()
    hot_stocks = get_hot_stocks(3)  # 只取前3，更简洁
    stance = analyze_market_stance(indices)
    
    # 根据时段调整内容
    lines = [
        f"{context} - {now}",
        "━━━━━━━━━━━━━━━━━━━━",
    ]
    
    # 大盘速览
    for name, data in indices.items():
        sign = "+" if data['change_pct'] >= 0 else ""
        lines.append(f"{name}: {data['price']:.2f} ({sign}{data['change_pct']:.2f}%)")
    
    lines.append("")
    
    # 时段特定内容
    if time_str == '0930':
        lines.extend([
            "【开盘观察】",
            "关注量能配合及主线板块持续性",
        ])
    elif time_str == '1430':
        lines.extend([
            "【尾盘策略】",
            "关注资金流向，决定是否持仓过夜",
        ])
    else:
        # 涨跌家数统计
        lines.extend([
            "【活跃个股】",
        ])
        for code, data in hot_stocks:
            name = data.get('name', '未知')
            change = data.get('percentage', 0)
            sign = "+" if change >= 0 else ""
            lines.append(f"{name}: {sign}{change:.2f}%")
    
    lines.extend([
        "",
        f"【当前立场】{stance}",
    ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='A股交易时段自动更新')
    parser.add_argument('--time', required=True, 
                       choices=['0930', '1030', '1130', '1330', '1430'],
                       help='交易时段 (0930/1030/1130/1330/1430)')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='输出格式')
    
    args = parser.parse_args()
    
    try:
        output = generate_trading_update(args.time)
        print(output)
    except Exception as e:
        print(f"❌ 生成更新失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
