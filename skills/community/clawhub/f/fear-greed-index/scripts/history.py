#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""获取最近30天恐惧贪婪指数历史"""

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
    import os

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
        "description": "Fear & Greed Index History"
    }
    return _post("/billing/charge", body, k)


def get_history(days=30):
    """获取最近N天历史数据"""
    url = f"https://api.alternative.me/fng/?limit={days}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode())
    
    return data['data']


def format_output(data):
    """格式化输出历史"""
    lines = [
        "📜 最近30天恐惧贪婪指数历史",
        "",
        "日期       数值  情绪",
        "------------------------"
    ]
    
    from datetime import datetime
    for item in data:
        ts = int(item['timestamp'])
        date = datetime.fromtimestamp(ts).strftime('%m-%d')
        val = int(item['value'])
        cls = item['value_classification']
        lines.append(f"{date}   {val:3d}  {cls}")
    
    lines.append("")
    lines.append(f"💰 本次调用扣费: {PRICE} USDT via SkillPay.me")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--user-id", required=True, help="用户ID (用于SkillPay扣费)")
    p.add_argument("--days", type=int, default=30, help="获取多少天历史")
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
        data = get_history(args.days)
        print(format_output(data))
    except Exception as e:
        print(f"❌ 获取数据失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
