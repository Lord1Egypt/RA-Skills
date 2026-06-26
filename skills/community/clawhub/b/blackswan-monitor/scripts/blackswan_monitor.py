#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股黑天鹅对冲策略监控日报
基于改进版塔勒布期权策略的建仓、退出及风控规则
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback
import socket
import urllib.request

# 设置全局超时
socket.setdefaulttimeout(30)

# ============ 配置 ============
EMAIL_CONFIG = {
    "smtp_server": "smtp.qq.com",
    "smtp_port": 587,
    "from_email": "57189896@qq.com",
    "to_email": "57189896@qq.com",
    "auth_code": "dskokcscwmkdbhjg"
}

# 飞书配置（需要用户配置）
FEISHU_CONFIG = {
    "webhook": os.getenv("FEISHU_WEBHOOK", "")
}

# 数据文件路径
DATA_DIR = "/root/.openclaw/workspace/blackswan_data"
HISTORY_FILE = os.path.join(DATA_DIR, "iv_history.json")
STATE_FILE = os.path.join(DATA_DIR, "strategy_state.json")
MARGIN_FILE = os.path.join(DATA_DIR, "margin_history.json")

# 指数配置
INDEX_CONFIG = {
    "沪深300": {"symbol": "000300", "iv_threshold": 15.5, "exchange": "sse"},
    "上证50": {"symbol": "000016", "iv_threshold": 16.0, "exchange": "sse"},
    "中证500": {"symbol": "000905", "iv_threshold": 23.0, "exchange": "cffex"},
    "创业板": {"symbol": "399006", "iv_threshold": 20.0, "exchange": "szse"},  # 使用固定阈值
    "科创50": {"symbol": "000688", "iv_threshold": 25.0, "exchange": "sse"},
}

# 策略参数
STRATEGY_PARAMS = {
    "primary_exit_iv_rise": 55,  # 一级退出：IV单日涨幅≥55%
    "primary_exit_margin_drop": 5,  # 一级退出：融资余额单日降幅>5%
    "secondary_exit_iv_rise": 30,  # 二级退出：IV续涨≥30%
    "secondary_exit_margin_drop": 8,  # 二级退出：融资累计降幅>8%
    "style_divergence_threshold": 8,  # 风格分裂阈值：8个百分点
    "history_window": 250,  # 历史分位计算窗口
    "secondary_window": 3,  # 二级退出判断窗口（交易日）
}


def ensure_data_dir():
    """确保数据目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)


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
        return True, None
    except Exception as e:
        error_msg = f"❌ 邮件发送失败: {str(e)}"
        print(error_msg)
        # 记录详细错误到日志文件
        log_error(f"Email send failed: {str(e)}\n{traceback.format_exc()}")
        return False, str(e)


def log_error(error_text):
    """记录错误日志"""
    try:
        log_file = os.path.join(DATA_DIR, "error.log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"[{timestamp}] ERROR:\n")
            f.write(error_text)
            f.write("\n")
    except Exception as e:
        print(f"❌ 写入错误日志失败: {e}")


def send_feishu_backup(report):
    """飞书webhook备份发送"""
    webhook = FEISHU_CONFIG.get('webhook', '')
    if not webhook:
        print("⚠️ 飞书webhook未配置，跳过备份发送")
        return False
    
    try:
        import urllib.request
        import json
        
        payload = {
            "msg_type": "text",
            "content": {
                "text": f"【黑天鹅监控备份】\n\n{report[:2000]}..."  # 限制长度
            }
        }
        
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(payload).encode('utf-8')
        
        req = urllib.request.Request(webhook, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                print("✅ 飞书备份发送成功")
                return True
            else:
                print(f"❌ 飞书备份发送失败: {result}")
                return False
    except Exception as e:
        print(f"❌ 飞书备份发送失败: {e}")
        return False


def get_last_trade_date():
    """获取最近交易日（T-1）"""
    today = datetime.now()
    # 简单回退逻辑
    weekday = today.weekday()
    if weekday == 0:  # 周一，回退到上周五
        days_back = 3
    elif weekday == 6:  # 周日，回退到上周五
        days_back = 2
    else:
        days_back = 1
    
    trade_date = today - timedelta(days=days_back)
    return trade_date.strftime("%Y%m%d"), trade_date.strftime("%Y-%m-%d")


def get_index_close(symbol, date_str):
    """获取指数收盘价 - 带超时保护"""
    try:
        # 使用akshare获取指数历史数据，设置超时
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("获取指数数据超时")
        
        # 设置30秒超时
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)
        
        try:
            df = ak.index_zh_a_hist(symbol=symbol, period="daily", 
                                   start_date=date_str, end_date=date_str)
            signal.alarm(0)  # 取消超时
            
            if df is not None and len(df) > 0:
                close = float(df.iloc[0]['收盘'])
                return close
        except TimeoutError:
            print(f"  ⚠️ 获取指数{symbol}超时，使用历史数据")
            return None
        except Exception as e:
            signal.alarm(0)
            print(f"  获取指数{symbol}收盘价失败: {e}")
            return None
            
    except Exception as e:
        print(f"  获取指数{symbol}收盘价失败: {e}")
        return None


def get_iv_data(date_str):
    """获取各指数期权隐含波动率 - 带超时保护"""
    iv_data = {}
    
    # 尝试从风险指标获取IV，带超时
    try:
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("获取IV数据超时")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(45)  # 45秒超时
        
        try:
            df = ak.option_risk_indicator_sse(date=date_str)
            signal.alarm(0)
            
            if df is not None and len(df) > 0:
                def extract_underlying(symbol):
                    if '300ETF' in symbol:
                        return '沪深300'
                    elif '50ETF' in symbol and '500' not in symbol:
                        return '上证50'
                    elif '500ETF' in symbol:
                        return '中证500'
                    elif '科创50' in symbol or '588000' in symbol:
                        return '科创50'
                    return None
                
                df['underlying'] = df['CONTRACT_SYMBOL'].apply(extract_underlying)
                
                for name in ['沪深300', '上证50', '中证500', '科创50']:
                    subset = df[df['underlying'] == name]
                    if len(subset) > 0:
                        iv_values = pd.to_numeric(subset['IMPLC_VOLATLTY'], errors='coerce')
                        valid_ivs = iv_values[(iv_values > 0.01) & (iv_values < 1)]
                        if len(valid_ivs) > 0:
                            iv_data[name] = valid_ivs.mean() * 100
        except TimeoutError:
            print("  ⚠️ 获取IV数据超时，使用历史数据")
            # 从历史数据获取最近一次有效值
            history = load_history()
            for name in ['沪深300', '上证50', '中证500', '科创50']:
                if name in history and len(history[name]) > 0:
                    iv_data[name] = history[name][-1].get('iv')
                    print(f"  使用历史{name} IV: {iv_data[name]:.2f}%" if iv_data[name] else f"  {name}无历史数据")
        except Exception as e:
            signal.alarm(0)
            print(f"  获取上交所期权IV失败: {e}")
            
    except Exception as e:
        print(f"  获取期权IV失败: {e}")
    
    # 创业板IV通常获取困难，标记为None
    iv_data['创业板'] = None
    
    return iv_data


def get_margin_balance():
    """获取融资余额（单位：亿元）- 带超时保护"""
    try:
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("获取融资余额超时")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)  # 30秒超时
        
        try:
            # 使用akshare获取融资融券数据
            df = ak.stock_margin_sse()
            signal.alarm(0)
            
            if df is not None and len(df) > 0:
                # 获取最新一天的融资余额
                margin = float(df.iloc[0]['融资余额']) / 100000000  # 转换为亿元
                return margin
        except TimeoutError:
            print("  ⚠️ 获取融资余额超时，使用历史数据")
            history = load_history()
            if 'margin' in history and len(history['margin']) > 0:
                return history['margin'][-1].get('value')
        except Exception as e:
            signal.alarm(0)
            print(f"  获取融资余额失败: {e}")
            return None
            
    except Exception as e:
        print(f"  获取融资余额失败: {e}")
        return None


def load_history():
    """加载IV历史数据"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_history(history):
    """保存IV历史数据"""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"保存历史数据失败: {e}")


def load_state():
    """加载策略状态"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {
        "last_primary_trigger_date": None,
        "primary_trigger_iv": {},
        "primary_trigger_margin": None,
        "has_issued_secondary": False
    }


def save_state(state):
    """保存策略状态"""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"保存状态失败: {e}")


def calculate_iv_percentile(current_iv, history, name, window=250):
    """计算IV历史分位数"""
    if name not in history or len(history[name]) < 30:
        return None
    
    hist_ivs = [h.get("iv", 0) for h in history[name][-window:] if h.get("iv")]
    if len(hist_ivs) < 30:
        return None
    
    percentile = (sum(1 for h in hist_ivs if h <= current_iv) / len(hist_ivs)) * 100
    return percentile


def check_entry_conditions(iv_data, history):
    """检查建仓条件"""
    conditions = {}
    
    for name, config in INDEX_CONFIG.items():
        if name not in iv_data or iv_data[name] is None:
            conditions[name] = {"met": False, "reason": "数据缺失"}
            continue
        
        iv = iv_data[name]
        threshold = config["iv_threshold"]
        
        if name in ['创业板', '科创50']:
            # 使用历史分位数（如果可用）
            percentile = calculate_iv_percentile(iv, history, name)
            if percentile is not None:
                met = percentile < 25
                conditions[name] = {
                    "met": met,
                    "iv": iv,
                    "threshold": f"25%分位",
                    "percentile": percentile,
                    "reason": f"IV={iv:.1f}%, 分位={percentile:.0f}%"
                }
            else:
                # 使用固定阈值
                met = iv < threshold
                conditions[name] = {
                    "met": met,
                    "iv": iv,
                    "threshold": f"{threshold}%",
                    "reason": f"IV={iv:.1f}% {'<' if met else '>='} {threshold}% (固定阈值)"
                }
        else:
            # 使用固定阈值
            met = iv < threshold
            conditions[name] = {
                "met": met,
                "iv": iv,
                "threshold": f"{threshold}%",
                "reason": f"IV={iv:.1f}% {'<' if met else '>='} {threshold}%"
            }
    
    # 综合判断
    core_met = all(conditions[name]["met"] for name in ['沪深300', '上证50', '中证500'])
    optional_met = all(conditions[name].get("met", True) for name in ['创业板', '科创50'])
    
    return conditions, core_met and optional_met


def check_exit_signals(iv_data, prev_iv_data, margin, prev_margin, state, date_str):
    """检查退出信号"""
    signals = {
        "primary": False,
        "secondary": False,
        "primary_reasons": [],
        "secondary_reasons": []
    }
    
    # 计算IV单日涨幅
    iv_changes = {}
    for name in iv_data:
        if iv_data[name] is not None and name in prev_iv_data and prev_iv_data[name] is not None:
            change = (iv_data[name] - prev_iv_data[name]) / prev_iv_data[name] * 100
            iv_changes[name] = change
            
            # 一级退出：IV单日涨幅≥55%
            if change >= STRATEGY_PARAMS["primary_exit_iv_rise"]:
                signals["primary"] = True
                signals["primary_reasons"].append(f"{name} IV单日涨幅{change:.1f}%≥55%")
    
    # 一级退出：融资余额单日降幅>5%
    if margin is not None and prev_margin is not None and prev_margin > 0:
        margin_change = (margin - prev_margin) / prev_margin * 100
        if margin_change < -STRATEGY_PARAMS["primary_exit_margin_drop"]:
            signals["primary"] = True
            signals["primary_reasons"].append(f"融资余额单日降幅{abs(margin_change):.1f}%>{STRATEGY_PARAMS['primary_exit_margin_drop']}%")
    
    # 更新一级触发状态
    if signals["primary"]:
        if state["last_primary_trigger_date"] != date_str:
            state["last_primary_trigger_date"] = date_str
            state["primary_trigger_iv"] = iv_data.copy()
            state["primary_trigger_margin"] = margin
            state["has_issued_secondary"] = False
            save_state(state)
    
    # 检查二级退出信号
    if state["last_primary_trigger_date"] is not None and not state["has_issued_secondary"]:
        # 计算距离一级触发的交易日数
        last_trigger = datetime.strptime(state["last_primary_trigger_date"], "%Y-%m-%d")
        current = datetime.strptime(date_str, "%Y-%m-%d")
        days_diff = (current - last_trigger).days
        
        if days_diff <= STRATEGY_PARAMS["secondary_window"]:
            # 二级退出：IV续涨≥30%
            for name in iv_data:
                if iv_data[name] is not None and name in state["primary_trigger_iv"]:
                    if state["primary_trigger_iv"][name] is not None and state["primary_trigger_iv"][name] > 0:
                        rise_from_primary = (iv_data[name] - state["primary_trigger_iv"][name]) / state["primary_trigger_iv"][name] * 100
                        if rise_from_primary >= STRATEGY_PARAMS["secondary_exit_iv_rise"]:
                            signals["secondary"] = True
                            signals["secondary_reasons"].append(f"{name} IV自一级触发后上涨{rise_from_primary:.1f}%≥30%")
            
            # 二级退出：融资余额累计降幅>8%
            if margin is not None and state["primary_trigger_margin"] is not None and state["primary_trigger_margin"] > 0:
                cumulative_drop = (state["primary_trigger_margin"] - margin) / state["primary_trigger_margin"] * 100
                if cumulative_drop > STRATEGY_PARAMS["secondary_exit_margin_drop"]:
                    signals["secondary"] = True
                    signals["secondary_reasons"].append(f"融资余额累计降幅{cumulative_drop:.1f}%>{STRATEGY_PARAMS['secondary_exit_margin_drop']}%")
            
            if signals["secondary"]:
                state["has_issued_secondary"] = True
                save_state(state)
        else:
            # 超过3个交易日，清除状态
            state["last_primary_trigger_date"] = None
            state["primary_trigger_iv"] = {}
            state["primary_trigger_margin"] = None
            state["has_issued_secondary"] = False
            save_state(state)
    
    return signals


def check_style_divergence(iv_data):
    """检查风格分裂"""
    if '沪深300' not in iv_data or '上证50' not in iv_data:
        return None, False
    
    if iv_data['沪深300'] is None or iv_data['上证50'] is None:
        return None, False
    
    diff = iv_data['沪深300'] - iv_data['上证50']
    has_divergence = abs(diff) > STRATEGY_PARAMS["style_divergence_threshold"]
    
    return diff, has_divergence


def generate_report(date_str, date_display, index_data, iv_data, margin, 
                   entry_conditions, entry_met, exit_signals, style_diff, has_divergence,
                   history, prev_iv_data):
    """生成监控日报 - 手机优化版"""
    
    # 计算IV单日涨幅
    iv_changes = {}
    for name in iv_data:
        if iv_data[name] is not None and name in prev_iv_data and prev_iv_data[name] is not None:
            iv_changes[name] = (iv_data[name] - prev_iv_data[name]) / prev_iv_data[name] * 100
        else:
            iv_changes[name] = None
    
    # 计算IV历史分位
    iv_percentiles = {}
    for name in iv_data:
        if iv_data[name] is not None:
            iv_percentiles[name] = calculate_iv_percentile(iv_data[name], history, name)
        else:
            iv_percentiles[name] = None
    
    # 计算融资余额变化
    margin_change = None
    if margin is not None and len(history.get("margin", [])) > 0:
        prev_margin = history["margin"][-1].get("value")
        if prev_margin is not None:
            margin_change = (margin - prev_margin) / prev_margin * 100
    
    # 构建手机优化报告
    report = f"""📊 黑天鹅监控日报
📅 {date_display}

━━━━━━━━━━━━━━━━━━━━
📈 市场数据概览
━━━━━━━━━━━━━━━━━━━━

"""
    
    # 市场数据 - 简洁格式
    for name in ['沪深300', '上证50', '中证500', '创业板', '科创50']:
        close = index_data.get(name)
        iv = iv_data.get(name)
        change = iv_changes.get(name)
        percentile = iv_percentiles.get(name)
        
        close_str = f"{close:.0f}" if close is not None else '-'
        iv_str = f"{iv:.1f}%" if iv is not None else '缺失'
        change_str = f"{change:+.1f}%" if change is not None else '-'
        percentile_str = f"{percentile:.0f}%" if percentile is not None else '-'
        
        report += f"▸ {name}\n"
        report += f"  收盘: {close_str} | IV: {iv_str}\n"
        report += f"  涨跌: {change_str} | 分位: {percentile_str}\n\n"
    
    margin_str = f"{margin:.0f}" if margin is not None else '缺失'
    margin_change_str = f"{margin_change:+.2f}%" if margin_change is not None else '-'
    report += f"💰 融资余额: {margin_str}亿 ({margin_change_str})\n"
    
    # 建仓条件判断
    report += f"""
━━━━━━━━━━━━━━━━━━━━
🎯 建仓条件检查
━━━━━━━━━━━━━━━━━━━━

"""
    for name in ['沪深300', '上证50', '中证500']:
        cond = entry_conditions.get(name, {})
        met = "✅" if cond.get("met") else "❌"
        iv_val = cond.get('iv', 0)
        threshold = cond.get('threshold', '-')
        report += f"{met} {name}: {iv_val:.1f}% < {threshold}\n"
    
    for name in ['创业板', '科创50']:
        cond = entry_conditions.get(name, {})
        if cond.get("percentile") is not None:
            met = "✅" if cond.get("met") else "❌"
            iv_val = cond.get('iv', 0)
            pct = cond.get('percentile', 0)
            report += f"{met} {name}: {iv_val:.1f}% (分位{pct:.0f}%)\n"
        else:
            met = "✅" if cond.get("met") else "❌"
            iv_val = cond.get('iv', 0) if cond.get('iv') else 0
            threshold = cond.get('threshold', '-')
            if cond.get('iv') is not None:
                report += f"{met} {name}: {iv_val:.1f}% < {threshold} (固定)\n"
            else:
                report += f"❌ {name}: 数据缺失\n"
    
    entry_conclusion = "✅ 满足" if entry_met else "❌ 不满足"
    report += f"\n📋 结论: {entry_conclusion}建仓条件\n"
    
    # 退出信号监控
    report += f"""
━━━━━━━━━━━━━━━━━━━━
🚨 退出信号监控
━━━━━━━━━━━━━━━━━━━━

"""
    if exit_signals["primary"]:
        report += "🔴 一级退出: 触发\n"
        for reason in exit_signals["primary_reasons"]:
            report += f"   {reason}\n"
        report += "\n💡 建议: 平仓50%持仓\n"
    else:
        report += "🟢 一级退出: 未触发\n"
        report += "   (IV涨≥55% 或 融资降>5%)\n"
    
    if exit_signals["secondary"]:
        report += "\n🔴 二级退出: 触发\n"
        for reason in exit_signals["secondary_reasons"]:
            report += f"   {reason}\n"
        report += "\n💡 建议: 清仓剩余50%\n"
    else:
        report += "\n🟢 二级退出: 未触发\n"
        report += "   (一级后IV涨≥30% 或 融资累计降>8%)\n"
    
    # 风格分裂预警
    report += f"""
━━━━━━━━━━━━━━━━━━━━
⚠️ 风格分裂预警
━━━━━━━━━━━━━━━━━━━━

"""
    if style_diff is not None:
        divergence_status = "🔴 存在" if has_divergence else "🟢 无"
        report += f"差值: {style_diff:.1f}个百分点\n"
        report += f"阈值: {STRATEGY_PARAMS['style_divergence_threshold']} | 状态: {divergence_status}\n"
        if has_divergence:
            report += "\n💡 建议: 暂停新开仓\n"
    else:
        report += "数据不足\n"
    
    # 操作建议摘要
    report += f"""
━━━━━━━━━━━━━━━━━━━━
📋 操作建议
━━━━━━━━━━━━━━━━━━━━

"""
    if entry_met:
        report += "🆕 新开仓: ✅ 建议开仓\n"
    else:
        report += "🆕 新开仓: ⏸️ 建议观望\n"
    
    if exit_signals["secondary"]:
        report += "📦 现有持仓: 🔴 建议清仓\n"
    elif exit_signals["primary"]:
        report += "📦 现有持仓: 🟡 建议减仓50%\n"
    else:
        report += "📦 现有持仓: 🟢 建议保持\n"
    
    # 风险提示
    report += f"""
━━━━━━━━━━━━━━━━━━━━
💡 风险提示
━━━━━━━━━━━━━━━━━━━━

"""
    if not entry_met and not exit_signals["primary"]:
        report += "市场波动率适中，维持现有策略。"
    elif exit_signals["primary"]:
        report += "市场波动率快速上升或融资余额骤降，注意风险控制！"
    elif entry_met:
        report += "市场波动率处于低位，可考虑逐步建仓。"
    
    report += f"""

━━━━━━━━━━━━━━━━━━━━
祝投资顺利！
【龙虾AI】自动生成，仅供参考
生成时间: {datetime.now().strftime("%H:%M")}
"""
    
    return report


def main():
    """主函数"""
    print("=" * 70)
    print("A股黑天鹅对冲策略监控日报")
    print(f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    try:
        ensure_data_dir()
        
        # 获取日期
        date_str, date_display = get_last_trade_date()
        print(f"\n监控日期：{date_display} (T-1日)")
        
        # 加载历史数据和状态
        history = load_history()
        state = load_state()
        
        # 获取指数收盘价
        print("\n📊 正在获取指数收盘价...")
        index_data = {}
        for name, config in INDEX_CONFIG.items():
            close = get_index_close(config["symbol"], date_str)
            index_data[name] = close
            print(f"  {name}: {close:.2f}" if close else f"  {name}: 获取失败")
        
        # 获取期权IV数据
        print("\n📊 正在获取期权隐含波动率...")
        iv_data = get_iv_data(date_str)
        for name, iv in iv_data.items():
            print(f"  {name}: {iv:.2f}%" if iv else f"  {name}: 获取失败")
        
        # 获取融资余额
        print("\n📊 正在获取融资余额...")
        margin = get_margin_balance()
        print(f"  融资余额: {margin:.1f}亿元" if margin else "  融资余额: 获取失败")
        
        # 保存当前数据到历史
        if date_str not in [h.get("date") for h in history.get("沪深300", [])]:
            for name in iv_data:
                if name not in history:
                    history[name] = []
                history[name].append({
                    "date": date_str,
                    "iv": iv_data[name],
                    "close": index_data.get(name)
                })
                # 只保留最近300天
                history[name] = history[name][-300:]
        
        if margin is not None:
            if "margin" not in history:
                history["margin"] = []
            history["margin"].append({
                "date": date_str,
                "value": margin
            })
            history["margin"] = history["margin"][-300:]
        
        save_history(history)
        
        # 获取前一日IV数据（用于计算涨幅）
        prev_iv_data = {}
        for name in iv_data:
            if name in history and len(history[name]) >= 2:
                prev_iv_data[name] = history[name][-2].get("iv")
            else:
                prev_iv_data[name] = None
        
        # 检查建仓条件
        print("\n🔍 正在检查建仓条件...")
        entry_conditions, entry_met = check_entry_conditions(iv_data, history)
        print(f"  建仓条件: {'满足' if entry_met else '不满足'}")
        
        # 检查退出信号
        print("\n🔍 正在检查退出信号...")
        prev_margin = history["margin"][-2].get("value") if "margin" in history and len(history["margin"]) >= 2 else None
        exit_signals = check_exit_signals(iv_data, prev_iv_data, margin, prev_margin, state, date_display)
        print(f"  一级退出: {'触发' if exit_signals['primary'] else '未触发'}")
        print(f"  二级退出: {'触发' if exit_signals['secondary'] else '未触发'}")
        
        # 检查风格分裂
        print("\n🔍 正在检查风格分裂...")
        style_diff, has_divergence = check_style_divergence(iv_data)
        print(f"  IV差值: {style_diff:.1f}个百分点" if style_diff else "  无法计算")
        print(f"  风格分裂: {'存在' if has_divergence else '不存在'}")
        
        # 生成报告
        print("\n📝 正在生成报告...")
        report = generate_report(
            date_str, date_display, index_data, iv_data, margin,
            entry_conditions, entry_met, exit_signals, style_diff, has_divergence,
            history, prev_iv_data
        )
        
        # 发送邮件
        print("\n📧 正在发送邮件...")
        subject = f"【黑天鹅监控】{date_display} 市场数据与策略信号"
        email_sent, email_error = send_email(subject, report)
        
        # 邮件失败时，尝试飞书备份
        if not email_sent:
            print("⚠️ 邮件发送失败，尝试飞书备份...")
            send_feishu_backup(report)
        
        # 打印报告
        print("\n" + "=" * 70)
        print(report)
        print("=" * 70)
        
        # 记录执行结果
        if email_sent:
            print("\n✅ 任务执行完成！邮件发送成功")
        else:
            print(f"\n⚠️ 任务执行完成，但邮件发送失败: {email_error}")
        
    except Exception as e:
        error_msg = f"任务执行出错: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        log_error(error_msg)
        # 尝试发送错误邮件
        try:
            send_email(f"【黑天鹅监控】执行出错 - {datetime.now().strftime('%Y-%m-%d')}", error_msg)
        except:
            pass


if __name__ == "__main__":
    main()
