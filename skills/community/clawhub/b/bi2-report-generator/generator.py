#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BI2 事业部经营分析报告生成器

根据 PPTX 截图数据自动生成 BI2 事业部经营分析报告（HTML 格式）
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 默认数据（基于截图紫色底色实际数据）
DEFAULT_DATA = {
    "monthly": [
        {"month": "2025-01", "sales": 8199, "gross_profit": 1617, "gross_margin": "19.73%", "net_profit": 48, "net_margin": "0.58%"},
        {"month": "2025-02", "sales": 7922, "gross_profit": 1546, "gross_margin": "19.52%", "net_profit": 121, "net_margin": "1.52%"},
        {"month": "2025-03", "sales": 9854, "gross_profit": 2035, "gross_margin": "20.66%", "net_profit": 1378, "net_margin": "13.98%"},
        {"month": "2025-04", "sales": 11046, "gross_profit": 2572, "gross_margin": "23.29%", "net_profit": 1291, "net_margin": "11.69%"},
        {"month": "2025-05", "sales": 10009, "gross_profit": 2294, "gross_margin": "22.92%", "net_profit": 1882, "net_margin": "18.81%"},
        {"month": "2025-06", "sales": 10474, "gross_profit": 2427, "gross_margin": "23.17%", "net_profit": 968, "net_margin": "9.24%"},
        {"month": "2025-07", "sales": 13166, "gross_profit": 3333, "gross_margin": "25.32%", "net_profit": 1662, "net_margin": "12.62%"},
        {"month": "2025-08", "sales": 11392, "gross_profit": 2734, "gross_margin": "24.00%", "net_profit": 971, "net_margin": "8.52%"},
        {"month": "2025-09", "sales": 6576, "gross_profit": 1716, "gross_margin": "24.87%", "net_profit": 453, "net_margin": "6.88%"},
        {"month": "2025-10", "sales": 5766, "gross_profit": 1434, "gross_margin": "24.60%", "net_profit": 36, "net_margin": "0.63%"},
        {"month": "2025-11", "sales": 7467, "gross_profit": 1837, "gross_margin": "21.92%", "net_profit": -60, "net_margin": "-0.81%"},
        {"month": "2025-12", "sales": 6234, "gross_profit": 1139, "gross_margin": "18.27%", "net_profit": 1094, "net_margin": "17.55%"},
        {"month": "2026-01", "sales": 8716, "gross_profit": 1537, "gross_margin": "17.63%", "net_profit": 432, "net_margin": "4.95%"},
        {"month": "2026-02", "sales": 5407, "gross_profit": 813, "gross_margin": "15.04%", "net_profit": -251, "net_margin": "-4.65%"},
        {"month": "2026-03", "sales": 11191, "gross_profit": 2108, "gross_margin": "18.84%", "net_profit": 873, "net_margin": "7.80%"},
    ],
    "quarterly": {
        "2025_Q1": {"sales": 27167, "gross_margin": "19.97%"},
        "2025_Q2": {"sales": 31989, "gross_margin": "23.54%"},
        "2025_Q3": {"sales": 32651, "gross_margin": "25.32%"},
        "2025_Q4": {"sales": 19467, "gross_margin": "18.27%"},
        "2026_Q1": {"sales": 25314, "gross_margin": "17.16%"},
    },
    "expense": {
        "2025_Q3": {"total": 1605.23, "months": [542.82, 512.98, 565.40]},
        "2025_Q4": {"total": 1550.82, "months": [440.95, 570.53, 539.34]},
        "2026_Q1": {"total": 1372.54, "months": [507.58, 465.72, 399.24]},
    },
    "customers_2025": [
        {"rank": 1, "name": "帝国", "sales": 70956, "ratio": "65.64%", "status": "核心客户"},
        {"rank": 2, "name": "MTL", "sales": 33766, "ratio": "31.24%", "status": "主要客户"},
        {"rank": 3, "name": "BAT", "sales": 3378, "ratio": "3.12%", "status": "老项目"},
        {"rank": 4, "name": "ITMS", "sales": 0, "ratio": "0.00%", "status": "新项目"},
    ],
    "customers_2026_ytd": [
        {"rank": 1, "name": "帝国 - 液态", "sales": 11541, "net_profit": 605, "net_margin": "5.24%", "status": "核心客户"},
        {"rank": 2, "name": "MTL-液态", "sales": 5192, "net_profit": 174, "net_margin": "3.36%", "status": "主要客户"},
        {"rank": 3, "name": "帝国 - 固态", "sales": 3597, "net_profit": 180, "net_margin": "5.01%", "status": "核心客户"},
        {"rank": 4, "name": "ITMS-固态", "sales": 1772, "net_profit": -196, "net_margin": "-4.75%", "status": "新客户"},
        {"rank": 5, "name": "BAT-液态", "sales": 849, "net_profit": 260, "net_margin": "30.68%", "status": "新客户"},
    ],
    "inventory": {"month3_total": 10039, "month2_total": 14643, "reduction": 4600, "turnover_days": 16.9, "standard_days": 28.0},
    "ar": {"total": 37429, "overdue": 1671, "overdue_rate": "4.47%"},
    "forecast": {
        "2026-04": {"sales": 6110, "gross_profit": 920, "gross_margin": "15.06%", "net_profit": 274, "net_margin": "4.49%"},
        "2026-05": {"sales": 8624, "gross_profit": 1228, "gross_margin": "14.25%", "net_profit": 268, "net_margin": "3.12%"},
        "2026-06": {"sales": 6814, "gross_profit": 941, "gross_margin": "13.81%", "net_profit": 76, "net_margin": "1.13%"},
        "2026_Q2": {"sales": 21548, "gross_profit": 3090, "gross_margin": "14.34%", "net_profit": 619, "net_margin": "2.87%"},
    },
}

# 用户文件夹映射
USER_FOLDERS = {
    "Richard": "/Users/zhangzhaoliangdemacmini/Desktop/Openclaw_Pool/Richard_Folder/",
    "JING": "/Users/zhangzhaoliangdemacmini/Desktop/Openclaw_Pool/JING_Folder/",
    "Jeanie": "/Users/zhangzhaoliangdemacmini/Desktop/Openclaw_Pool/Jeanie_Folder/",
    "Mickey": "/Users/zhangzhaoliangdemacmini/Desktop/Openclaw_Pool/Mickey_Folder/",
    "City": "/Users/zhangzhaoliangdemacmini/Desktop/Openclaw_Pool/City_Folder/",
}


def generate_report(data=None, user="Richard", version="完善版"):
    """生成 HTML 报告"""
    if data is None:
        data = DEFAULT_DATA
    
    today = datetime.now().strftime("%Y%m%d")
    filename = f"BI2 事业部经营分析报告_{today}_{version}.html"
    output_path = os.path.join(USER_FOLDERS.get(user, USER_FOLDERS["Richard"]), filename)
    
    # 读取模板
    template_path = os.path.join(os.path.dirname(__file__), "report_template.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    else:
        # 使用内置简化模板
        template = get_simplified_template()
    
    # 填充数据（简化版：实际应使用模板引擎）
    html_content = template
    
    # 保存文件
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return {"success": True, "path": output_path, "filename": filename}


def get_simplified_template():
    """获取简化版 HTML 模板"""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>BI2 事业部经营分析报告</title>
</head>
<body>
    <h1>BI2 事业部经营分析报告</h1>
    <p>报告生成时间：{date}</p>
    <p>数据源：PPTX 截图（真实数据）</p>
</body>
</html>""".format(date=datetime.now().strftime("%Y-%m-%d"))


def send_to_feishu(file_path, user_open_id):
    """发送文件到飞书"""
    import requests
    
    app_id = "cli_a92550a0def91bb4"
    app_secret = "gKxq8vGTcr13awNezls7Uh6kqhv4AEwB"
    
    # 获取 token
    token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    token_resp = requests.post(token_url, json={"app_id": app_id, "app_secret": app_secret})
    token = token_resp.json().get("tenant_access_token")
    
    if not token:
        return {"success": False, "error": "Failed to get token"}
    
    # 上传文件
    headers = {"Authorization": f"Bearer {token}"}
    upload_url = "https://open.feishu.cn/open-apis/im/v1/files"
    
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        files = {"file": (file_name, f, "application/octet-stream")}
        data = {"file_type": "stream"}
        upload_resp = requests.post(upload_url, headers=headers, files=files, data=data)
    
    upload_data = upload_resp.json()
    file_key = upload_data.get("data", {}).get("file_key")
    
    if not file_key:
        return {"success": False, "error": "Failed to upload file"}
    
    # 发送文件消息
    send_url = "https://open.feishu.cn/open-apis/im/v1/messages"
    msg_content = {"file_key": file_key, "file_type": "stream"}
    send_data = {
        "receive_id": user_open_id,
        "msg_type": "file",
        "content": json.dumps(msg_content)
    }
    params = {"receive_id_type": "open_id"}
    
    send_resp = requests.post(send_url, headers=headers, params=params, json=send_data)
    send_data_resp = send_resp.json()
    
    return {
        "success": send_data_resp.get("code") == 0,
        "message_id": send_data_resp.get("data", {}).get("message_id"),
        "file_name": file_name,
    }


if __name__ == "__main__":
    # 测试生成
    result = generate_report()
    print(f"报告生成：{result}")
