#!/usr/bin/env python3
"""
AI 法律合规检查工具 v1.0
用法:
  python ai_compliance_check.py                       # 交互模式
  python ai_compliance_check.py --scenario personal    # 个人/商用场景
  python ai_compliance_check.py --scenario enterprise  # 企业AI办公场景
  python ai_compliance_check.py --scenario service     # 对外AI服务场景
  python ai_compliance_check.py --redline              # 违规红线速查
  python ai_compliance_check.py --filing                # 算法备案流程
  python ai_compliance_check.py --labeling              # AI内容标识要求
  python ai_compliance_check.py --regulations           # 法规速查表
功能: 根据用户场景输出结构化合规检查报告
"""

import sys
import json
from datetime import datetime

# ============================================================
# 法规速查表
# ============================================================
REGULATIONS = {
    "gen_ai": {
        "name": "生成式人工智能服务管理暂行办法",
        "effective_date": "2023.08.15",
        "key_articles": "第4条(训练数据), 第7条(内容安全), 第9条(用户权益), 第14-17条(备案与评估)",
        "url": "https://www.gov.cn/zhengce/zhengceku/202307/content_6891752.htm"
    },
    "deep_synthesis": {
        "name": "互联网信息服务深度合成管理规定",
        "effective_date": "2023.01.10",
        "key_articles": "第6条(标识义务), 第14条(安全评估), 第17条(算法备案), 第19条(数据管理)",
        "url": "https://www.gov.cn/zhengce/zhengceku/2022-12/12/content_5731431.htm"
    },
    "anthropomorphic": {
        "name": "人工智能拟人化互动服务管理暂行办法（⚠️ 征求意见稿，尚未施行）",
        "effective_date": "征求意见稿（2025.12.27 发布，尚未施行）",
        "key_articles": "未成年人保护, 情感操纵禁止, 2小时提醒, 安全评估（均为征求意见稿内容，正式稿可能调整，不得作为执法依据）",
        "url": "https://www.cac.gov.cn/（检索：人工智能拟人化互动服务管理暂行办法 征求意见）"
    },
    "labeling": {
        "name": "人工智能生成合成内容标识办法",
        "effective_date": "2025.09.01",
        "key_articles": "第4-6条(显式标识), 第7-9条(隐式标识), 第10条(用户义务), 第11条(平台义务)",
        "url": "https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm"
    },
    "algorithm": {
        "name": "互联网信息服务算法推荐管理规定",
        "effective_date": "2022.03.01",
        "key_articles": "第6条(服务提供者义务), 第8条(用户选择权), 第9条(拒绝权), 第24条(算法备案), 第17条(大数据杀熟禁止)",
        "url": "https://www.gov.cn/zhengce/zhengceku/2022-01/04/content_5666429.htm"
    },
    "face_recognition": {
        "name": "人脸识别技术应用安全管理办法",
        "effective_date": "2025.06.01",
        "key_articles": "单独同意, 非唯一验证, 10万人备案, 私密空间禁止安装",
        "url": "https://www.cac.gov.cn/2025-03/21/c_1744174262156096.htm"
    },
    "weather_ai": {
        "name": "人工智能气象应用服务办法",
        "effective_date": "2025年",
        "key_articles": "AI气象服务专项管控（参考性）",
        "url": "https://www.cac.gov.cn/2025-03/04/c_1741640826321320.htm"
    }
}

# ============================================================
# 三套合规检查表
# ============================================================
PERSONAL_CHECKLIST = [
    {"item": "是否了解AI生成内容需主动标识", "law": "标识办法第10条", "risk": "中"},
    {"item": "发布AI生成图文是否添加水印/声明", "law": "标识办法第4-6条", "risk": "高"},
    {"item": "是否侵犯他人肖像权（AI换脸等）", "law": "民法典第1019条", "risk": "高"},
    {"item": "是否侵犯他人著作权（训练素材/生成内容）", "law": "著作权法", "risk": "中"},
    {"item": "AI生成内容是否含虚假信息", "law": "生成式AI办法第7条", "risk": "高"},
    {"item": "是否用于诈骗/侵权/不正当竞争", "law": "民法典/刑法", "risk": "极高"},
    {"item": "是否向未成年人提供不适宜内容", "law": "拟人化互动办法", "risk": "极高"},
    {"item": "AI换脸/语音合成是否获得当事人同意", "law": "深度合成规定第6条", "risk": "高"},
    {"item": "是否了解AI产出物的版权归属规则", "law": "著作权法", "risk": "中"},
    {"item": "是否散布AI生成的虚假信息", "law": "网络安全法/治安管理处罚法", "risk": "极高"},
    {"item": "是否在电商/广告中使用AI生成虚假内容", "law": "广告法/反不正当竞争法", "risk": "高"},
    {"item": "是否保留AI生成过程的创作记录（版权举证）", "law": "著作权法", "risk": "中"},
]

ENTERPRISE_CHECKLIST = [
    {"item": "是否制定企业AI使用内部管理制度", "law": "数据安全法第29条", "risk": "中"},
    {"item": "AI处理员工个人信息是否取得同意", "law": "个人信息保护法第13条", "risk": "高"},
    {"item": "AI自动化决策是否提供说明和拒绝权", "law": "个人信息保护法第24条", "risk": "高"},
    {"item": "训练数据是否来自合法来源", "law": "生成式AI办法第4条/数据安全法", "risk": "高"},
    {"item": "是否对AI系统进行数据安全分类分级", "law": "数据安全法第21条", "risk": "中"},
    {"item": "重要数据是否进行出境安全评估", "law": "数据安全法第31条/网络数据安全管理条例", "risk": "高"},
    {"item": "AI生成内容是否进行安全审核", "law": "生成式AI办法第7条", "risk": "高"},
    {"item": "是否建立AI内容投诉举报机制", "law": "生成式AI办法第10条", "risk": "中"},
    {"item": "是否使用人脸识别技术且未取得单独同意", "law": "人脸识别管理办法", "risk": "极高"},
    {"item": "AI办公系统是否通过网络安全等级保护测评", "law": "网络安全法第21条", "risk": "中"},
    {"item": "是否制定数据泄露应急预案", "law": "数据安全法第29条", "risk": "中"},
    {"item": "外包AI服务是否签署数据处理协议", "law": "个人信息保护法第21条", "risk": "中"},
    {"item": "是否对AI决策结果保留可追溯记录", "law": "个人信息保护法第24条", "risk": "中"},
    {"item": "是否评估AI系统对就业/考核的公平性影响", "law": "算法推荐规定第6条", "risk": "中"},
    {"item": "是否完成AI伦理审查（如适用）", "law": "AI伦理审查办法", "risk": "中"},
]

SERVICE_CHECKLIST = [
    {"item": "是否完成算法备案（10个工作日内）", "law": "算法推荐规定第24条/深度合成规定第17条/生成式AI办法第17条", "risk": "极高"},
    {"item": "是否开展安全评估", "law": "生成式AI办法第15条/深度合成规定第14条", "risk": "极高"},
    {"item": "AI生成内容是否添加显式标识（文字/图标）", "law": "标识办法第4-6条", "risk": "极高"},
    {"item": "AI生成内容是否添加隐式标识（元数据）", "law": "标识办法第7-9条", "risk": "极高"},
    {"item": "是否禁止用户删除/篡改AI标识", "law": "标识办法第13条", "risk": "高"},
    {"item": "训练数据是否取得个人信息主体同意", "law": "个人信息保护法/生成式AI办法第4条", "risk": "极高"},
    {"item": "训练数据是否侵犯他人知识产权", "law": "著作权法/生成式AI办法第4条", "risk": "高"},
    {"item": "是否建立内容安全审核机制", "law": "生成式AI办法第7条/网络安全法", "risk": "高"},
    {"item": "是否提供用户投诉举报渠道", "law": "生成式AI办法第10条", "risk": "中"},
    {"item": "是否保障用户选择权/拒绝权（算法推荐）", "law": "算法推荐规定第8-9条", "risk": "高"},
    {"item": "是否禁止大数据杀熟（差别定价）", "law": "算法推荐规定第17条", "risk": "高"},
    {"item": "是否完成AI伦理审查", "law": "AI伦理审查办法", "risk": "中"},
    {"item": "是否向未成年人提供虚拟伴侣/情感诱导服务", "law": "拟人化互动办法", "risk": "极高"},
    {"item": "拟人化服务是否设置2小时提醒+退出途径", "law": "拟人化互动办法", "risk": "高"},
    {"item": "是否使用人脸识别且满足合规条件", "law": "人脸识别管理办法", "risk": "极高"},
    {"item": "是否进行个人信息保护影响评估", "law": "个人信息保护法第55-56条", "risk": "高"},
    {"item": "是否签订用户协议并公示服务规则", "law": "生成式AI办法第10条", "risk": "中"},
    {"item": "是否留存算法日志（6个月以上）", "law": "算法推荐规定第14条", "risk": "中"},
]

# ============================================================
# 违规红线清单
# ============================================================
REDLINES = {
    "内容安全": [
        "生成法律、行政法规禁止的内容",
        "生成暴力/淫秽/虚假信息",
        "AI生成虚假新闻并传播",
        "AI生成内容涉及危害国家安全",
    ],
    "深度合成": [
        "AI换脸未取得当事人同意",
        "深度合成内容未添加标识",
        "删除/篡改/伪造深度合成标识",
        "利用深度合成实施诈骗",
    ],
    "算法推荐": [
        "未完成算法备案即上线服务",
        "大数据杀熟（同品不同价）",
        "未提供算法推荐关闭选项",
        "算法推荐未保障用户选择权",
    ],
    "数据保护": [
        "训练数据非法获取个人信息",
        "重要数据未经安全评估即出境",
        "未建立数据分类分级制度",
        "数据泄露未及时报告主管部门",
    ],
    "拟人化互动": [
        "向未成年人提供虚拟伴侣服务",
        "通过情感操纵诱导用户消费",
        "过度迎合诱导情感依赖",
        "未设置2小时提醒和退出途径",
    ],
    "资质备案": [
        "对外提供生成式AI服务未备案",
        "具有舆论属性未做安全评估",
        "未留存算法日志6个月以上",
        "未建立投诉举报机制",
    ],
    "知识产权": [
        "训练数据侵犯他人著作权",
        "AI生成内容冒充他人作品",
        "AI换脸侵犯肖像权",
        "AI生成内容用于虚假广告",
    ],
}

# ============================================================
# 算法备案流程
# ============================================================
FILING_STEPS = [
    {"step": 1, "name": "确认是否需要备案", "desc": "判断服务是否具有舆论属性或社会动员能力", "deadline": "服务上线前评估"},
    {"step": 2, "name": "准备备案材料", "desc": "服务提供者信息、服务形式、应用领域、算法类型、自评估报告", "deadline": "10个工作日内"},
    {"step": 3, "name": "登录备案系统", "desc": "访问 https://beian.cac.gov.cn 注册并填写", "deadline": "-"},
    {"step": 4, "name": "提交算法自评估报告", "desc": "含算法原理、数据来源、安全措施、风险评估", "deadline": "-"},
    {"step": 5, "name": "配合网信办审核", "desc": "网信办30个工作日内完成审核，可能要求补充材料", "deadline": "30个工作日"},
    {"step": 6, "name": "获取备案编号", "desc": "审核通过后获得备案编号，需在服务中公示", "deadline": "-"},
    {"step": 7, "name": "持续合规", "desc": "算法变更需10个工作日内更新备案；留存日志≥6个月", "deadline": "持续"},
]

# ============================================================
# AI内容标识要求
# ============================================================
LABELING_REQUIREMENTS = {
    "显式标识": {
        "文本": "在文本首尾添加文字提示（如『本内容由AI生成』）",
        "图片": "添加显著视觉标识（水印/角标）",
        "视频": "起始画面添加标识，持续≥3秒",
        "音频": "在开头添加语音提示",
    },
    "隐式标识": {
        "元数据": "文件元数据中添加生成合成内容属性信息",
        "信息项": "服务提供者名称/编码、内容编号、生成时间",
    },
    "用户义务": "发布AI生成内容须主动声明并使用标识功能",
    "平台义务": "核验元数据中是否有隐式标识，添加提示标识",
    "禁止行为": "不得删除、篡改、伪造、隐匿标识",
}

# ============================================================
# 核心函数
# ============================================================

def print_regulations():
    """打印法规速查表"""
    print("\n" + "=" * 70)
    print("📋 AI 专项部门规章速查表（7 部）")
    print("=" * 70)
    for key, reg in REGULATIONS.items():
        print(f"\n  [{reg['effective_date']}] {reg['name']}")
        print(f"  关键条款: {reg['key_articles']}")
        print(f"  来源: {reg['url']}")
    print("\n" + "=" * 70)
    print("⚠️  注: 法规内容详见 references/ai_regulations_compendium.md")
    print("    基础法律 AI 法条详见 references/basic_laws_ai_provisions.md")


def run_checklist(scenario):
    """运行合规检查表"""
    checklists = {
        "personal": ("个人/商用场景", PERSONAL_CHECKLIST),
        "enterprise": ("企业AI办公场景", ENTERPRISE_CHECKLIST),
        "service": ("对外AI服务场景", SERVICE_CHECKLIST),
    }

    if scenario not in checklists:
        print("未知场景。可用: personal, enterprise, service")
        return

    title, items = checklists[scenario]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "=" * 70)
    print(f"🔍 AI 合规检查报告 — {title}")
    print(f"⏰ 检查时间: {timestamp}")
    print("=" * 70)

    risk_order = {"极高": 0, "高": 1, "中": 2, "低": 3}
    sorted_items = sorted(items, key=lambda x: risk_order.get(x["risk"], 99))

    high_count = sum(1 for i in sorted_items if i["risk"] in ("极高", "高"))

    for i, item in enumerate(sorted_items, 1):
        risk_icon = {"极高": "🔴", "高": "🟠", "中": "🟡", "低": "🟢"}.get(item["risk"], "⚪")
        print(f"\n  {i}. [{risk_icon} {item['risk']}] {item['item']}")
        print(f"     适用法规: {item['law']}")

    print("\n" + "=" * 70)
    print(f"📊 检查结果汇总:")
    print(f"   检查项目: {len(sorted_items)} 项")
    print(f"   高风险项: {high_count} 项（需优先处理）")
    print(f"   合规状态: {'❌ 存在高风险项，需立即整改' if high_count > 0 else '✅ 未发现高风险项'}")
    print("=" * 70)
    print("\n⚠️  注: 本工具提供合规筛查参考，不构成正式法律意见。")
    print("    复杂场景建议咨询专业律师。")


def print_redlines():
    """打印违规红线清单"""
    print("\n" + "=" * 70)
    print("🚫 AI 违规红线清单")
    print("=" * 70)
    total = 0
    for category, items in REDLINES.items():
        print(f"\n  【{category}】({len(items)}条)")
        for i, item in enumerate(items, 1):
            print(f"    {i}. {item}")
            total += 1
    print(f"\n  共 {total} 条违规红线行为")
    print("\n" + "=" * 70)
    print("⚠️  注: 触碰红线可能导致: 罚款、责令整改、下架服务、吊销许可、")
    print("    行政处罚甚至刑事责任。详见 references/violation_redlines.md")


def print_filing_guide():
    """打印算法备案流程"""
    print("\n" + "=" * 70)
    print("📝 算法备案流程指南")
    print("   备案平台: https://beian.cac.gov.cn")
    print("=" * 70)
    for step in FILING_STEPS:
        print(f"\n  步骤 {step['step']}: {step['name']}")
        print(f"  描述: {step['desc']}")
        print(f"  时限: {step['deadline']}")
    print("\n" + "=" * 70)
    print("⚠️  注: 详细材料清单和自评估报告模板见 references/algorithm_filing_guide.md")


def print_labeling_guide():
    """打印AI内容标识要求"""
    print("\n" + "=" * 70)
    print("🏷️  AI 生成合成内容标识要求")
    print("   生效日期: 2025.09.01")
    print("=" * 70)
    print("\n  【显式标识】（用户可感知）")
    for media, req in LABELING_REQUIREMENTS["显式标识"].items():
        print(f"    {media}: {req}")
    print("\n  【隐式标识】（元数据层面）")
    for key, req in LABELING_REQUIREMENTS["隐式标识"].items():
        print(f"    {key}: {req}")
    print(f"\n  用户义务: {LABELING_REQUIREMENTS['用户义务']}")
    print(f"  平台义务: {LABELING_REQUIREMENTS['平台义务']}")
    print(f"  禁止行为: {LABELING_REQUIREMENTS['禁止行为']}")
    print("\n" + "=" * 70)


def interactive_mode():
    """交互模式"""
    print("\n" + "=" * 70)
    print("⚖️  AI 法律合规检查工具 v1.0")
    print("=" * 70)
    print("""
  请选择检查模式:

  [1] 个人/商用场景合规检查
  [2] 企业AI办公场景合规检查
  [3] 对外AI服务场景合规检查
  [4] 违规红线速查
  [5] 算法备案流程指南
  [6] AI内容标识要求
  [7] 法规速查表
  [0] 退出
""")
    try:
        choice = input("  请输入选项编号: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n  已退出。")
        return

    actions = {
        "1": lambda: run_checklist("personal"),
        "2": lambda: run_checklist("enterprise"),
        "3": lambda: run_checklist("service"),
        "4": print_redlines,
        "5": print_filing_guide,
        "6": print_labeling_guide,
        "7": print_regulations,
        "0": lambda: print("\n  已退出。"),
    }
    action = actions.get(choice)
    if action:
        action()
    else:
        print("  无效选项。")


def main():
    if len(sys.argv) < 2:
        interactive_mode()
        return

    arg = sys.argv[1]

    if arg == "--scenario":
        if len(sys.argv) < 3:
            print("用法: python ai_compliance_check.py --scenario <personal|enterprise|service>")
            sys.exit(1)
        run_checklist(sys.argv[2])
    elif arg == "--redline":
        print_redlines()
    elif arg == "--filing":
        print_filing_guide()
    elif arg == "--labeling":
        print_labeling_guide()
    elif arg == "--regulations":
        print_regulations()
    elif arg == "--help" or arg == "-h":
        print("AI 法律合规检查工具 v1.0")
        print("用法:")
        print("  python ai_compliance_check.py                       # 交互模式")
        print("  python ai_compliance_check.py --scenario personal    # 个人/商用场景")
        print("  python ai_compliance_check.py --scenario enterprise  # 企业AI办公场景")
        print("  python ai_compliance_check.py --scenario service     # 对外AI服务场景")
        print("  python ai_compliance_check.py --redline              # 违规红线速查")
        print("  python ai_compliance_check.py --filing                # 算法备案流程")
        print("  python ai_compliance_check.py --labeling              # AI内容标识要求")
        print("  python ai_compliance_check.py --regulations           # 法规速查表")
    else:
        print(f"未知参数: {arg}")
        print("使用 --help 查看用法。")


if __name__ == "__main__":
    main()
