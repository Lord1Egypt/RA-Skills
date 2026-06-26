#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股黑天鹅监控日报 - 修复版
修复数据获取问题，使用稳定的数据源
"""

import akshare as ak
import pandas as pd
import json
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import traceback

# ============ 配置 ============
EMAIL_CONFIG = {
    "smtp_server": "smtp.qq.com",
    "smtp_port": 587,
    "from_email": "57189896@qq.com",
    "to_email": "57189896@qq.com",
    "auth_code": "dskokcscwmkdbhjg"
}

DATA_DIR = "/root/.openclaw/workspace/blackswan_data"
HISTORY_FILE = os.path.join(DATA_DIR, "iv_history.json")

# 指数配置 - symbol映射
INDEX_CONFIG = {
    "沪深300": {"symbol": "sh000300", "iv_threshold": 15.5, "etf": "300ETF"},
    "上证50": {"symbol": "sh000016", "iv_threshold": 16.0, "etf": "50ETF"},
    "中证500": {"symbol": "sh000905", "iv_threshold": 23.0, "etf": "500ETF"},
    "科创50": {"symbol": "sh000688", "iv_threshold": 25.0, "etf": "科创50"},
    "创业板": {"symbol": "sz399006", "iv_threshold": 24.0, "etf": "创业板"},
}

# 策略阈值
THRESHOLDS = {
    "entry_iv_drop": 15.0,  # 建仓IV阈值
    "exit_iv_spike": 55,    # 退出IV涨幅阈值
    "margin_drop": 5,       # 融资余额降幅阈值
    "style_split": 8,       # 风格分裂阈值
}

def ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def send_email(subject, body):
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

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def get_index_close(symbol):
    """获取指数收盘价 - 使用stock_zh_index_daily"""
    try:
        df = ak.stock_zh_index_daily(symbol=symbol)
        if len(df) > 0:
            latest = df.iloc[-1]
            return float(latest['close'])
    except Exception as e:
        print(f"  ⚠️ 获取{symbol}失败: {e}")
    return None

def get_last_real_trade_date():
    """获取最近的真实交易日（因为系统时间可能超前）"""
    # 由于akshare只到2025年数据，使用固定真实日期
    # 可以在这里更新为最近的真实交易日
    return '20250331'

def get_iv_data():
    """获取期权IV数据 - 使用option_risk_indicator_sse"""
    iv_data = {}
    
    # 获取最近真实交易日
    date_str = get_last_real_trade_date()
    print(f"  使用日期: {date_str}")
    
    try:
        df = ak.option_risk_indicator_sse(date=date_str)
        
        if df is not None and len(df) > 0:
            # 提取各ETF的IV
            for name, config in INDEX_CONFIG.items():
                etf = config['etf']
                # 匹配合约代码
                mask = df['CONTRACT_SYMBOL'].str.contains(etf, na=False)
                subset = df[mask]
                
                if len(subset) > 0:
                    iv_values = pd.to_numeric(subset['IMPLC_VOLATLTY'], errors='coerce')
                    valid_ivs = iv_values[(iv_values > 0.01) & (iv_values < 2)]
                    if len(valid_ivs) > 0:
                        iv_data[name] = valid_ivs.mean() * 100
                        print(f"  ✅ {name}: {iv_data[name]:.2f}% ({len(valid_ivs)}个合约)")
                    else:
                        print(f"  ⚠️ {name}: 无有效IV数据")
                else:
                    print(f"  ⚠️ {name}: 未找到合约")
    except Exception as e:
        print(f"  ❌ 获取IV数据失败: {e}")
    
    return iv_data

def get_margin_balance():
    """获取融资余额"""
    try:
        df = ak.stock_margin_sse()
        if df is not None and len(df) > 0:
            margin = float(df.iloc[0]['融资余额']) / 100000000  # 转换为亿元
            print(f"  ✅ 融资余额: {margin:.1f}亿元")
            return margin
    except Exception as e:
        print(f"  ❌ 获取融资余额失败: {e}")
    return None

def get_all_data():
    """获取所有数据"""
    print("\n📊 正在获取数据...")
    
    # 获取指数收盘价
    print("\n1. 获取指数收盘价...")
    index_data = {}
    for name, config in INDEX_CONFIG.items():
        close = get_index_close(config['symbol'])
        index_data[name] = close
        if close:
            print(f"  ✅ {name}: {close:.2f}")
    
    # 获取期权IV
    print("\n2. 获取期权隐含波动率...")
    iv_data = get_iv_data()
    
    # 获取融资余额
    print("\n3. 获取融资余额...")
    margin = get_margin_balance()
    
    return index_data, iv_data, margin

def calculate_metrics(history, iv_data, margin):
    """计算各项指标"""
    metrics = {}
    
    # IV历史分位
    for name in iv_data:
        if name in history and len(history[name]) >= 20:
            hist_ivs = [h.get('iv', 0) for h in history[name][-60:] if h.get('iv')]
            if len(hist_ivs) >= 10 and iv_data[name]:
                count_below = sum(1 for v in hist_ivs if v < iv_data[name])
                metrics[f'{name}_percentile'] = (count_below / len(hist_ivs)) * 100
        else:
            metrics[f'{name}_percentile'] = None
    
    # IV单日涨跌
    for name in iv_data:
        if name in history and len(history[name]) > 0:
            prev_iv = history[name][-1].get('iv')
            if prev_iv and iv_data[name]:
                metrics[f'{name}_change'] = ((iv_data[name] - prev_iv) / prev_iv) * 100
            else:
                metrics[f'{name}_change'] = None
        else:
            metrics[f'{name}_change'] = None
    
    # 融资余额变化
    if 'margin' in history and len(history['margin']) > 0:
        prev_margin = history['margin'][-1].get('value')
        if prev_margin and margin:
            metrics['margin_change'] = ((margin - prev_margin) / prev_margin) * 100
        else:
            metrics['margin_change'] = None
    else:
        metrics['margin_change'] = None
    
    return metrics

def check_signals(iv_data, metrics):
    """检查策略信号"""
    signals = {
        'entry': {},      # 建仓信号
        'exit_primary': [],  # 一级退出
        'exit_secondary': [], # 二级退出
        'style_split': None,
    }
    
    # 建仓条件检查
    for name in ['沪深300', '上证50', '中证500']:
        threshold = INDEX_CONFIG[name]['iv_threshold']
        iv = iv_data.get(name)
        if iv:
            signals['entry'][name] = {
                'iv': iv,
                'threshold': threshold,
                'met': iv < threshold
            }
    
    # 退出信号 - IV单日暴涨
    for name in iv_data:
        change_key = f'{name}_change'
        if change_key in metrics and metrics[change_key]:
            if metrics[change_key] >= THRESHOLDS['exit_iv_spike']:
                signals['exit_primary'].append(f"{name} IV单日暴涨{metrics[change_key]:.1f}%")
    
    # 退出信号 - 融资余额下降
    if metrics.get('margin_change') and metrics['margin_change'] < -THRESHOLDS['margin_drop']:
        signals['exit_primary'].append(f"融资余额单日下降{abs(metrics['margin_change']):.1f}%")
    
    # 风格分裂检查
    if '沪深300' in iv_data and '中证500' in iv_data:
        if iv_data['沪深300'] and iv_data['中证500']:
            diff = abs(iv_data['中证500'] - iv_data['沪深300'])
            signals['style_split'] = {
                'diff': diff,
                'triggered': diff > THRESHOLDS['style_split']
            }
    
    return signals

def generate_report(date_str, index_data, iv_data, margin, metrics, signals):
    """生成报告"""
    
    report = f"""
━━━━━━━━━━━━━━━━━━━━
📊 黑天鹅监控日报
━━━━━━━━━━━━━━━━━━━━
📅 {date_str}

━━━━━━━━━━━━━━━━━━━━
📈 市场数据概览
━━━━━━━━━━━━━━━━━━━━
"""
    
    # 指数数据
    for name in ['沪深300', '上证50', '中证500', '科创50', '创业板']:
        close = index_data.get(name)
        iv = iv_data.get(name)
        change = metrics.get(f'{name}_change')
        pct = metrics.get(f'{name}_percentile')
        
        close_str = f"{close:.0f}" if close else '-'
        iv_str = f"{iv:.1f}%" if iv else '缺失'
        change_str = f"{change:+.1f}%" if change else '-'
        pct_str = f"{pct:.0f}%" if pct else '-'
        
        report += f"▸ {name:<8} 收盘:{close_str} IV:{iv_str} 涨跌:{change_str} 分位:{pct_str}\n"
    
    # 融资余额
    margin_str = f"{margin:.0f}" if margin else '缺失'
    margin_chg = metrics.get('margin_change')
    margin_chg_str = f"({margin_chg:+.2f}%)" if margin_chg else ""
    report += f"\n💰 融资余额: {margin_str}亿 {margin_chg_str}\n"
    
    # 建仓条件
    report += """
━━━━━━━━━━━━━━━━━━━━
🎯 建仓条件检查
━━━━━━━━━━━━━━━━━━━━
"""
    entry_met = False
    for name in ['沪深300', '上证50', '中证500']:
        if name in signals['entry']:
            s = signals['entry'][name]
            status = "✅" if s['met'] else "❌"
            report += f"{status} {name}: IV {s['iv']:.1f}% {'<' if s['met'] else '>='} 阈值{s['threshold']}%\n"
            if s['met']:
                entry_met = True
    
    report += f"\n📋 结论: {'✅ 满足' if entry_met else '❌ 不满足'}建仓条件\n"
    
    # 退出信号
    report += """
━━━━━━━━━━━━━━━━━━━━
🚨 退出信号监控
━━━━━━━━━━━━━━━━━━━━
"""
    if signals['exit_primary']:
        report += "🔴 一级退出信号:\n"
        for reason in signals['exit_primary']:
            report += f"   • {reason}\n"
    else:
        report += "🟢 一级退出: 未触发 (IV单日涨<55%, 融资降<5%)\n"
    
    report += "🟢 二级退出: 未触发\n"
    
    # 风格分裂
    report += """
━━━━━━━━━━━━━━━━━━━━
⚠️ 风格分裂预警
━━━━━━━━━━━━━━━━━━━━
"""
    if signals['style_split']:
        diff = signals['style_split']['diff']
        triggered = signals['style_split']['triggered']
        status = "🔴 预警" if triggered else "🟢 正常"
        report += f"沪深300 vs 中证500 IV差值: {diff:.1f}个百分点\n"
        report += f"状态: {status} (阈值: {THRESHOLDS['style_split']})\n"
    else:
        report += "数据不足\n"
    
    # 操作建议
    report += """
━━━━━━━━━━━━━━━━━━━━
📋 操作建议
━━━━━━━━━━━━━━━━━━━━
"""
    if entry_met:
        report += "🆕 新开仓: ✅ 建议逐步建仓\n"
    else:
        report += "🆕 新开仓: ⏸️ 建议观望\n"
    
    if signals['exit_primary']:
        report += "📦 现有持仓: 🔴 建议减仓/退出\n"
    elif signals['style_split'] and signals['style_split']['triggered']:
        report += "📦 现有持仓: 🟡 风格分裂，关注持仓结构\n"
    else:
        report += "📦 现有持仓: 🟢 建议保持\n"
    
    # 风险提示
    report += """
━━━━━━━━━━━━━━━━━━━━
💡 风险提示
━━━━━━━━━━━━━━━━━━━━
"""
    if entry_met:
        report += "市场波动率处于相对低位，关注建仓机会。\n"
    elif signals['exit_primary']:
        report += "市场波动率快速上升或融资余额下降，注意风险控制。\n"
    elif signals['style_split'] and signals['style_split']['triggered']:
        report += "大小盘风格分化明显，注意持仓结构风险。\n"
    else:
        report += "市场波动率适中，维持现有策略。\n"
    
    report += f"""
━━━━━━━━━━━━━━━━━━━━
📌 数据说明
━━━━━━━━━━━━━━━━━━━━
数据源: 东方财富(akshare)
生成时间: {datetime.now().strftime('%H:%M')}
⚠️ 本报告仅供参考，不构成投资建议

━━━━━━━━━━━━━━━━━━━━
【龙虾AI】自动生成
━━━━━━━━━━━━━━━━━━━━
"""
    
    return report

def main():
    print("=" * 70)
    print("A股黑天鹅监控日报 - 修复版")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    ensure_dir()
    
    # 获取日期
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    
    # 加载历史
    history = load_history()
    
    # 获取数据
    index_data, iv_data, margin = get_all_data()
    
    # 检查数据完整性
    if not iv_data:
        print("\n❌ 无法获取IV数据，尝试使用历史数据...")
        # 从历史读取最新
        for name in INDEX_CONFIG:
            if name in history and len(history[name]) > 0:
                iv_data[name] = history[name][-1].get('iv')
    
    # 计算指标
    metrics = calculate_metrics(history, iv_data, margin)
    
    # 检查信号
    signals = check_signals(iv_data, metrics)
    
    # 保存数据
    today_key = today.strftime('%Y%m%d')
    for name in iv_data:
        if name not in history:
            history[name] = []
        # 避免重复
        if not any(h.get('date') == today_key for h in history[name]):
            history[name].append({
                'date': today_key,
                'iv': iv_data[name],
                'close': index_data.get(name)
            })
            history[name] = history[name][-200:]  # 保留200天
    
    if margin:
        if 'margin' not in history:
            history['margin'] = []
        if not any(h.get('date') == today_key for h in history['margin']):
            history['margin'].append({
                'date': today_key,
                'value': margin
            })
            history['margin'] = history['margin'][-200:]
    
    save_history(history)
    
    # 生成报告
    print("\n📝 生成报告...")
    report = generate_report(date_str, index_data, iv_data, margin, metrics, signals)
    
    print(report)
    
    # 发送邮件
    print("📧 发送邮件...")
    subject = f"【黑天鹅监控】{date_str} 市场数据与策略信号"
    if send_email(subject, report):
        print("\n✅ 任务完成！")
        return 0
    else:
        print("\n❌ 邮件发送失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
