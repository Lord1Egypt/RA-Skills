#!/usr/bin/env python3
"""每日自选股报告生成脚本 - 含KDJ指标
用法：python3 daily_report.py "股票代码:名称,股票代码:名称,..."
示例：python3 daily_report.py "1A0001:上证指数,600036:招商银行,000858:五粮液"
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
import ssl
import sys

def parse_stocks(stocks_str: str) -> dict:
    """解析用户提供的股票列表"""
    stocks = {}
    if not stocks_str:
        print("错误：请提供股票列表")
        print("用法：python3 daily_report.py \"1A0001:上证指数,600036:招商银行\"")
        sys.exit(1)
    
    items = stocks_str.split(",")
    for item in items:
        item = item.strip()
        if ":" in item:
            code, name = item.split(":", 1)
            stocks[code.strip()] = name.strip()
        else:
            # 没有名称就用代码
            stocks[item.strip()] = item.strip()
    
    return stocks

def get_stock_price(code: str, name: str) -> dict:
    """获取股票价格 - 使用新浪API"""
    try:
        if code.startswith("6") or code == "1A0001":
            stock_type = "sh"
        elif code.startswith("0") or code.startswith("3"):
            stock_type = "sz"
        else:
            stock_type = "sh"
        
        # 处理上证指数
        if code == "1A0001":
            stock_code = "sh000001"
        else:
            stock_code = f"{stock_type}{code}"
        
        url = f"https://hq.sinajs.cn/list={stock_code}"
        req = urllib.request.Request(url, headers={
            "Referer": "https://finance.sina.com.cn",
            "User-Agent": "Mozilla/5.0"
        })
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            data = response.read().decode("gb2312", errors="ignore")
        
        if "=" in data:
            values = data.split("=")[1].strip('"').split(",")
            if len(values) > 3:
                actual_name = values[0]
                open_price = float(values[1]) if values[1] else 0
                prev_close = float(values[2]) if values[2] else 0
                current_price = float(values[3]) if values[3] else 0
                high = float(values[4]) if len(values) > 4 and values[4] else 0
                low = float(values[5]) if len(values) > 5 and values[5] else 0
                volume = float(values[8]) if len(values) > 8 and values[8] else 0
                amount = float(values[9]) if len(values) > 9 and values[9] else 0
                
                change = current_price - prev_close
                pct = (change / prev_close * 100) if prev_close > 0 else 0
                
                return {
                    "code": code,
                    "name": name if name != code else actual_name,
                    "open": open_price,
                    "prev_close": prev_close,
                    "price": current_price,
                    "high": high,
                    "low": low,
                    "change": change,
                    "pct": pct,
                    "volume": volume,
                    "amount": amount
                }
    except Exception as e:
        print(f"获取 {code} 失败: {e}")
    
    return {"code": code, "name": name, "price": 0, "prev_close": 0, 
            "change": 0, "pct": 0, "volume": 0, "amount": 0}

def get_kdj(code: str, period: int = 9) -> dict:
    """获取KDJ指标 - 使用东方财富API"""
    try:
        # 东方财富K线接口
        if code.startswith("6"):
            symbol = f"1.{code}"
        elif code == "1A0001":
            symbol = "1.000001"
        else:
            symbol = f"0.{code}"
        
        url = f"http://push2his.eastmoney.com/api/qt/stock/kline/get?secid={symbol}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=0&end=20500101&lmt=30"
        
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0"
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        if result.get("data") and result["data"].get("klines"):
            klines = result["data"]["klines"]
            
            if len(klines) >= period:
                # 解析K线数据: 日期,开盘,收盘,最高,最低,成交量,成交额,振幅,涨跌幅,涨跌额,换手率
                highs = []
                lows = []
                closes = []
                
                for line in klines[-period:]:
                    parts = line.split(",")
                    if len(parts) >= 5:
                        highs.append(float(parts[3]))
                        lows.append(float(parts[4]))
                        closes.append(float(parts[2]))
                
                # 最新数据
                current_close = closes[-1] if closes else 0
                n_high = max(highs)
                n_low = min(lows)
                
                if n_high != n_low:
                    rsv = (current_close - n_low) / (n_high - n_low) * 100
                else:
                    rsv = 50
                
                # 计算K、D、J (使用EMA方式)
                k = 2/3 * 50 + 1/3 * rsv
                d = 2/3 * 50 + 1/3 * k
                j = 3 * k - 2 * d
                
                return {"k": k, "d": d, "j": j}
    except Exception as e:
        print(f"获取KDJ失败 {code}: {e}")
    
    return {"k": "-", "d": "-", "j": "-"}

def format_amount(val: float) -> str:
    if val >= 100000000:
        return f"{val/100000000:.2f}亿"
    elif val >= 10000:
        return f"{val/10000:.2f}万"
    return f"{val:.0f}"

def get_k_signal(k: float) -> str:
    if k == "-":
        return ""
    if k >= 80:
        return " (超买⚠️)"
    elif k <= 20:
        return " (超卖🚀)"
    elif k >= 50:
        return " (偏强)"
    else:
        return " (偏弱)"

def generate_report(stocks: dict) -> str:
    report = []
    report.append(f"📊 自选股日报 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    
    stocks_data = []
    for code, name in stocks.items():
        data = get_stock_price(code, name)
        kdj = get_kdj(code)
        data["kdj"] = kdj
        stocks_data.append(data)
    
    valid_stocks = [s for s in stocks_data if s["price"] > 0]
    valid_stocks.sort(key=lambda x: x["pct"], reverse=True)
    
    # ==================== 涨跌幅排行 ====================
    report.append("=" * 50)
    report.append("📈 今日涨跌幅排行")
    report.append("=" * 50)
    
    for s in valid_stocks:
        trend = "🔺" if s["pct"] > 0 else "🔻" if s["pct"] < 0 else "➡️"
        color = f"+{s['pct']:.2f}%" if s["pct"] > 0 else f"{s['pct']:.2f}%"
        report.append(f"{trend} {s['name']}: {s['price']:.2f} ({color})")
    
    # ==================== KDJ指标 ====================
    report.append("")
    report.append("=" * 50)
    report.append("📊 KDJ技术指标")
    report.append("=" * 50)
    
    for s in valid_stocks:
        kdj = s.get("kdj", {"k": "-", "d": "-", "j": "-"})
        if kdj["k"] != "-":
            k_val = float(kdj["k"])
            signal = get_k_signal(k_val)
            report.append(f"{s['name']}: K={kdj['k']:.1f} D={kdj['d']:.1f} J={kdj['j']:.1f}{signal}")
        else:
            report.append(f"{s['name']}: KDJ计算中...")
    
    # ==================== 涨跌幅详情 ====================
    report.append("")
    report.append("=" * 50)
    report.append("📋 详细行情")
    report.append("=" * 50)
    
    for s in valid_stocks:
        trend = "📈" if s["pct"] > 0 else "📉" if s["pct"] < 0 else "➡️"
        kdj = s.get("kdj", {"k": "-", "d": "-", "j": "-"})
        
        report.append(f"\n{trend} {s['name']} ({s['code']})")
        report.append(f"   现价: {s['price']:.2f}  昨收: {s['prev_close']:.2f}")
        report.append(f"   涨跌: {s['change']:+.2f}  涨幅: {s['pct']:+.2f}%")
        
        if kdj["k"] != "-":
            report.append(f"   KDJ: K={kdj['k']:.1f} D={kdj['d']:.1f} J={kdj['j']:.1f}")
        
        if s["amount"] > 0:
            report.append(f"   成交额: {format_amount(s['amount'])}")
    
    # ==================== 重点关注 ====================
    report.append("")
    report.append("=" * 50)
    report.append("⚠️ 重点关注")
    report.append("=" * 50)
    
    # K值超卖信号
    oversold = [s for s in valid_stocks if s.get("kdj", {}).get("k", "-") != "-" and float(s["kdj"]["k"]) <= 20]
    if oversold:
        report.append("\n🚀 超卖区（可能反弹）:")
        for s in oversold:
            report.append(f"   • {s['name']}: K={s['kdj']['k']:.1f}")
    
    # K值超买信号
    overbought = [s for s in valid_stocks if s.get("kdj", {}).get("k", "-") != "-" and float(s["kdj"]["k"]) >= 80]
    if overbought:
        report.append("\n⚠️ 超买区（注意风险）:")
        for s in overbought:
            report.append(f"   • {s['name']}: K={s['kdj']['k']:.1f}")
    
    # 涨幅前3
    top3 = valid_stocks[:3] if len(valid_stocks) >= 3 else valid_stocks
    report.append("\n🔥 涨幅前3:")
    for i, s in enumerate(top3, 1):
        if s["pct"] > 0:
            report.append(f"   {i}. {s['name']}: +{s['pct']:.2f}%")
    
    # ==================== 统计 ====================
    report.append("")
    report.append("=" * 50)
    report.append("📊 今日统计")
    report.append("=" * 50)
    
    up = len([s for s in valid_stocks if s["pct"] > 0])
    down = len([s for s in valid_stocks if s["pct"] < 0])
    flat = len([s for s in valid_stocks if s["pct"] == 0])
    
    avg_pct = sum(s["pct"] for s in valid_stocks) / len(valid_stocks) if valid_stocks else 0
    
    report.append(f"   上涨: {up}只  ⬆️")
    report.append(f"   下跌: {down}只  ⬇️")
    report.append(f"   平盘: {flat}只  ➡️")
    report.append(f"   平均涨幅: {avg_pct:+.2f}%")
    
    report.append("")
    report.append(f"📌 数据来源: 新浪财经+东方财富 | 更新时间: {datetime.now().strftime('%H:%M')}")
    
    return "\n".join(report)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 daily_report.py \"代码1:名称1,代码2:名称2,...\"")
        print("示例：python3 daily_report.py \"1A0001:上证指数,600036:招商银行,000858:五粮液\"")
        sys.exit(1)
    
    stocks_str = sys.argv[1]
    stocks = parse_stocks(stocks_str)
    print(generate_report(stocks))