#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""获取最新加密货币恐惧贪婪指数"""

import os
import argparse
import json
import sys
import urllib.request
import urllib.error

# 解决Windows编码问题
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# SkillPay 配置
SKILL_ID = "bf7f7f4e-baac-41d4-b4ed-6d078d74442e"
PRICE = 0.001  # 每次调用 0.001 USDT

def skillpay_charge(user_id, api_key=None):
    """SkillPay 扣费"""
    import json
    import urllib.request
    import urllib.error

    API = "https://skillpay.me/api/v1"

    def _post(path, body, key):
        req = urllib.request.Request(f"{API}{path}", data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", "X-API-Key": key}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            return json.loads(e.read())

    k = api_key or os.environ.get("SKILLPAY_API_KEY")
    if not k:
        return {"success": False, "error": "SKILLPAY_API_KEY not set"}
    
    body = {
        "user_id": user_id,
        "skill_id": SKILL_ID,
        "amount": PRICE,
        "currency": "USDT",
        "description": "Fear & Greed Index Query"
    }
    return _post("/billing/charge", body, k)


def get_fear_greed():
    """获取加密货币恐惧贪婪指数"""
    url = "https://api.alternative.me/fng/?limit=2"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode())
    
    latest = data['data'][0]
    prev = data['data'][1] if len(data['data']) > 1 else None
    
    return {
        "value": int(latest['value']),
        "classification": latest['value_classification'],
        "timestamp": int(latest['timestamp']),
        "value_prev": int(prev['value']) if prev else None,
    }


def get_btc_price():
    """获取BTC最新价格"""
    url = "https://api.alternative.me/v2/ticker/bitcoin/?convert=USD"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode())
    
    btc = data['data']['1']
    return {
        "price": round(btc['quotes']['USD']['price'], 2),
        "change_24h": round(btc['quotes']['USD']['percentage_change_24h'], 2)
    }


def get_emoji(value):
    """根据数值获取emoji"""
    if value <= 24:
        return "😨"  # 极度恐惧
    elif value <= 44:
        return "😟"  # 恐惧
    elif value <= 55:
        return "😐"  # 中性
    elif value <= 75:
        return "😋"  # 贪婪
    else:
        return "🤪"  # 极度贪婪


def get_analysis(value, change_24h):
    """生成简单分析"""
    if value <= 24:
        if change_24h < 0:
            return "市场极度恐慌，这往往是长线买入的机会。别人恐惧我贪婪嘛。"
        else:
            return "市场仍在极度恐慌，但价格已经开始反弹，可能是筑底信号。"
    elif value <= 44:
        return "市场处于恐惧状态，多头需要耐心等待情绪回暖。"
    elif value <= 55:
        return "情绪中性，市场方向不明，多看少动。"
    elif value <= 75:
        return "市场处于贪婪状态，赚钱效应不错，但注意追高风险。"
    else:
        if change_24h > 0:
            return "市场极度贪婪，人气狂热，往往是阶段顶部信号，注意止盈。"
        else:
            return "情绪极度贪婪但价格开始下跌，警惕回调风险。"


def format_output(index, btc):
    """格式化输出"""
    value = index['value']
    val_prev = index['value_prev']
    
    trend = ""
    if val_prev is not None:
        diff = value - val_prev
        if diff > 5:
            trend = " ↗️ 相比昨日贪婪度上升"
        elif diff < -5:
            trend = " ↘️ 相比昨日贪婪度下降"
        else:
            trend = " ➡️ 相比昨日变化不大"
    
    emoji = get_emoji(value)
    analysis = get_analysis(value, btc['change_24h'])
    
    lines = [
        "📊 加密货币恐惧贪婪指数",
        "",
        f"当前指数: **{value}** {emoji} {index['classification']}{trend}",
        "",
        f"₿ BTC 价格: ${btc['price']:,}",
        f"24h 涨跌: {btc['change_24h']}%",
        "",
        "💡 分析:",
        analysis,
        "",
        "分级: 0-24 极度恐惧 | 25-44 恐惧 | 45-55 中性 | 56-75 贪婪 | 76-100 极度贪婪",
        "",
        f"💰 本次调用扣费: {PRICE} USDT via SkillPay.me"
    ]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--user-id", required=True, help="用户ID (用于SkillPay扣费)")
    p.add_argument("--api-key", default=None, help="SkillPay API Key")
    args = p.parse_args()

    # 扣费
    result = skillpay_charge(args.user_id, args.api_key)
    if not result.get("success"):
        if result.get("needs_payment"):
            print(f"❌ 余额不足，请先充值。")
            print(f"🔗 充值链接: {result.get('payment_url')}")
            sys.exit(1)
        else:
            print(f"❌ 扣费失败: {result.get('message', result.get('error'))}")
            sys.exit(1)

    try:
        index = get_fear_greed()
        btc = get_btc_price()
        print(format_output(index, btc))
    except Exception as e:
        print(f"❌ 获取数据失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
