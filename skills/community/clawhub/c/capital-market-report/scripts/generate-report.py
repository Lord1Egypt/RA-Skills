#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pytz"]
# ///
"""
资本市场简报生成器
始终获取所有数据，根据交易时间判断仅用于显示标注
"""

import subprocess
import sys
import json
from datetime import datetime, time
from typing import Dict, List, Tuple, Optional
import pytz

# 指数配置
INDICES = {
    "A股": [
        ("上证指数", "sh000001"),
        ("科创50", "sh000688"),
        ("创业板指", "sz399006"),
    ],
    "港股": [
        ("恒生指数", "hkHSI"),
        ("恒生科技", "hkHSTECH"),
    ],
    "美股": [
        ("标普500", "usINX"),
        ("纳指100", "usNDX"),
    ],
}

# 交易时间配置 (北京时间)
TRADING_HOURS = {
    "A股": {
        "weekdays": [0, 1, 2, 3, 4],  # 周一到周五
        "sessions": [
            (time(9, 30), time(11, 30)),
            (time(13, 0), time(15, 0)),
        ]
    },
    "港股": {
        "weekdays": [0, 1, 2, 3, 4],
        "sessions": [
            (time(9, 30), time(12, 0)),
            (time(13, 0), time(16, 0)),
        ]
    },
    "美股": {
        "weekdays": [0, 1, 2, 3, 4],
        "sessions": [
            (time(21, 30), time(23, 59, 59)),  # 夏令时
            (time(0, 0), time(4, 0)),  # 次日凌晨
        ],
        "sessions_winter": [
            (time(22, 30), time(23, 59, 59)),  # 冬令时
            (time(0, 0), time(5, 0)),  # 次日凌晨
        ]
    },
}

# 夏令时判断 (3月第二个周日 - 11月第一个周日)
def is_dst(dt: datetime) -> bool:
    """判断是否为夏令时"""
    year = dt.year
    # 3月第二个周日
    dst_start = pytz.timezone('America/New_York').localize(datetime(year, 3, 8 + (6 - datetime(year, 3, 1).weekday()) % 7, 2, 0))
    # 11月第一个周日
    dst_end = pytz.timezone('America/New_York').localize(datetime(year, 11, 1 + (6 - datetime(year, 11, 1).weekday()) % 7, 2, 0))
    # 转换为北京时间进行比较
    tz = pytz.timezone('Asia/Shanghai')
    dt_utc = dt.astimezone(pytz.UTC)
    return dst_start.astimezone(pytz.UTC) <= dt_utc < dst_end.astimezone(pytz.UTC)

def is_market_open(market: str, dt: datetime) -> bool:
    """判断市场是否开盘（仅用于显示标注）"""
    if market not in TRADING_HOURS:
        return False
    
    config = TRADING_HOURS[market]
    weekday = dt.weekday()
    
    # 检查是否为交易日
    if weekday not in config["weekdays"]:
        return False
    
    current_time = dt.time()
    
    # 美股特殊处理夏令时/冬令时
    if market == "美股":
        if is_dst(dt):
            sessions = config["sessions"]
        else:
            sessions = config.get("sessions_winter", config["sessions"])
    else:
        sessions = config["sessions"]
    
    # 检查是否在交易时段内
    for start, end in sessions:
        if start <= current_time <= end:
            return True
    
    return False

def get_beijing_time() -> datetime:
    """获取北京时间"""
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz)

def get_stock_data() -> Dict[str, Dict]:
    """获取所有股价数据（始终获取，不管市场是否开盘）"""
    # 构建代码到显示名称的映射
    code_to_name = {}
    all_codes = []
    for market, stocks in INDICES.items():
        for display_name, code in stocks:
            code_to_name[code] = display_name
            all_codes.append(display_name)  # query_stock.py 支持名称查询
    
    # 调用腾讯财经API
    script_path = "~/.openclaw/skills/tencent-finance-stock-price/scripts/query_stock.py"
    cmd = f"uv run {script_path} {' '.join(all_codes)}"
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        # 解析输出 - 按顺序匹配
        lines = result.stdout.strip().split('\n')[2:]  # 跳过表头
        data = {}
        code_list = list(code_to_name.keys())
        for i, line in enumerate(lines):
            parts = line.split()
            if len(parts) >= 5:
                # 使用原始查询顺序的显示名称作为key
                if i < len(all_codes):
                    key = all_codes[i]
                else:
                    key = parts[0]
                price = parts[2]
                change = parts[3]
                # Fix: percentage includes both emoji and number
                pct = parts[4] + " " + parts[5] if len(parts) >= 6 else parts[4]
                data[key] = {
                    "price": price,
                    "change": change,
                    "pct": pct,
                }
        return data
    except Exception as e:
        return {"error": str(e)}

def get_crypto_price(symbol: str = "BTC") -> Dict:
    """获取加密货币价格"""
    script_path = "~/.openclaw/workspace-group/skills/cryptoprice/scripts/cryptoprice.py"
    cmd = f"uv run {script_path} {symbol}"
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        # 解析: "Bitcoin (BTC): $67,947.09"
        line = result.stdout.strip()
        if "$" in line:
            price = line.split("$")[1].strip()
            return {"symbol": symbol, "price": price}
        return {"error": "parse failed"}
    except Exception as e:
        return {"error": str(e)}

def format_report(stock_data: Dict, crypto_data: Dict) -> str:
    """格式化报告，交易时间判断仅用于显示标注"""
    now = get_beijing_time()
    time_str = now.strftime("%Y-%m-%d %H:%M")
    
    # 判断各市场状态（仅用于显示标注）
    market_status = {}
    for market in ["A股", "港股", "美股"]:
        market_status[market] = is_market_open(market, now)
    
    report = f"""📊 资本市场简报 | {time_str}

---
"""
    
    # 按市场分类显示
    for market in ["A股", "港股", "美股"]:
        is_open = market_status[market]
        status_icon = "🟢" if is_open else "🔴"
        status_text = "交易中" if is_open else "休市"
        
        report += f"\n### {status_icon} {market}（{status_text}）\n"
        
        if market in INDICES:
            for name, code in INDICES[market]:
                if name in stock_data and "error" not in stock_data:
                    d = stock_data[name]
                    report += f"• {name}：{d['price']}点 ({d['change']} / {d['pct']})\n"
                else:
                    report += f"• {name}：[获取失败]\n"
    
    # 大宗商品（24小时交易）
    report += "\n### 🟢 大宗商品（24小时交易）\n"
    report += "• 黄金：[使用 web_search 获取实时价格]\n"
    report += "• 原油(WTI)：[使用 web_search 获取实时价格]\n"
    
    if crypto_data.get("price"):
        report += f"• 比特币：${crypto_data['price']}\n"
    else:
        report += "• 比特币：[获取失败]\n"
    
    report += """
---

### 📰 24小时要闻速览

#### 🔴 利空
[从以下媒体抓取利空新闻]
- 中文：36氪、新浪财经、财联社
- 英文：BBC、Bloomberg、Yahoo Finance、WSJ

#### 🟢 利好
[从以下媒体抓取利好新闻]

#### ⚪ 中性
[从以下媒体抓取中性新闻]

每条新闻格式：
1. **标题**
   📰 来源 | 时间
   摘要

---

### 📡 信息来源
中文媒体：36氪、新浪财经、财联社、人民网
国际媒体：BBC、Bloomberg、Yahoo Finance、WSJ

---

"""
    
    # 添加交易时间说明
    report += "⏰ **交易时间参考**（北京时间）：\n"
    report += "• A股：09:30-11:30, 13:00-15:00（周一至周五）\n"
    report += "• 港股：09:30-12:00, 13:00-16:00（周一至周五）\n"
    report += "• 美股：21:30-04:00（夏令时）/ 22:30-05:00（冬令时）\n"
    report += "• 大宗商品/加密货币：24小时交易\n"
    
    return report

def main():
    """主函数"""
    beijing_now = get_beijing_time()
    print(f"当前北京时间: {beijing_now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"夏令时: {'是' if is_dst(beijing_now) else '否'}")
    
    # 检查各市场状态（仅用于显示）
    for market in ["A股", "港股", "美股"]:
        status = "交易中" if is_market_open(market, beijing_now) else "休市"
        print(f"{market}: {status}")
    
    print("\n正在获取数据...")
    
    # 始终获取所有数据
    stock_data = get_stock_data()
    crypto_data = get_crypto_price("BTC")
    
    report = format_report(stock_data, crypto_data)
    print("\n" + "="*50)
    print(report)

if __name__ == "__main__":
    main()
