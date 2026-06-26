#!/usr/bin/env python3
"""
历史日报查询脚本 - 双模式版
模式1: 查询历史股价数据（如果接口可用）
模式2: 查询已保存的历史报告文件
"""

import sys
import argparse
import requests
import os
from datetime import datetime
from typing import Optional, Dict

# 报告保存目录
REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def get_tencent_historical(symbol: str, date_str: str) -> Optional[Dict]:
    """从腾讯财经获取历史数据"""
    try:
        url = f"http://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
        params = {'param': f"{symbol},day,{date_str},{date_str},1,qfq"}
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        key = f"{symbol}"
        if key in data.get('data', {}):
            klines = data['data'][key].get('day', [])
            if klines:
                k = klines[0]
                return {
                    'date': k[0],
                    'open': float(k[1]),
                    'close': float(k[2]),
                    'low': float(k[3]),
                    'high': float(k[4]),
                    'volume': float(k[5])
                }
        return None
    except:
        return None


def check_saved_report(date_str: str) -> Optional[str]:
    """检查是否有保存的历史报告"""
    filename = f"report_{date_str.replace('-', '')}.txt"
    filepath = os.path.join(REPORTS_DIR, filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def save_report(date_str: str, content: str):
    """保存报告到文件"""
    filename = f"report_{date_str.replace('-', '')}.txt"
    filepath = os.path.join(REPORTS_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath


def analyze_historical_stance(changes: list) -> str:
    """基于涨跌幅分析市场立场"""
    if not changes:
        return "➡️ 数据缺失"
    
    avg_change = sum(changes) / len(changes)
    
    if avg_change > 1.5:
        return "🔥 强势上涨"
    elif avg_change > 0.5:
        return "📈 震荡上行"
    elif avg_change > -0.5:
        return "➡️ 横盘震荡"
    elif avg_change > -1.5:
        return "📉 震荡偏弱"
    else:
        return "❄️ 明显下跌"


def generate_historical_report(date_str: str, use_online: bool = True) -> str:
    """生成历史日报"""
    # 验证日期
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        date_nodash = date_str.replace("-", "")
    except ValueError:
        return "❌ 日期格式错误，请使用 YYYY-MM-DD"
    
    # 检查周末
    if target_date.weekday() >= 5:
        return f"⚠️ {date_str} 是周末，股市休市"
    
    # 检查未来日期
    if target_date > datetime.now():
        return "❌ 不能查询未来日期"
    
    # 先检查是否有保存的报告
    saved = check_saved_report(date_str)
    if saved:
        return f"📂 找到已保存的报告 ({date_str}):\n\n{saved}"
    
    if not use_online:
        return f"❌ 未找到 {date_str} 的保存报告，且在线查询已禁用"
    
    # 尝试在线获取数据
    print(f"🔍 正在查询 {date_str} 的历史数据...")
    
    sh_data = get_tencent_historical("sh000001", date_nodash)
    sz_data = get_tencent_historical("sz399001", date_nodash)
    cy_data = get_tencent_historical("sz399006", date_nodash)
    
    if sh_data is None and sz_data is None:
        return f"""❌ 无法获取 {date_str} 的在线数据

可能原因：
• 该日期为非交易日（节假日）
• 网络连接不稳定
• 数据源暂时不可用

💡 提示：
• 每日运行 market_brief.py 时会自动保存报告
• 之后可通过本脚本查询已保存的历史报告"""
    
    # 计算数据
    changes = []
    lines = [f"📊 A股历史日报 - {date_str}", "━━━━━━━━━━━━━━━━━━━━", ""]
    
    if sh_data:
        changes.append((sh_data['close'] - sh_data['open']) / sh_data['open'] * 100)
        pct = changes[-1]
        sign = "+" if pct >= 0 else ""
        trend = "📈" if pct > 0 else "📉" if pct < 0 else "➡️"
        lines.append(f"上证指数: {sh_data['close']:.2f} ({sign}{pct:.2f}%) {trend}")
    
    if sz_data:
        changes.append((sz_data['close'] - sz_data['open']) / sz_data['open'] * 100)
        pct = changes[-1]
        sign = "+" if pct >= 0 else ""
        trend = "📈" if pct > 0 else "📉" if pct < 0 else "➡️"
        lines.append(f"深证成指: {sz_data['close']:.2f} ({sign}{pct:.2f}%) {trend}")
    
    if cy_data:
        changes.append((cy_data['close'] - cy_data['open']) / cy_data['open'] * 100)
        pct = changes[-1]
        sign = "+" if pct >= 0 else ""
        trend = "📈" if pct > 0 else "📉" if pct < 0 else "➡️"
        lines.append(f"创业板指: {cy_data['close']:.2f} ({sign}{pct:.2f}%) {trend}")
    
    lines.extend([
        "",
        f"【市场立场】{analyze_historical_stance(changes)}",
        "",
        "💡 提示: 历史数据仅供参考"
    ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='查询历史A股日报')
    parser.add_argument('--date', '-d', required=True, help='日期: YYYY-MM-DD')
    parser.add_argument('--offline', action='store_true', help='仅查询已保存的报告')
    parser.add_argument('--save', '-s', action='store_true', help='保存报告')
    
    args = parser.parse_args()
    
    report = generate_historical_report(args.date, use_online=not args.offline)
    print(report)
    
    # 保存报告
    if args.save and not report.startswith("❌") and not report.startswith("⚠️"):
        filepath = save_report(args.date, report)
        print(f"\n💾 报告已保存: {filepath}")


if __name__ == "__main__":
    main()
