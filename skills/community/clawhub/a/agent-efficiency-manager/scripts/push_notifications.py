#!/usr/bin/env python3
"""
推送优化建议通知（企微 / 腾讯文档）
"""

import json
import argparse
from pathlib import Path

def push_via_wecom(webhook_url, recommendations):
    """通过企微 Webhook 推送"""
    import requests
    
    # 构造消息
    content = "## 📊 Agent 效率优化建议\n\n"
    
    for rec in recommendations.get("recommendations", []):
        agent_name = rec.get("agent_name", "Unknown")
        summary = rec.get("summary", "")
        
        content += f"### {agent_name}\n"
        content += f"{summary}\n\n"
        
        # 添加推荐
        add_recs = rec.get("add_recommendations", [])
        if add_recs:
            content += "**建议添加：**\n"
            for skill in add_recs[:3]:  # 最多显示 3 个
                content += f"- {skill['skill_name']}：{skill['reason']}\n"
            content += "\n"
        
        # 添加移除建议
        remove_sugs = rec.get("remove_suggestions", [])
        if remove_sugs:
            content += "**建议移除：**\n"
            for sug in remove_sugs:
                content += f"- {sug['skill']}：{sug['reason']}\n"
            content += "\n"
    
    # 发送企微消息
    message = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    
    try:
        resp = requests.post(webhook_url, json=message, timeout=10)
        if resp.status_code == 200:
            print(f"✅ 企微推送成功")
        else:
            print(f"❌ 企微推送失败：{resp.text}")
    except Exception as e:
        print(f"❌ 企微推送异常：{e}")

def push_via_tencent_docs(recommendations, output_path):
    """推送到腾讯文档（生成可分享的文档）"""
    # 生成 Markdown 报告
    report = f"# Agent 效率优化建议\n\n生成时间：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for rec in recommendations.get("recommendations", []):
        agent_name = rec.get("agent_name", "Unknown")
        summary = rec.get("summary", "")
        
        report += f"## {agent_name}\n\n"
        report += f"{summary}\n\n"
        
        # 添加推荐
        add_recs = rec.get("add_recommendations", [])
        if add_recs:
            report += "**建议添加：**\n\n"
            for skill in add_recs:
                report += f"- **{skill['skill_name']}**（评分：{skill['rating']}）\n"
                report += f"  - 描述：{skill['description']}\n"
                report += f"  - 理由：{skill['reason']}\n\n"
        
        # 添加移除建议
        remove_sugs = rec.get("remove_suggestions", [])
        if remove_sugs:
            report += "**建议移除：**\n\n"
            for sug in remove_sugs:
                report += f"- **{sug['skill']}**\n"
                report += f"  - 理由：{sug['reason']}\n\n"
        
        report += "---\n\n"
    
    # 保存到本地（实际应调用腾讯文档 API）
    output_path = Path(output_path).expanduser()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"✅ 报告已生成：{output_path}")
    print(f"   提示：实际使用时需要调用腾讯文档 API 上传")

def push_notifications(recommendations_path, channel, webhook_url=None, output_path="optimization_report.md"):
    """推送通知"""
    # 读取建议
    with open(recommendations_path, "r", encoding="utf-8") as f:
        recommendations = json.load(f)
    
    if channel == "wecom":
        if not webhook_url:
            print("❌ 错误：企微推送需要 --webhook 参数")
            return
        push_via_wecom(webhook_url, recommendations)
    
    elif channel == "tencent-docs":
        push_via_tencent_docs(recommendations, output_path)
    
    else:
        print(f"❌ 不支持的推送渠道：{channel}")
        print("   支持的渠道：wecom, tencent-docs")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="推送优化建议通知")
    parser.add_argument("--recommendations", default="recommendations.json", help="建议文件路径")
    parser.add_argument("--channel", default="tencent-docs", choices=["wecom", "tencent-docs"], help="推送渠道")
    parser.add_argument("--webhook", help="企微 Webhook URL（channel=wecom 时必填）")
    parser.add_argument("--output", default="optimization_report.md", help="输出报告路径（channel=tencent-docs 时）")
    args = parser.parse_args()
    
    recommendations_path = Path(args.recommendations).expanduser()
    push_notifications(recommendations_path, args.channel, args.webhook, args.output)
