#!/usr/bin/env python3
"""
AI副业真伪鉴别器 - ai-side-hustle-checker
基于规则引擎分析副业项目的可信度

用法:
  python3 hustle_checker.py --interactive
  python3 hustle_checker.py --project "用AI写小红书月入过万"
  python3 hustle_checker.py --course "AI副业训练营"
"""

import json
import re
import sys
import argparse
from datetime import datetime

# ========== 骗术特征库 ==========

RED_FLAGS = [
    # 收益类
    (r"月\s*入\s*\d+\s*万", "收益承诺过高，无具体数据支撑"),
    (r"日\s*赚\s*\d+", "日赚承诺典型收割套路"),
    (r"躺\s*赚", "躺赚承诺绝对虚假"),
    (r"被\s*动\s*收\s*入?\s*\d+", "被动收入夸大，周期不明"),
    (r"一\s*定\s*能\s*(赚|成功)", "绝对化承诺，违反广告法"),
    (r"立\s*刻?\s*(变现|赚钱|暴富)", "即时变现承诺不可信"),
    (r"只\s*需?\s*每天\s*\d+\s*分", "极短时间承诺高收益"),
    (r"轻\s*松\s*(赚|日)", "轻松赚钱是典型话术"),

    # 门槛类
    (r"零\s*基\s*础", "零基础+高收益=典型骗局"),
    (r"不\s*需?\s*任\s*何\s*经\s*验", "无门槛+高回报=收割"),
    (r"普\s*通\s*人", "普通人也能=收割话术"),
    (r"小\s*白", "小白也能=收割话术"),
    (r"不\s*用\s*(学习|学)", "无需学习=虚假宣传"),

    # 焦虑类
    (r"最\s*后\s*(一?\s*次|机会|名额)", "限量紧迫感=催单套路"),
    (r"即\s*将\s*涨\s*价", "涨价压迫=催单套路"),
    (r"别\s*人\s*(已经|都)\s*(在|月入)", "社交证明造假"),
    (r"错\s*过\s*就", "错过恐慌=催单套路"),
    (r"月\s*薪\s*翻\s*\d", "薪资翻倍=虚假焦虑"),

    # 套路类
    (r"先\s*付\s*(定金|学费|费用)", "预付款是风险信号"),
    (r"限\s*量", "限量=催单套路"),
    (r"内\s*部\s*(渠|名|消)", "内部渠道=伪造可信度"),
    (r"秘\s*密", "神秘感=制造信息差假象"),
    (r"老\s*板\s*(不\s*知|不会)", "贬低他人抬高自己=套路"),
    (r"别\s*人\s*告\s*诉\s*你", "隐藏信息=制造焦虑"),

    # 课程类
    (r"训\s*练\s*营", "训练营需警惕教学质量"),
    (r"陪\s*跑", "陪跑服务难量化"),
    (r"收\s*益\s*分\s*成", "分成模式需警惕跑路风险"),
    (r"拉\s*新\s*?(人|下线)", "拉新分成=传销特征"),
    (r"裂\s*变", "裂变=传销特征"),
    (r"代\s*理", "代理模式风险高"),
]

# 绿色信号
GREEN_FLAGS = [
    (r"需\s*要\s*\d+\s*个?\s*月", "明确收益周期"),
    (r"\d+\s*-\s*\d+\s*个?\s*月", "收益周期合理"),
    (r"需\s*要\s*(学习|投入|努力)", "承认需要付出"),
    (r"不\s*保\s*证", "不保证收益=诚信"),
    (r"具\s*体\s*步\s*骤", "有具体步骤=可验证"),
    (r"真\s*实\s*案\s*例", "真实案例=有据可查"),
    (r"有\n?效\s*退", "退款保障=风险降低"),
    (r"第\s*一\s*次", "首次尝试=低风险"),
    (r"从\s*\d+\s*开\s*始", "从低开始=合理预期"),
    (r"不\s*是\s*(躺|快|暴)", "明确说明不是轻松赚钱"),
]

# 具体副业类型评估
PROJECT_TYPES = {
    "小红书": {
        "base_score": 65,
        "realistic": "月入500-5000（需3-6个月积累）",
        "keys": "内容质量+持续更新+个人特色",
        "risks": "竞争激烈，同质化严重"
    },
    "AI写作": {
        "base_score": 60,
        "realistic": "月入500-3000（需建立客户关系）",
        "keys": "接单能力+AI辅助效率+专业领域",
        "risks": "价格战严重，客户难找"
    },
    "AI课程": {
        "base_score": 30,
        "realistic": "卖课本身可赚钱，但需真实实力",
        "keys": "有真实受众+专业积累+交付能力",
        "risks": "课程市场已饱和，口碑难建立"
    },
    "AI工具推荐": {
        "base_score": 40,
        "realistic": "联盟佣金可赚，但需流量基础",
        "keys": "有垂直流量+真实推荐+信任背书",
        "risks": "竞争激烈，真实推荐难维持"
    },
    "AI代写服务": {
        "base_score": 70,
        "realistic": "月入1000-8000（需稳定客户）",
        "keys": "专业领域+交付速度+沟通能力",
        "risks": "价格透明化，单价下降"
    },
    "AI数字人": {
        "base_score": 35,
        "realistic": "高客单价但获客难",
        "keys": "有企业客户+视频制作能力",
        "risks": "技术门槛高，竞争已激烈"
    },
    "AI心理咨询": {
        "base_score": 50,
        "realistic": "可做但需专业背景",
        "keys": "心理学背景+AI辅助+伦理边界",
        "risks": "伦理风险，资质要求"
    },
    "AI数据分析": {
        "base_score": 75,
        "realistic": "月入3000-20000（有技术门槛）",
        "keys": "数据分析能力+行业知识+可视化",
        "risks": "需持续学习新技术"
    },
    "AI绘图": {
        "base_score": 55,
        "realistic": "月入1000-8000（需风格建立）",
        "keys": "审美能力+AI工具熟练+持续出新",
        "risks": "AI绘图泛滥，价格下降"
    },
    "微信公众号": {
        "base_score": 60,
        "realistic": "广告+打赏变现需1-2年积累",
        "keys": "垂直领域+持续输出+私域运营",
        "risks": "公众号红利期已过"
    },
    "知乎": {
        "base_score": 65,
        "realistic": "赞赏+付费咨询+致知计划",
        "keys": "专业深度+持续输出+粉丝积累",
        "risks": "冷启动难，收益周期长"
    },
    "抖店/电商": {
        "base_score": 45,
        "realistic": "有真实机会但失败率高",
        "keys": "选品能力+资金+供应链",
        "risks": "资金要求高，失败率高"
    },
    "B站UP主": {
        "base_score": 60,
        "realistic": "平台收益+接广告，需1年以上",
        "keys": "内容创意+持续更新+粉丝互动",
        "risks": "竞争激烈，收益周期长"
    },
}

# ========== 分析函数 ==========

def detect_type(text):
    """检测副业类型"""
    text_lower = text.lower()
    for ptype, info in PROJECT_TYPES.items():
        if ptype in text or ptype[:2] in text:
            return ptype, info
    return None, None


def check_red_flags(text):
    """检测红灯信号"""
    flags = []
    for pattern, description in RED_FLAGS:
        if re.search(pattern, text):
            flags.append(description)
    return flags


def check_green_flags(text):
    """检测绿灯信号"""
    flags = []
    for pattern, description in GREEN_FLAGS:
        if re.search(pattern, text):
            flags.append(description)
    return flags


def estimate_score(text, red_flags, green_flags):
    """估算可信度评分"""
    base = 50

    # 红灯扣分
    for _ in red_flags:
        base -= 10

    # 绿灯加分
    for _ in green_flags:
        base += 7

    # 副业类型加成
    ptype, info = detect_type(text)
    if info:
        base += (info["base_score"] - 50) * 0.3  # 部分参考类型基准

    return max(0, min(100, base))


def get_rating(score):
    """获取评级"""
    if score >= 80:
        return "🟢 真实机会", "这套模式是可行的，但需要付出真实努力，不保证快速暴富。"
    elif score >= 60:
        return "🟡 需谨慎", "有机会，但存在夸大成分。认真评估自身能力后再决定。"
    elif score >= 40:
        return "🟠 高风险", "多数是坑，少数有真实价值。建议谨慎或换方向。"
    else:
        return "🔴 基本骗局", "典型的割韭菜项目，建议远离或极度谨慎。"


def analyze(text):
    """完整分析"""
    text_lower = text.lower()

    # 1. 检测副业类型
    ptype, ptype_info = detect_type(text)

    # 2. 检测红灯绿灯
    red_flags = check_red_flags(text)
    green_flags = check_green_flags(text)

    # 3. 计算评分
    score = estimate_score(text, red_flags, green_flags)
    rating, rating_desc = get_rating(score)

    # 4. 识别具体问题
    issues = []
    if any("收益承诺" in f or "过高" in f for f in red_flags):
        issues.append("收益承诺过高，与实际情况不符")
    if any("普通" in f or "零基" in f for f in red_flags):
        issues.append("强调普通人也能做，掩盖了真实门槛")
    if any("限量" in f or "涨价" in f or "最后" in f for f in red_flags):
        issues.append("限时压迫催单，是典型销售套路")
    if any("拉新" in f or "代理" in f or "裂变" in f for f in red_flags):
        issues.append("拉新/代理模式有传销风险")
    if "训练营" in text:
        issues.append("训练营教学质量参差不齐，需谨慎评估")

    # 5. 真实成分
    real_parts = []
    if ptype_info:
        real_parts.append("「{}」赛道本身是存在的".format(ptype))
        real_parts.append("合理预期：{}".format(ptype_info["realistic"]))
        real_parts.append("关键成功因素：{}".format(ptype_info["keys"]))
    if green_flags:
        real_parts.append("该项目包含部分合理说明：{}".format("；".join(green_flags[:3])))

    # 6. 修正后评估
    fixed_estimate = ""
    if ptype_info:
        fixed_estimate = "基于「{}」赛道，修正后预期：{}".format(
            ptype, ptype_info["realistic"])
    else:
        fixed_estimate = "建议：以月入{}作为合理目标，而不是宣传中的夸张数字".format(
            "1000-3000" if score > 40 else "0（建议远离）")

    return {
        "score": score,
        "rating": rating,
        "rating_desc": rating_desc,
        "red_flags": red_flags,
        "green_flags": green_flags,
        "project_type": ptype,
        "type_info": ptype_info,
        "issues": issues,
        "real_parts": real_parts,
        "fixed_estimate": fixed_estimate,
        "risks": ptype_info["risks"] if ptype_info else "请参考上方分析"
    }


def generate_report(text, result):
    """生成鉴别报告"""
    lines = []
    lines.append("")
    lines.append("🔎 AI副业真伪鉴别报告")
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("")
    lines.append("📋 项目：「{}」".format(text[:50] + ("..." if len(text) > 50 else "")))
    lines.append("")
    lines.append("📊 可信度评分：{}/100（{}）".format(result["score"], result["rating"]))
    lines.append("💬 {}".format(result["rating_desc"]))

    if result["red_flags"]:
        lines.append("")
        lines.append("⚠️ 风险信号（共{}个）：".format(len(result["red_flags"])))
        seen = set()
        for f in result["red_flags"][:5]:
            if f not in seen:
                lines.append("  🔴 {}".format(f))
                seen.add(f)

    if result["issues"]:
        lines.append("")
        lines.append("🎯 具体问题：")
        for issue in result["issues"]:
            lines.append("  ⚠️ {}".format(issue))

    if result["green_flags"]:
        lines.append("")
        lines.append("✅ 真实成分：")
        for f in result["green_flags"][:3]:
            lines.append("  🟢 {}".format(f))

    if result["real_parts"]:
        lines.append("")
        lines.append("📌 赛道分析：")
        for p in result["real_parts"][:4]:
            lines.append("  📍 {}".format(p))

    lines.append("")
    lines.append("💡 修正后评估：")
    lines.append("  {}".format(result["fixed_estimate"]))

    if result["risks"]:
        lines.append("")
        lines.append("⚠️ 风险提示：")
        lines.append("  {}".format(result["risks"]))

    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("⚡ 快速判断法则：")
    lines.append("  • 月入过万+零基础 = 骗局")
    lines.append("  • 有具体步骤+有门槛 = 可信")
    lines.append("  • 限时优惠+催单 = 收割")
    lines.append("  • 需要拉人 = 远离")

    return "\n".join(lines)


def interactive_mode():
    """交互模式"""
    print("🔎 AI副业真伪鉴别器".center(50, "="))
    print("输入AI副业项目描述，我来帮你分析是否可信")
    print("输入 q 退出\n")

    while True:
        try:
            text = input("💬 请描述项目（粘贴标题/描述）：\n> ").strip()
            if not text:
                continue
            if text.lower() in ["q", "quit", "exit"]:
                print("\n✅ 再见！记住：天下没有免费的午餐。\n")
                break

            result = analyze(text)
            print(generate_report(text, result))
            print()

        except (EOFError, KeyboardInterrupt):
            print("\n\n✅ 再见！\n")
            break


# ========== 主入口 ==========

def main():
    parser = argparse.ArgumentParser(description="🔎 AI副业真伪鉴别器")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="交互模式")
    parser.add_argument("--project", "-p",
                        help="快速评估项目")
    parser.add_argument("--course", "-c",
                        help="鉴别课程")
    parser.add_argument("--scan", "-s",
                        help="扫描关键词")
    parser.add_argument("--json", action="store_true",
                        help="JSON格式输出")
    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
        return

    text = args.project or args.course or args.scan or ""

    if not text:
        print("🔎 AI副业真伪鉴别器")
        print("用法：")
        print("  python3 hustle_checker.py --interactive  # 交互模式")
        print("  python3 hustle_checker.py -p 'AI写小红书月入过万'")
        print("  python3 hustle_checker.py -c 'AI副业训练营'")
        print("  python3 hustle_checker.py -s '月入十万 AI副业'")
        sys.exit(0)

    result = analyze(text)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(generate_report(text, result))


if __name__ == "__main__":
    main()
