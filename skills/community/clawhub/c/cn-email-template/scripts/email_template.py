#!/usr/bin/env python3
"""
cn-email-template: 专业商务邮件生成器
支持10+常见商务场景，自动生成专业邮件正文
用法: python email_template.py <场景> <关键词>
"""

import sys
import os

# 邮件模板库
TEMPLATES = {
    "初次联系": {
        "subject": "关于{主题}的合作探讨",
        "greeting": "您好{姓名}，",
        "intro": "我是{发件人}，从{来源}了解到贵司/您的{相关领域}，非常感兴趣。",
        "body": "这次冒昧联系，主要是希望{目的}。{附加信息}",
        "closing": "期待您的回复，如方便也可添加我的微信进一步交流。",
        "signature": "{发件人}\n{职位}\n{联系方式}"
    },
    "跟进": {
        "subject": "跟进：{原主题}",
        "greeting": "您好{姓名}，",
        "intro": "此前来信关于{原主题}的事宜，不知您是否方便查阅。",
        "body": "{跟进内容}",
        "closing": "如有任何疑问，随时告知。祝好！",
        "signature": "{发件人}"
    },
    "感谢": {
        "subject": "感谢您的{事项}",
        "greeting": "您好{姓名}，",
        "intro": "非常感谢您{感谢原因}。",
        "body": "{具体感谢内容}",
        "closing": "期待未来有更多合作机会！",
        "signature": "{发件人}"
    },
    "报价": {
        "subject": "关于{项目}的报价方案",
        "greeting": "您好{姓名}，",
        "intro": "感谢您对{产品/服务}的关注，根据您的需求，我们准备了以下方案：",
        "body": "{报价详情}",
        "closing": "报价有效期{有效期}，如有任何调整需求欢迎沟通。",
        "signature": "{发件人}\n{职位}\n{公司}"
    },
    "拒绝": {
        "subject": "关于{事项}的反馈",
        "greeting": "您好{姓名}，",
        "intro": "感谢您的{事项}申请/提案，经过慎重评估，我们暂时无法推进。",
        "body": "{拒绝原因}。我们会在{未来时机}重新评估。",
        "closing": "感谢您的理解，祝顺利！",
        "signature": "{发件人}"
    },
    "道歉": {
        "subject": "关于{事项}的说明与致歉",
        "greeting": "您好{姓名}，",
        "intro": "对于{问题}给贵司/您带来的不便，我们深感抱歉。",
        "body": "{问题原因}。我们已采取{解决方案}，确保不再发生。",
        "closing": "再次为给您造成的困扰致歉，期待您的谅解。",
        "signature": "{发件人}\n{职位}\n{公司}"
    },
    "会议邀请": {
        "subject": "邀请：{会议主题}（{日期}{时间}）",
        "greeting": "您好{姓名}，",
        "intro": "诚挚邀请您参加{会议主题}，详情如下：",
        "body": "📅 日期：{日期}\n🕐 时间：{时间}\n📍 地点：{地点}\n📋 议程：{议程}",
        "closing": "请确认是否方便出席，回复确认即可。",
        "signature": "{发件人}"
    },
    "周报": {
        "subject": "【{周期}周报】{姓名} — {起始日期}",
        "greeting": "各位好，",
        "intro": "以下是{周期}周（{起始日期} - {结束日期}）的工作汇报：",
        "body": "📌 本周完成：\n{完成事项}\n\n📋 下周计划：\n{下周计划}\n\n⚠️ 需要支持：\n{需要支持}",
        "closing": "如有疑问欢迎随时沟通。",
        "signature": "{姓名}"
    },
    "离职告别": {
        "subject": "告别与感谢",
        "greeting": "各位同事，",
        "intro": "怀着不舍的心情，告知大家我将于{离职日期}离开{公司}。",
        "body": "感谢{感谢对象}。在{公司}的{时长}是我职业生涯中宝贵的经历。",
        "closing": "我的联系方式：{联系方式}，欢迎保持联系。江湖再见！",
        "signature": "{发件人}"
    },
    "节日问候": {
        "subject": "{节日}快乐！{祝福语}",
        "greeting": "尊敬的{姓名}，",
        "intro": "金{节日}将至，{公司/发件人}全体同仁恭祝您：",
        "body": "{祝福内容}",
        "closing": "新的一年，期待继续与您携手共进！",
        "signature": "{公司}\n{发件人}"
    }
}


def generate_email(scenario, **kwargs):
    """生成邮件内容"""
    if scenario not in TEMPLATES:
        available = ', '.join(TEMPLATES.keys())
        print(f"未知场景。可用场景：{available}")
        return None
    
    t = TEMPLATES[scenario]
    
    # 填充模板
    subject = t["subject"].format(**kwargs)
    greeting = t["greeting"].format(**kwargs).replace("{姓名}", kwargs.get("姓名", ""))
    intro = t["intro"].format(**kwargs)
    body = t["body"].format(**kwargs)
    closing = t["closing"].format(**kwargs)
    signature = t["signature"].format(**kwargs)
    
    # 组装邮件
    email = f"""【邮件主题】
{subject}

【收件人】
{kwargs.get('收件人', '[收件人邮箱]')}

{greeting}
{intro}

{body}

{closing}

{signature}"""
    return email


def list_scenarios():
    print("可用场景：")
    for i, name in enumerate(TEMPLATES.keys(), 1):
        print(f"  {i}. {name}")
    print("\n用法: python email_template.py <场景> <键1=值1> <键2=值2> ...")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h', 'help']:
        list_scenarios()
        print("\n示例:")
        print('  python email_template.py 初次联系 发件人=张三 职位=产品经理 姓名=李四 公司=XX科技 目的=合作开发 收件人=contact@example.com')
        print('  python email_template.py 周报 姓名=张三 周期=本周 起始日期=4月14日 结束日期=4月18日 完成事项="- 项目A完成\\n- 客户B签约"')
        sys.exit(0)
    
    scenario = sys.argv[1]
    kwargs = {}
    
    for arg in sys.argv[2:]:
        if '=' in arg:
            k, v = arg.split('=', 1)
            kwargs[k] = v
    
    email = generate_email(scenario, **kwargs)
    if email:
        print(email)


if __name__ == '__main__':
    main()
