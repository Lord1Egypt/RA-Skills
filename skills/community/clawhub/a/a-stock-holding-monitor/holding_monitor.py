#!/home/linuxbrew/.linuxbrew/bin/python3
"""
A股持仓监控脚本
监控持仓股票的止损/支撑破位/目标价/异常波动
触发条件：
  - 触及止损价 → 建议止损
  - 跌破支撑位 → 关注是否企稳
  - 当日跌幅超5% → 异动告警
  - 乖离率超+5% → 短线过热警告

使用方法：
  1. 修改下方的 HOLDINGS 列表，填入你的持仓
  2. 命令行运行：python3 holding_monitor.py
  3. 配合cron定时检查：*/30 9-15 * * 1-5 python3 /path/to/holding_monitor.py

作者：林林（微信助手）
"""

import requests
import time
import json
import sys

# ==================== 持仓配置 ====================
# 在这里填入你的持仓信息
# code格式：sh开头表示上证，sz开头表示深证
# 例如：sh600519（茅台） sz000001（平安）
HOLDINGS = [
    {
        "name": "洛阳钼业",
        "code": "sh603993",
        "cost": 20.146,
        "qty": 200,
        "stop_loss": 18.5,
        "support": 19.5,
        "target": "24-26",
        "optimistic": 27,
    },
    {
        "name": "潍柴动力",
        "code": "sz000338",
        "cost": 26.871,
        "qty": 100,
        "stop_loss": 26.0,
        "support": 26.5,
        "target": "29-30",
        "optimistic": 32,
    },
]
# ==============================================


def get_price(code):
    """获取股票实时价格"""
    try:
        r = requests.get(f"http://hq.sinajs.cn/list={code}",
                        headers={"Referer": "http://finance.sina.com.cn", "User-Agent": "Mozilla/5.0"}, timeout=10)
        m = r.text.split('"')[1].split(',')
        price = float(m[3])
        prev = float(m[2])
        chg = (price - prev) / prev * 100
        return price, prev, chg
    except Exception as e:
        print(f"获取{code}价格失败: {e}")
        return None, None, None


def get_ma5(code):
    """获取MA5"""
    try:
        params = {"symbol": code, "scale": 240, "ma": 5, "datalen": 20}
        r = requests.get(
            "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData",
            params=params,
            headers={"Referer": "http://finance.sina.com.cn", "User-Agent": "Mozilla/5.0"},
            timeout=15
        )
        data = r.json()
        closes = [float(d["close"]) for d in data]
        return sum(closes[-5:]) / 5
    except:
        return None


def check_holdings():
    """检查所有持仓，返回需要提醒的信息"""
    alerts = []
    prices_data = {}

    for h in HOLDINGS:
        price, prev, chg = get_price(h["code"])
        if price is None:
            continue

        ma5 = get_ma5(h["code"])
        profit = (price - h["cost"]) * h["qty"]
        profit_pct = (price - h["cost"]) / h["cost"] * 100

        item = {
            "name": h["name"],
            "code": h["code"],
            "price": price,
            "prev": prev,
            "chg": chg,
            "cost": h["cost"],
            "profit": profit,
            "profit_pct": profit_pct,
            "ma5": ma5,
            "stop_loss": h["stop_loss"],
            "support": h["support"],
            "target": h["target"],
            "optimistic": h["optimistic"],
            "signals": [],
            "action": "持有",
        }

        # 1. 触发止损
        if price <= h["stop_loss"]:
            item["signals"].append(f"🔴 触及止损价 {h['stop_loss']}，建议止损！")
            item["action"] = "止损"

        # 2. 跌破重要支撑
        elif price <= h["support"]:
            item["signals"].append(f"🟠 跌破支撑位 {h['support']}，关注是否企稳")
            item["action"] = "关注"

        # 3. 跌幅超5%异动
        elif chg <= -5:
            item["signals"].append(f"🔴 当日跌幅 {chg:.2f}%，异动！")
            item["action"] = "异动"

        # 4. 乖离率超5%
        elif ma5 and (price - ma5) / ma5 * 100 > 5:
            item["signals"].append(f"⚠️ 乖离率 +{(price-ma5)/ma5*100:.2f}%，短线过热")

        prices_data[h["code"]] = {
            "price": price,
            "chg": chg,
            "profit": profit,
            "profit_pct": profit_pct,
            "action": item["action"],
            "signals": item["signals"],
            "ma5": ma5,
            "support": h["support"],
            "stop_loss": h["stop_loss"],
            "target": h["target"],
        }

        alerts.append(item)

    return prices_data, alerts


def format_message(prices_data):
    """格式化输出"""
    lines = ["📊 A股持仓监控\n"]
    has_action = False

    for h in HOLDINGS:
        code = h["code"]
        if code in prices_data:
            d = prices_data[code]
            lines.append(f"---")
            lines.append(f"【{h['name']} {code}】")
            lines.append(f"现价: {d['price']:.3f}  {d['chg']:+.2f}%")
            lines.append(f"成本: {h['cost']:.3f}  浮盈: {d['profit']:+.0f}元({d['profit_pct']:+.2f}%)")
            if d['ma5']:
                lines.append(f"MA5: {d['ma5']:.2f}  乖离率: {(d['price']-d['ma5'])/d['ma5']*100:+.2f}%")
            lines.append(f"支撑: {d['support']}  止损: {d['stop_loss']}  目标: {d['target']}")

            if d['signals']:
                lines.append("")
                for sig in d['signals']:
                    lines.append(sig)
                has_action = True

            lines.append(f"→ 操作建议: {d['action']}")

    if not has_action:
        lines.append("\n✅ 所有持仓正常，无触发信号")

    return "\n".join(lines)


def main():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 持仓检查...")

    prices_data, alerts = check_holdings()

    if not prices_data:
        print("获取价格失败")
        sys.exit(1)

    # 打印结果
    for h in HOLDINGS:
        code = h["code"]
        if code in prices_data:
            d = prices_data[code]
            print(f"{h['name']}: 现价{d['price']} {d['chg']:+.2f}% 浮盈{d['profit']:+.0f}元({d['profit_pct']:+.2f}%)")
            if d['signals']:
                for s in d['signals']:
                    print(f"  {s}")
                print(f"  → {d['action']}")

    # 输出消息
    msg = format_message(prices_data)
    print("\n" + msg)

    # 保存状态
    with open("/tmp/holding_check.json", "w") as f:
        json.dump({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "prices": prices_data}, f, ensure_ascii=False)

    # 有信号返回2，无信号返回0
    has_signal = any(d.get('signals') for d in prices_data.values())
    sys.exit(2 if has_signal else 0)


if __name__ == "__main__":
    main()
