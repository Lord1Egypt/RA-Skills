#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可转债监控提醒模块
强赎、下修、回售等条款监控
"""

from datetime import datetime, timedelta

# 模拟转债监控数据
MOCK_MONITOR_DATA = [
    {
        'code': '123100',
        'name': '小康转债',
        'current_price': 185.5,
        'convert_value': 178.2,
        'days_to_redemption': 5,
        'redemption_condition': '已触发',
        'redemption_price': 102,
        'announcement_date': '2026-03-05',
        'last_trading_date': '2026-03-12',
    },
    {
        'code': '123150',
        'name': '九洲转债',
        'current_price': 112.3,
        'convert_value': 98.5,
        'down_revision_count': 2,
        'down_revision_date': '2026-02-28',
        'next_down_revision_possible': '2026-04-01',
    },
    {
        'code': '123180',
        'name': '浙 22 转债',
        'current_price': 98.5,
        'convert_value': 95.2,
        'years_to_maturity': 1.5,
        'put_option_condition': '接近触发',
        'put_option_price': 101,
    },
]


def check_strong_redemption():
    """
    检查强赎提醒
    
    强赎条件（通常）:
    - 正股连续 30 个交易日中至少 15 日收盘价 >= 转股价 * 130%
    - 或者转债余额 < 3000 万元
    
    Returns:
        list: 强赎提醒列表
    """
    alerts = []
    
    for cb in MOCK_MONITOR_DATA:
        if cb.get('redemption_condition') == '已触发':
            alerts.append({
                'type': '⚠️ 强赎提醒',
                'code': cb['code'],
                'name': cb['name'],
                'reason': f"强赎条件已触发，最后交易日 {cb['last_trading_date']}",
                'deadline': cb['last_trading_date'],
                'current_price': cb['current_price'],
                'redemption_price': cb['redemption_price'],
                'loss_warning': f"如不及时操作，将亏损 {cb['current_price'] - cb['redemption_price']}元/张",
            })
    
    return alerts


def check_downward_revision():
    """
    检查下修提醒
    
    下修条件（通常）:
    - 正股连续 30 个交易日中至少 15 日收盘价 <= 转股价 * 85%
    - 董事会可提议下修转股价
    
    Returns:
        list: 下修提醒列表
    """
    alerts = []
    
    for cb in MOCK_MONITOR_DATA:
        # 检查已下修
        if cb.get('down_revision_date'):
            alerts.append({
                'type': '📉 下修公告',
                'code': cb['code'],
                'name': cb['name'],
                'reason': f"已下修转股价，下修日期 {cb['down_revision_date']}",
                'deadline': cb.get('next_down_revision_possible', 'N/A'),
                'revision_count': cb.get('down_revision_count', 1),
            })
        
        # 检查可能下修
        if cb.get('current_price', 100) < 105 and cb.get('convert_value', 100) < 95:
            if not cb.get('down_revision_date'):
                alerts.append({
                    'type': '👀 可能下修',
                    'code': cb['code'],
                    'name': cb['name'],
                    'reason': f"正股持续低于转股价，可能下修",
                    'deadline': cb.get('next_down_revision_possible', '待公告'),
                })
    
    return alerts


def check_put_option():
    """
    检查回售提醒
    
    回售条件（通常）:
    - 最后 2 年，正股连续 30 日收盘价 <= 转股价 * 70%
    - 或者改变募集资金用途
    
    Returns:
        list: 回售提醒列表
    """
    alerts = []
    
    for cb in MOCK_MONITOR_DATA:
        if cb.get('put_option_condition') == '接近触发':
            alerts.append({
                'type': '💰 回售机会',
                'code': cb['code'],
                'name': cb['name'],
                'reason': f"回售条件接近触发，回售价 {cb['put_option_price']}元",
                'deadline': '需关注公告',
                'current_price': cb['current_price'],
                'put_price': cb['put_option_price'],
            })
    
    return alerts


def check_maturity_reminder():
    """
    检查到期提醒
    
    Returns:
        list: 到期提醒列表
    """
    alerts = []
    today = datetime.now()
    
    for cb in MOCK_MONITOR_DATA:
        years_to_maturity = cb.get('years_to_maturity', 5)
        if years_to_maturity < 2:
            alerts.append({
                'type': '⏰ 到期提醒',
                'code': cb['code'],
                'name': cb['name'],
                'reason': f"距离到期还有约{int(years_to_maturity * 365)}天",
                'deadline': f"{today.year + int(years_to_maturity)}年",
                'years_left': years_to_maturity,
            })
    
    return alerts


def get_all_alerts():
    """
    获取所有提醒
    
    Returns:
        list: 所有提醒
    """
    all_alerts = []
    
    all_alerts.extend(check_strong_redemption())
    all_alerts.extend(check_downward_revision())
    all_alerts.extend(check_put_option())
    all_alerts.extend(check_maturity_reminder())
    
    return all_alerts


def format_alert_message(alert):
    """
    格式化提醒消息
    
    Args:
        alert: 提醒字典
        
    Returns:
        str: 格式化后的消息
    """
    lines = [
        f"{alert['type']}: {alert['name']} ({alert['code']})",
        f"  原因：{alert['reason']}",
        f"  截止：{alert['deadline']}",
    ]
    
    if 'loss_warning' in alert:
        lines.append(f"  ⚠️ {alert['loss_warning']}")
    
    if 'current_price' in alert and 'redemption_price' in alert:
        lines.append(f"  现价：{alert['current_price']}元，强赎价：{alert['redemption_price']}元")
    
    return '\n'.join(lines)


if __name__ == "__main__":
    # 测试
    print("=== 强赎提醒 ===")
    redemption = check_strong_redemption()
    if redemption:
        for alert in redemption:
            print(format_alert_message(alert))
    else:
        print("暂无强赎提醒")
    
    print("\n=== 下修提醒 ===")
    revision = check_downward_revision()
    if revision:
        for alert in revision:
            print(format_alert_message(alert))
    else:
        print("暂无下修提醒")
    
    print("\n=== 所有提醒汇总 ===")
    all_alerts = get_all_alerts()
    if all_alerts:
        print(f"共 {len(all_alerts)} 条提醒:")
        for alert in all_alerts:
            print(f"  - {alert['type']}: {alert['name']}")
    else:
        print("✅ 暂无提醒")
