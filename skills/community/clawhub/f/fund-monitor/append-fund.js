#!/usr/bin/env python3
"""基金飞书更新脚本 - 在文档末尾新增记录"""

import json
import sys
from datetime import datetime

# 飞书配置
DOC_TOKEN = "J9BndSQkHoguODx96PtcNslnnsc"
APP_ID = "cli_a9f34580c5badbd9"
APP_SECRET = "DDxM8UV6Dn5OO0Il8MxNGbGmX1PEiLuJ"

def get_access_token():
    import requests
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = {"app_id": APP_ID, "app_secret": APP_SECRET}
    resp = requests.post(url, json=data)
    return resp.json().get("tenant_access_token")

def get_fund_data():
    """获取基金数据"""
    # 读取基金快照数据
    try:
        with open("/Users/js/.openclaw/workspace/fund_data.json", "r") as f:
            return json.load(f)
    except:
        return None

def append_to_doc(token, content):
    """在飞书文档末尾追加内容"""
    import requests
    url = "https://open.feishu.cn/open-apis/docx/v1/documents/blocks/append"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "doc_token": DOC_TOKEN,
        "content": content
    }
    resp = requests.post(url, json=data, headers=headers)
    return resp.json()

def main():
    # 获取基金数据（从命令行参数或文件）
    if len(sys.argv) > 1:
        # 从命令行参数获取
        try:
            fund_data = json.loads(sys.argv[1])
        except:
            print("Failed to parse fund data")
            return
    else:
        fund_data = get_fund_data()
    
    if not fund_data:
        print("No fund data found")
        return
    
    # 获取access token
    token = get_access_token()
    
    # 构建新增内容
    today = datetime.now().strftime("%Y-%m-%d")
    total_market = fund_data.get("totalMarketValue", 0)
    total_profit = fund_data.get("totalProfit", 0)
    today_profit = fund_data.get("todayProfit", 0)
    total_return = fund_data.get("totalReturn", 0)
    up_count = fund_data.get("upCount", 0)
    down_count = fund_data.get("downCount", 0)
    
    content = f"""---
## 📈 {today} 基金账户快照

**日期:** {today}

**总本金:** {fund_data.get("totalPrincipal", 0):,.2f} 元

**总市值:** {total_market:,.2f} 元

**持仓总收益:** {total_profit:+,} 元

**今日收益:** {today_profit:+,} 元

**总收益率:** {total_return:+.2f}%

**上涨基金:** {up_count}只 | **下跌基金:** {down_count}只
"""
    
    # 追加到飞书文档
    result = append_to_doc(token, content)
    
    if result.get("code") == 0:
        print(f"✅ Fund data appended to Feishu doc: {today}")
    else:
        print(f"❌ Failed to append: {result}")

if __name__ == "__main__":
    main()
