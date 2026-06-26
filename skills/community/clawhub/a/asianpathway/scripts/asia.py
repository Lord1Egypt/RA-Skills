#!/usr/bin/env python3
"""亚洲直通车课程助手 - CLI入口"""
import sys

COMMANDS = {
    "overview": "亚洲班课程全貌概览",
    "pathway": "查看特定国家升学路径：asia pathway <国家>（支持：新加坡/马来西亚/韩国/日本）",
    "compare": "对比四条升学路径的差异",
    "subjects": "展示课程科目设置和选课建议",
    "activities": "展示社团和实践项目体系",
    "faq": "常见问题解答",
    "help": "显示所有命令帮助"
}

def cmd_help():
    print("📋 亚洲直通车课程助手 - 可用命令")
    print("="*50)
    for name, desc in COMMANDS.items():
        print(f"  {name:10s}  {desc}")
    print()
    print("示例: asia overview | asia pathway 新加坡 | asia compare")

def cmd_overview():
    print("🌏 亚洲直通车课程全貌")
    print("="*50)
    print()
    print("定位: 科德高中融合部亚洲班，面向以亚洲大学为目标的学生")
    print()
    print("核心课程结构:")
    print("  1. 基础学术课程（数学/英语/科学/社科）")
    print("  2. 亚洲语言课程（日语/韩语）")
    print("  3. 升学预备课程（雅思/TOPIK/JLPT备考）")
    print("  4. 特色实践项目（户外/社团/研学）")
    print()
    print("目标升学国家:")
    print("  🇸🇬 新加坡 — NUS / NTU / SMU")
    print("  🇲🇾 马来西亚 — 马来亚大学 / 英澳名校分校")
    print("  🇰🇷 韩国 — 首尔大学 / 高丽大学 / 延世大学（SKY）")
    print("  🇯🇵 日本 — 东京大学 / 京都大学 / 早稻田 / 庆应（SGU英文项目）")
    print()
    print("使用 asia pathway <国家> 查看详细升学路径")

def cmd_pathway(country):
    pathways = {
        "新加坡": "🇸🇬 新加坡升学路径\n" + "="*40 + "\n\n"
            "目标大学: 新加坡国立大学(NUS)、南洋理工(NTU)、新加坡管理大学(SMU)\n"
            "申请要求:\n"
            "  • A-Level: 3A（含数学），建议进阶数学\n"
            "  • 雅思: 6.5+\n"
            "  • NUS国际生录取率约5-8%\n"
            "  • 2027年起所有新加坡学生必修AI课程\n\n"
            "融合部适配: A-Level数学+物理/经济+雅思 → NUS/NTU\n"
            "建议选科: 数学+进阶数学+物理/经济\n\n"
            "关键节点: 申请截止约每年2月，7月底前出A-Level成绩",

        "马来西亚": "🇲🇾 马来西亚升学路径\n" + "="*40 + "\n\n"
            "目标大学: 马来亚大学(UM)、莫纳什马来西亚、诺丁汉马来西亚等英澳分校\n"
            "申请要求:\n"
            "  • A-Level: 2-3科通过\n"
            "  • 雅思: 6.0-6.5\n"
            "  • 英澳名校分校成本仅为欧美1/3\n\n"
            "融合部适配: A-Level任意三科+雅思 → 英澳名校马来西亚分校\n"
            "优势: 性价比最高，英联邦体系，可作为跳板",

        "韩国": "🇰🇷 韩国升学路径\n" + "="*40 + "\n\n"
            "目标大学: 首尔大学(SNU)、高丽大学、延世大学（SKY联盟）\n"
            "申请要求:\n"
            "  • 韩语: TOPIK 3-5级（根据学校和专业）\n"
            "  • 部分大学接受英语授课申请\n"
            "  • 高中成绩单+推荐信+面试\n\n"
            "融合部适配: A-Level+韩语 → 韩国SKY\n"
            "关键: 韩语能力是决定因素，建议同时准备英语成绩",

        "日本": "🇯🇵 日本升学路径（SGU英文授课）\n" + "="*40 + "\n\n"
            "目标大学: 东大、京大、早稻田、庆应（SGU英文项目）\n"
            "SGU项目: 37所大学开设英文授课项目，无需日语N1\n"
            "申请要求:\n"
            "  • A-Level/IB/SAT 成绩\n"
            "  • 英语: 雅思6.0+/托福80+\n"
            "  • 部分学校需要面试\n\n"
            "融合部适配: A-Level+英语成绩 → 日本SGU项目\n"
            "优势: 不需要日语就能申请，文化相近，学费低廉\n\n"
            "2026年新兴方向:\n"
            "  • 早稻田: AI治理与风险管理\n"
            "  • 东京大学: 生成式AI与创意计算（硕士阶段）"
    }
    for key, content in pathways.items():
        if key in country:
            print(content)
            return
    print(f"❌ 没有'{country}'的路径信息。试试：新加坡、马来西亚、韩国、日本")

def cmd_compare():
    print("📊 四条升学路径对比")
    print("="*60)
    print(f"{'维度':12s} {'新加坡':14s} {'马来西亚':14s} {'韩国':14s} {'日本':14s}")
    print("-"*60)
    print(f"{'语言要求':12s} {'雅思6.5+':14s} {'雅思6.0+':14s} {'TOPIK 3-5':14s} {'雅思6.0+':14s}")
    print(f"{'A-Level':12s} {'3A(含数学)':14s} {'2-3科通过':14s} {'3科通过':14s} {'3科通过':14s}")
    print(f"{'年费用':12s} {'高(15-25万)':14s} {'低(5-10万)':14s} {'中(8-15万)':14s} {'中(8-12万)':14s}")
    print(f"{'竞争度':12s} {'🔥🔥🔥🔥':14s} {'🔥🔥':14s} {'🔥🔥🔥':14s} {'🔥🔥🔥':14s}")
    print(f"{'QS排名':12s} {'NUS#8/NTU#12':14s} {'UM#65':14s} {'SNU#31':14s} {'东大#28':14s}")
    print()
    print("建议: 选路径不是选国家，是选学生的匹配度。")

def cmd_subjects():
    print("📚 亚洲班科目设置与选课建议")
    print("="*50)
    print()
    print("核心科目（必修）:")
    print("  📐 数学 — 所有路径通用，最低门槛")
    print("  📖 英语 — 雅思备考基础")
    print("  🌐 亚洲语言 — 日语/韩语（根据目标国家选择）")
    print()
    print("选修科目（根据目标国家/专业选择）:")
    print("  📊 经济 — 商科方向（新加坡金融/韩国经营学）")
    print("  🔬 物理 — 工程/CS方向（NUS/NTU工科）")
    print("  🧪 化学 — 医学/材料方向")
    print("  💻 计算机 — AI/数据方向（强烈推荐）")
    print("  🏛️ 历史/地理 — 人文社科方向")
    print()
    print("推荐组合:")
    print("  🅰 数学+经济+亚洲语言 → 商科/经营学方向")
    print("  🅱 数学+物理+计算机 → 工科/AI方向")
    print("  🅲 数学+经济+计算机 → 金融科技方向")

def cmd_activities():
    print("🎯 社团与实践项目体系")
    print("="*50)
    print()
    print("社团活动:")
    print("  • 户外探索社（Jessie 主理——户外实践型教学）")
    print("  • AI创新社")
    print("  • 模拟联合国")
    print("  • 韩流文化社 / 日本动漫社")
    print("  • 商业模拟社")
    print()
    print("研学项目:")
    print("  • 新加坡名校研学营")
    print("  • 日本科技文化研学")
    print("  • 韩国K-pop文化体验")
    print("  • 马来西亚英校短期交换")
    print()
    print("竞赛项目:")
    print("  • 新加坡NUS/NTU AI创新挑战赛")
    print("  • 日本SGU英文辩论赛")
    print("  • 韩国SKY商业案例分析赛")

def cmd_faq():
    print("❓ 亚洲班常见问题")
    print("="*50)
    print()
    faqs = [
        ("亚洲班和A-Level班能互转吗？", "视学生进度和课程匹配度而定，建议在G10阶段确定方向。"),
        ("零基础学日语/韩语来得及吗？", "亚洲班从零基础开始教学，G10开始学，到申请时可达中级水平（TOPIK 3-4 / JLPT N3-N2）。"),
        ("新加坡NUS/NTU好申请吗？", "NUS国际生录取率约5-8%，竞争激烈。A-Level 3A+数学是门槛，进阶数学是加分项。"),
        ("日本SGU项目需要日语吗？", "不需要。SGU是英文授课项目，直接用A-Level/IB/雅思申请。但会日语会加分。"),
        ("毕业后可以留当地工作吗？", "新加坡/马来西亚：可申请工作签证。韩国：毕业后签证延长至2年。日本：就业签证政策持续优化。"),
    ]
    for i, (q, a) in enumerate(faqs, 1):
        print(f"Q{i}: {q}")
        print(f"A: {a}")
        print()

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("help", "--help", "-h"):
        cmd_help()
        return
    cmd = sys.argv[1]
    if cmd == "overview":
        cmd_overview()
    elif cmd == "pathway":
        cmd_pathway(" ".join(sys.argv[2:]) if len(sys.argv) > 2 else "")
    elif cmd == "compare":
        cmd_compare()
    elif cmd == "subjects":
        cmd_subjects()
    elif cmd == "activities":
        cmd_activities()
    elif cmd == "faq":
        cmd_faq()
    else:
        cmd_help()

if __name__ == "__main__":
    main()
