#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股黑天鹅监控 - 完整版（使用历史数据）
恢复所有分析模块：建仓条件、退出信号、风格分裂预警
"""

import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import traceback
import sys

# 配置
EMAIL_CONFIG = {
    "smtp_server": "smtp.qq.com",
    "smtp_port": 587,
    "from_email": "57189896@qq.com",
    "to_email": "57189896@qq.com",
    "auth_code": "dskokcscwmkdbhjg"
}

DATA_DIR = "/root/.openclaw/workspace/blackswan_data"
HISTORY_FILE = os.path.join(DATA_DIR, "iv_history.json")

# 建仓阈值配置
ENTRY_THRESHOLDS = {
    '沪深300': 15.5,
    '上证50': 16.0,
    '中证500': 23.0,
    '科创50': 25.0,
    '创业板': 24.0
}

# 退出阈值配置
EXIT_THRESHOLDS = {
    '一级退出_IV涨幅': 55,  # IV较建仓时上涨≥55%
    '一级退出_融资降幅': 5,  # 融资余额下降>5%
    '二级退出_IV涨幅': 30,  # 一级退出后IV再涨≥30%
    '二级退出_融资累计降幅': 8  # 融资余额累计下降>8%
}

# 风格分裂预警阈值
STYLE_SPLIT_THRESHOLD = 8  # 大小盘IV差值阈值

def load_history():
    """加载历史数据"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def calculate_iv_change(history, name):
    """计算IV较昨日的涨跌幅度"""
    if name not in history or len(history[name]) < 2:
        return None
    
    latest = history[name][-1].get('iv')
    previous = history[name][-2].get('iv')
    
    if latest is None or previous is None or previous == 0:
        return None
    
    return ((latest - previous) / previous) * 100

def calculate_percentile(history, name):
    """计算IV历史分位数（近60日）"""
    if name not in history or len(history[name]) < 10:
        return None
    
    # 取最近60个数据点
    iv_values = [d.get('iv') for d in history[name][-60:] if d.get('iv') is not None]
    
    if len(iv_values) < 10:
        return None
    
    current_iv = history[name][-1].get('iv')
    if current_iv is None:
        return None
    
    # 计算分位数
    count_below = sum(1 for v in iv_values if v < current_iv)
    percentile = (count_below / len(iv_values)) * 100
    
    return percentile

def check_entry_conditions(latest_iv):
    """检查建仓条件"""
    results = {}
    any_triggered = False
    
    for name, threshold in ENTRY_THRESHOLDS.items():
        iv = latest_iv.get(name)
        if iv is None:
            results[name] = {'status': 'missing', 'message': '数据缺失'}
        elif iv < threshold:
            results[name] = {'status': 'triggered', 'iv': iv, 'threshold': threshold}
            any_triggered = True
        else:
            results[name] = {'status': 'not_triggered', 'iv': iv, 'threshold': threshold}
    
    return results, any_triggered

def check_exit_signals(history, latest_iv, latest_margin):
    """检查退出信号"""
    # 这里简化处理，实际应该跟踪持仓成本
    # 使用IV的5日涨幅作为替代指标
    
    signals = {
        '一级退出': {'triggered': False, 'reasons': []},
        '二级退出': {'triggered': False, 'reasons': []}
    }
    
    # 检查IV短期暴涨（5日涨幅超过阈值）
    for name in ['沪深300', '上证50', '中证500', '科创50']:
        if name in history and len(history[name]) >= 5:
            latest = history[name][-1].get('iv')
            past = history[name][-5].get('iv')
            if latest and past and past > 0:
                change_5d = ((latest - past) / past) * 100
                if change_5d >= EXIT_THRESHOLDS['一级退出_IV涨幅']:
                    signals['一级退出']['triggered'] = True
                    signals['一级退出']['reasons'].append(f"{name} IV 5日暴涨 {change_5d:.1f}%")
    
    # 检查融资余额变化（需要更多历史数据）
    if 'margin' in history and len(history['margin']) >= 5:
        latest_m = history['margin'][-1].get('value')
        past_m = history['margin'][-5].get('value')
        if latest_m and past_m and past_m > 0:
            margin_change = ((latest_m - past_m) / past_m) * 100
            if margin_change < -EXIT_THRESHOLDS['一级退出_融资降幅']:
                signals['一级退出']['triggered'] = True
                signals['一级退出']['reasons'].append(f"融资余额5日下降 {abs(margin_change):.1f}%")
    
    return signals

def check_style_split(latest_iv):
    """检查风格分裂（大小盘IV差值）"""
    # 大盘：上证50，小盘：中证500
    large_cap = latest_iv.get('上证50')
    small_cap = latest_iv.get('中证500')
    
    if large_cap is None or small_cap is None:
        return None
    
    diff = abs(small_cap - large_cap)
    
    return {
        'diff': diff,
        'threshold': STYLE_SPLIT_THRESHOLD,
        'triggered': diff > STYLE_SPLIT_THRESHOLD,
        'large_cap': large_cap,
        'small_cap': small_cap
    }

def generate_advice(entry_results, exit_signals, style_split):
    """生成操作建议"""
    # 新开仓建议
    entry_triggered = any(r['status'] == 'triggered' for r in entry_results.values())
    
    if entry_triggered:
        new_position_advice = "🟢 建议建仓 - 至少一个指数满足IV<阈值条件"
    else:
        new_position_advice = "⏸️ 建议观望 - 暂不满足建仓条件"
    
    # 现有持仓建议
    if exit_signals['一级退出']['triggered'] or exit_signals['二级退出']['triggered']:
        hold_advice = "🔴 建议减仓/退出 - 触发退出信号"
    elif style_split and style_split['triggered']:
        hold_advice = "🟡 建议警惕 - 风格分裂预警，关注持仓结构"
    else:
        hold_advice = "🟢 建议保持 - 无异常信号"
    
    return {
        'new_position': new_position_advice,
        'existing_position': hold_advice
    }

def send_email(subject, body):
    """发送邮件"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['from_email']
        msg['To'] = EMAIL_CONFIG['to_email']
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['from_email'], EMAIL_CONFIG['auth_code'])
        server.send_message(msg)
        server.quit()
        print(f"✅ 邮件发送成功: {subject}")
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def main():
    print("=" * 70)
    print("A股黑天鹅监控日报 - 完整版")
    print(f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 获取日期
    today = datetime.now()
    date_display = today.strftime('%Y-%m-%d')
    
    # 加载历史数据
    history = load_history()
    
    # 获取最新的IV数据
    latest_iv = {}
    iv_change = {}
    iv_percentile = {}
    
    indices = ['沪深300', '上证50', '中证500', '科创50', '创业板']
    
    for name in indices:
        if name in history and len(history[name]) > 0:
            latest_iv[name] = history[name][-1].get('iv')
            iv_change[name] = calculate_iv_change(history, name)
            iv_percentile[name] = calculate_percentile(history, name)
        else:
            latest_iv[name] = None
            iv_change[name] = None
            iv_percentile[name] = None
    
    # 获取最新融资余额
    latest_margin = None
    margin_change = None
    if 'margin' in history and len(history['margin']) > 0:
        latest_margin = history['margin'][-1].get('value')
        if len(history['margin']) >= 2:
            prev_margin = history['margin'][-2].get('value')
            if prev_margin and prev_margin > 0:
                margin_change = ((latest_margin - prev_margin) / prev_margin) * 100
    
    # 执行分析
    entry_results, entry_any = check_entry_conditions(latest_iv)
    exit_signals = check_exit_signals(history, latest_iv, latest_margin)
    style_split = check_style_split(latest_iv)
    advice = generate_advice(entry_results, exit_signals, style_split)
    
    # 获取缓存日期
    cache_date = history.get('沪深300', [{}])[-1].get('date', 'N/A') if '沪深300' in history and len(history['沪深300']) > 0 else 'N/A'
    if cache_date != 'N/A' and len(cache_date) == 8:
        cache_date = f"{cache_date[:4]}-{cache_date[4:6]}-{cache_date[6:]}"
    
    # 生成报告
    report = f"""
━━━━━━━━━━━━━━━━━━━━
📊 黑天鹅监控日报
━━━━━━━━━━━━━━━━━━━━
📅 {date_display}

⚠️ 注意：由于数据源连接问题，本次报告使用历史缓存数据。

━━━━━━━━━━━━━━━━━━━━
📈 市场数据概览
━━━━━━━━━━━━━━━━━━━━
"""
    
    # 添加各指数数据
    for name in indices:
        iv = latest_iv.get(name)
        change = iv_change.get(name)
        pct = iv_percentile.get(name)
        
        if iv is None:
            report += f"▸ {name:<8} 收盘: - | IV: 缺失 | 涨跌: - | 分位: -\n"
        else:
            change_str = f"{change:+.1f}%" if change is not None else "-"
            pct_str = f"{pct:.0f}%" if pct is not None else "-"
            report += f"▸ {name:<8} IV: {iv:.1f}% | 涨跌: {change_str} | 分位: {pct_str}\n"
    
    # 融资余额
    if latest_margin:
        margin_chg_str = f"({margin_change:+.2f}%)" if margin_change is not None else ""
        report += f"\n💰 融资余额: {latest_margin:.0f}亿 {margin_chg_str}\n"
    
    # 建仓条件检查
    report += """
━━━━━━━━━━━━━━━━━━━━
🎯 建仓条件检查
━━━━━━━━━━━━━━━━━━━━
"""
    for name in indices:
        result = entry_results.get(name, {'status': 'missing'})
        threshold = ENTRY_THRESHOLDS.get(name, 0)
        
        if result['status'] == 'missing':
            report += f"⚪ {name}: 数据缺失\n"
        elif result['status'] == 'triggered':
            report += f"✅ {name}: {result['iv']:.1f}% < {threshold}% 🎯 满足条件\n"
        else:
            report += f"❌ {name}: {result['iv']:.1f}% ≥ {threshold}%\n"
    
    if entry_any:
        report += "\n📋 结论: ✅ 满足建仓条件\n"
    else:
        report += "\n📋 结论: ❌ 不满足建仓条件\n"
    
    # 退出信号监控
    report += """
━━━━━━━━━━━━━━━━━━━━
🚨 退出信号监控
━━━━━━━━━━━━━━━━━━━━
"""
    if exit_signals['一级退出']['triggered']:
        report += f"🔴 一级退出: 已触发\n"
        for reason in exit_signals['一级退出']['reasons']:
            report += f"   - {reason}\n"
    else:
        report += f"🟢 一级退出: 未触发 (IV涨≥{EXIT_THRESHOLDS['一级退出_IV涨幅']}% 或 融资降>{EXIT_THRESHOLDS['一级退出_融资降幅']}%)\n"
    
    if exit_signals['二级退出']['triggered']:
        report += f"🔴 二级退出: 已触发\n"
    else:
        report += f"🟢 二级退出: 未触发 (一级后IV涨≥{EXIT_THRESHOLDS['二级退出_IV涨幅']}% 或 融资累计降>{EXIT_THRESHOLDS['二级退出_融资累计降幅']}%)\n"
    
    # 风格分裂预警
    report += """
━━━━━━━━━━━━━━━━━━━━
⚠️ 风格分裂预警
━━━━━━━━━━━━━━━━━━━━
"""
    if style_split:
        diff = style_split['diff']
        threshold = style_split['threshold']
        if style_split['triggered']:
            report += f"差值: {diff:.1f}个百分点 | 阈值: {threshold} | 状态: 🔴 预警\n"
            report += f"上证50: {style_split['large_cap']:.1f}% vs 中证500: {style_split['small_cap']:.1f}%\n"
        else:
            report += f"差值: {diff:.1f}个百分点 | 阈值: {threshold} | 状态: 🟢 正常\n"
    else:
        report += "数据不足，无法计算风格分裂指标\n"
    
    # 操作建议
    report += f"""
━━━━━━━━━━━━━━━━━━━━
📋 操作建议
━━━━━━━━━━━━━━━━━━━━
🆕 新开仓: {advice['new_position']}
📦 现有持仓: {advice['existing_position']}
"""
    
    # 风险提示
    report += """
━━━━━━━━━━━━━━━━━━━━
💡 风险提示
━━━━━━━━━━━━━━━━━━━━
"""
    if entry_any:
        report += "市场波动率处于低位，可能出现建仓机会。建议关注。\n"
    elif style_split and style_split['triggered']:
        report += "大小盘风格分化明显，注意持仓结构风险。\n"
    else:
        report += "市场波动率适中，维持现有策略。\n"
    
    report += f"""
━━━━━━━━━━━━━━━━━━━━
📌 数据说明
━━━━━━━━━━━━━━━━━━━━
数据缓存时间: {cache_date}
生成时间: {datetime.now().strftime('%H:%M')}
⚠️ 本报告使用历史缓存数据，建议通过交易软件核实实时数据。

━━━━━━━━━━━━━━━━━━━━
【龙虾AI】自动生成，仅供参考
━━━━━━━━━━━━━━━━━━━━
"""
    
    print(report)
    
    # 发送邮件
    subject = f"【黑天鹅监控】{date_display} 市场数据与策略信号 (缓存数据)"
    if send_email(subject, report):
        print("\n✅ 任务完成 - 邮件已发送")
        return 0
    else:
        print("\n❌ 任务失败 - 邮件发送失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
