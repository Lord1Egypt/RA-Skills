#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📧 Email Helper - 邮件助手（优化版）
功能：邮件草稿、回复建议、邮件模板、AI 润色
支持：中文/英文/日文
"""

import json
import random
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).parent
TEMPLATES_FILE = DATA_DIR / "templates.json"
SENT_FILE = DATA_DIR / "sent_emails.json"

# ========== 邮件模板库（优化版） ==========

EMAIL_TEMPLATES = {
    # 工作类
    "请假": {
        "subject": "请假申请 - {name} - {date}",
        "content": """
尊敬的{leader}：

您好！

因{reason}，我需要在{start_date}至{end_date}期间请假{days}天。

请假期间的工作已安排如下：
1. {handover1}
2. {handover2}

如有紧急情况，可通过{contact}联系我。

恳请批准，谢谢！

此致
敬礼

{name}
{date}
""",
        "tags": ["工作", "请假", "申请"]
    },
    
    "工作汇报": {
        "subject": "{period}工作汇报 - {name} - {date}",
        "content": """
尊敬的{leader}：

您好！

现将我{period}的工作情况汇报如下：

✅ 已完成工作：
1. {task1} - {result1}
2. {task2} - {result2}
3. {task3} - {result3}

🔄 进行中工作：
1. {ongoing1} - 进度{progress1}%
2. {ongoing2} - 进度{progress2}%

📋 下阶段计划：
1. {plan1}
2. {plan2}

⚠️ 需要支持：
{support_needed}

请审阅，谢谢！

此致
敬礼

{name}
{date}
""",
        "tags": ["工作", "汇报", "总结"]
    },
    
    "会议邀请": {
        "subject": "会议邀请：{meeting_topic} - {date}",
        "content": """
各位同事：

大家好！

兹定于{meeting_date} {meeting_time}在{meeting_location}召开{meeting_topic}会议。

📋 会议议程：
1. {agenda1}
2. {agenda2}
3. {agenda3}

👥 参会人员：{attendees}

📎 会议材料：{materials}

请准时参加，谢谢！

此致
敬礼

{organizer}
{date}
""",
        "tags": ["工作", "会议", "邀请"]
    },
    
    "商务合作": {
        "subject": "商务合作洽谈 - {company}",
        "content": """
尊敬的{recipient}：

您好！

我是{company}的{position}{name}。我们专注于{business}...

合作意向：
1. {cooperation1}
2. {cooperation2}

希望能与贵方探讨合作机会...

期待您的回复！

祝好，
{name}
{company}
{contact}
""",
        "tags": ["商务", "合作", "洽谈"]
    },
    
    "求职": {
        "subject": "应聘{position} - {name}",
        "content": """
尊敬的招聘负责人：

您好！

我在{channel}看到贵公司正在招聘{position}...

我的优势：
1. {skill1}
2. {skill2}
3. {skill3}

工作经历：
{work_experience}

期待有机会加入贵公司！

此致
敬礼

{name}
{contact}
""",
        "tags": ["求职", "应聘", "简历"]
    },
    
    "感谢": {
        "subject": "感谢 - {topic}",
        "content": """
尊敬的{recipient}：

您好！

非常感谢您{reason}...

您的帮助对我非常重要...

再次感谢！

祝好，
{name}
{date}
""",
        "tags": ["感谢", "礼貌"]
    },
    
    "道歉": {
        "subject": "致歉 - {topic}",
        "content": """
尊敬的{recipient}：

您好！

对于{issue}，我深感抱歉...

原因说明：{reason}

改进措施：
1. {improvement1}
2. {improvement2}

恳请谅解！

此致
敬礼

{name}
{date}
""",
        "tags": ["道歉", "致歉"]
    },
    
    "催款": {
        "subject": "关于{project}款项的提醒",
        "content": """
尊敬的{recipient}：

您好！

关于{project}项目，合同约定付款日期为{due_date}，截至目前尚未收到款项。

💰 欠款金额：{amount}
📄 发票号码：{invoice_no}

请您尽快安排付款，谢谢配合！

如有问题，请随时联系我。

祝好，
{name}
{company}
{contact}
""",
        "tags": ["财务", "催款", "提醒"]
    }
}

# ========== 英文邮件模板 ==========

EMAIL_TEMPLATES_EN = {
    "leave": {
        "subject": "Leave Application - {name}",
        "content": """
Dear {leader},

I am writing to request leave from {start_date} to {end_date} ({days} days) due to {reason}.

During my absence, I have arranged:
1. {handover1}
2. {handover2}

For urgent matters, please contact me at {contact}.

Thank you for your understanding.

Best regards,
{name}
{date}
""",
        "tags": ["work", "leave"]
    },
    
    "meeting": {
        "subject": "Meeting Invitation: {topic}",
        "content": """
Dear Team,

You are invited to attend a meeting on {date} at {time}.

📍 Location: {location}
📋 Agenda:
1. {agenda1}
2. {agenda2}

Please confirm your attendance.

Best regards,
{organizer}
""",
        "tags": ["work", "meeting"]
    },
    
    "follow_up": {
        "subject": "Follow-up: {topic}",
        "content": """
Dear {recipient},

I hope this email finds you well.

I'm writing to follow up on {topic}...

Could you please provide an update?

Looking forward to your reply.

Best regards,
{name}
""",
        "tags": ["follow-up", "reminder"]
    }
}

# ========== 邮件开场白库 ==========

OPENINGS = {
    "正式": [
        "尊敬的{recipient}：\n\n您好！",
        "尊敬的{recipient}：\n\n您好！祝您工作顺利！",
        "尊敬的{recipient}：\n\n感谢您百忙之中阅读此邮件。"
    ],
    "商务": [
        "尊敬的{recipient}：\n\n您好！",
        "尊敬的{recipient}：\n\n感谢贵公司一直以来的支持。"
    ],
    "非正式": [
        "Hi {recipient}，\n\n",
        "{recipient}，\n\n",
        "Hey {recipient}，\n\n希望你一切都好！"
    ]
}

# ========== 邮件结束语库 ==========

CLOSINGS = {
    "正式": [
        "此致\n敬礼",
        "顺祝商祺",
        "祝工作顺利"
    ],
    "商务": [
        "期待您的回复",
        "祝商祺",
        "祝好"
    ],
    "非正式": [
        "Best",
        "Cheers",
        "祝好",
        "有空联系"
    ]
}


def load_json(filepath):
    """加载 JSON 文件"""
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_json(filepath, data):
    """保存 JSON 文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_email(template_name, language="zh", **kwargs):
    """
    生成邮件
    
    Args:
        template_name: 模板名称
        language: 语言 (zh/en)
        **kwargs: 填充参数
        
    Returns:
        dict: 邮件内容
    """
    if language == "en":
        templates = EMAIL_TEMPLATES_EN
    else:
        templates = EMAIL_TEMPLATES
    
    if template_name not in templates:
        return None
    
    template = templates[template_name]
    
    # 填充默认值
    defaults = {
        "name": "[你的名字]",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "recipient": "[收件人]",
        "company": "[公司名]",
        "position": "[职位]",
        "contact": "[联系方式]",
        "leader": "[领导]",
        "reason": "[原因]",
        "start_date": "[开始日期]",
        "end_date": "[结束日期]",
        "days": "[天数]",
        "handover1": "[工作交接 1]",
        "handover2": "[工作交接 2]"
    }
    
    defaults.update(kwargs)
    
    subject = template["subject"].format(**defaults)
    content = template["content"].format(**defaults)
    
    return {
        "subject": subject,
        "content": content.strip(),
        "tags": template.get("tags", []),
        "language": language,
        "generated_at": datetime.now().isoformat()
    }


def polish_email(content, tone="formal"):
    """
    润色邮件
    
    Args:
        content: 邮件内容
        tone: 语气 (formal/casual/friendly)
        
    Returns:
        str: 润色后的内容
    """
    # 简单实现：添加合适的开场白和结束语
    if tone == "formal":
        opening = "尊敬的收件人：\n\n您好！"
        closing = "\n\n此致\n敬礼"
    elif tone == "casual":
        opening = "Hi,\n\n"
        closing = "\n\n祝好"
    else:  # friendly
        opening = "亲爱的朋友，\n\n"
        closing = "\n\n期待你的回复！"
    
    return f"{opening}\n{content}\n{closing}"


def suggest_subject(content):
    """
    根据内容建议邮件主题
    
    Args:
        content: 邮件正文
        
    Returns:
        str: 建议的主题
    """
    # 简单实现：提取关键词
    keywords = ["请假", "会议", "合作", "感谢", "道歉", "汇报", "邀请"]
    
    for keyword in keywords:
        if keyword in content:
            return f"关于{keyword} - {datetime.now().strftime('%Y-%m-%d')}"
    
    return f"邮件主题 - {datetime.now().strftime('%Y-%m-%d')}"


def save_sent_email(email):
    """保存已发送邮件"""
    sent = load_json(SENT_FILE)
    if "emails" not in sent:
        sent["emails"] = []
    
    sent["emails"].append(email)
    save_json(SENT_FILE, sent)


def get_email_stats():
    """获取邮件统计"""
    sent = load_json(SENT_FILE)
    emails = sent.get("emails", [])
    
    stats = {
        "total": len(emails),
        "by_type": {},
        "recent": []
    }
    
    for email in emails:
        tags = email.get("tags", [])
        for tag in tags:
            stats["by_type"][tag] = stats["by_type"].get(tag, 0) + 1
    
    stats["recent"] = emails[-5:]
    
    return stats


def main(query):
    """主函数"""
    query_lower = query.lower()
    
    # 语言检测
    language = "en" if any(word in query_lower for word in ["email", "leave", "meeting"]) else "zh"
    
    # ========== 工作邮件 ==========
    
    # 请假邮件
    if "请假" in query or "leave" in query_lower:
        template_name = "请假" if language == "zh" else "leave"
        email = generate_email(template_name, language=language)
        if not email:
            return f"❌ 未找到 {template_name} 模板"
        return f"""📧 **请假邮件已生成**

📝 **主题**：{email['subject']}

{email['content']}

💡 **提示**：请替换 [括号内] 的内容后发送"""
    
    # 工作汇报
    if "汇报" in query or "report" in query_lower:
        email = generate_email("工作汇报")
        return f"""📧 **工作汇报邮件已生成**

📝 **主题**：{email['subject']}

{email['content']}

💡 **提示**：请替换 [括号内] 的内容后发送"""
    
    # 会议邀请
    if "会议" in query or "meeting" in query_lower:
        email = generate_email("会议邀请")
        return f"""📧 **会议邀请邮件已生成**

📝 **主题**：{email['subject']}

{email['content']}

💡 **提示**：请替换 [括号内] 的内容后发送"""
    
    # ========== 商务邮件 ==========
    
    # 商务合作
    if "商务" in query or "合作" in query or "business" in query_lower:
        email = generate_email("商务合作")
        return f"""📧 **商务合作邮件已生成**

📝 **主题**：{email['subject']}

{email['content']}

💡 **提示**：请替换 [括号内] 的内容后发送"""
    
    # ========== 个人邮件 ==========
    
    # 感谢邮件
    if "感谢" in query or "谢谢" in query or "thank" in query_lower:
        email = generate_email("感谢")
        return f"""📧 **感谢邮件已生成**

📝 **主题**：{email['subject']}

{email['content']}

💡 **提示**：请替换 [括号内] 的内容后发送"""
    
    # 道歉邮件
    if "道歉" in query or "抱歉" in query:
        email = generate_email("道歉")
        return f"""📧 **道歉邮件已生成**

📝 **主题**：{email['subject']}

{email['content']}

💡 **提示**：请替换 [括号内] 的内容后发送"""
    
    # ========== 求职邮件 ==========
    
    # 求职/应聘
    if "求职" in query or "应聘" in query or "job" in query_lower:
        email = generate_email("求职")
        return f"""📧 **求职邮件已生成**

📝 **主题**：{email['subject']}

{email['content']}

💡 **提示**：请替换 [括号内] 的内容后发送"""
    
    # ========== 财务邮件 ==========
    
    # 催款
    if "催款" in query or "款项" in query or "付款" in query:
        email = generate_email("催款")
        return f"""📧 **催款邮件已生成**

📝 **主题**：{email['subject']}

{email['content']}

💡 **提示**：请替换 [括号内] 的内容后发送"""
    
    # ========== 邮件统计 ==========
    
    # 查看统计
    if "统计" in query or "记录" in query:
        stats = get_email_stats()
        response = "📊 **邮件统计**\n\n"
        response += f"总计：{stats['total']} 封\n\n"
        if stats['by_type']:
            response += "按类型：\n"
            for tag, count in stats['by_type'].items():
                response += f"  {tag}: {count} 封\n"
        return response
    
    # ========== 默认回复 ==========
    
    return """📧 邮件助手（优化版）

**支持模板**：

💼 工作类
1. 请假申请 - "帮我写请假邮件"
2. 工作汇报 - "写周报/月报"
3. 会议邀请 - "写会议邀请"

💼 商务类
4. 商务合作 - "写合作邮件"
5. 催款提醒 - "写催款邮件"

📝 个人类
6. 感谢信 - "写感谢邮件"
7. 道歉信 - "写道歉邮件"

💼 求职类
8. 求职信 - "写求职邮件"

**支持语言**：中文 / 英文

**其他功能**：
- 邮件润色
- 主题建议
- 发送记录统计

告诉我你需要写什么邮件？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("📧 邮件助手 - 测试")
    print("=" * 60)
    
    print("\n测试 1: 请假邮件")
    print(main("帮我写请假邮件"))
    
    print("\n" + "=" * 60)
    print("测试 2: 英文请假邮件")
    print(main("write a leave email"))
