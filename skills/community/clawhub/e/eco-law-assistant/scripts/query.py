#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生态环境法典普法与合规助手 - 查询脚本
唯一执行入口，支持条款检索、编号查询、结构概览、合规预检等功能。
"""
import json
import sys
import os
import re

# 加载法典知识库
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "data", "law_articles.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    ARTICLES = json.load(f)

# 加载解读知识库（王灿发教授解读 + 书籍指引）
COMMENTARY_PATH = os.path.join(SCRIPT_DIR, "..", "data", "commentary.json")
with open(COMMENTARY_PATH, "r", encoding="utf-8") as f:
    COMMENTARY = json.load(f)

# 构建编号索引
ARTICLE_INDEX = {a["article_number"]: a for a in ARTICLES}

# 法典施行后废止的10部法律
ABOLISHED_LAWS = [
    "中华人民共和国环境保护法",
    "中华人民共和国环境影响评价法",
    "中华人民共和国海洋环境保护法",
    "中华人民共和国大气污染防治法",
    "中华人民共和国水污染防治法",
    "中华人民共和国土壤污染防治法",
    "中华人民共和国固体废物污染环境防治法",
    "中华人民共和国噪声污染防治法",
    "中华人民共和国放射性污染防治法",
    "中华人民共和国清洁生产促进法",
]

# 热点条款清单
HOTSPOT_ARTICLES = {
    "全国生态日": 15,
    "基本原则": 6,
    "统一监督管理": 17,
    "生态环境保护督察": 28,
    "生态环境损害赔偿": 32,
    "行刑衔接": 33,
    "河湖长制林长制": 19,
    "现场检查": 51,
    "查封扣押": 52,
    "派出机构执法": 53,
    "生态环境信用监管": 54,
    "排污许可管理": 68 if 68 in ARTICLE_INDEX else None,
    "监测数据弄虚作假禁止": 80,
    "环评分类管理": 95,
    "环评不予批准情形": 105,
    "生态保护补偿": 111,
    "双罚制（法律责任通则）": None,  # 动态查找
    "按日连续处罚": None,
    "限产停产": None,
    "责令停产关闭": None,
    "行政拘留": None,
    "刑事责任": None,
}


def search_articles(keyword):
    """关键词检索法典条款"""
    results = []
    for a in ARTICLES:
        if keyword in a["text"]:
            results.append(a)
    
    if not results:
        print(f"未找到包含 \"{keyword}\" 的条款。")
        return
    
    print(f"找到 {len(results)} 条包含 \"{keyword}\" 的条款：\n")
    for a in results[:20]:  # 最多返回20条
        print(f"【{a['article_number_cn']}】 [{a['bian']}] [{a['chapter']}]")
        # 显示匹配关键词附近的内容
        text = a["text"]
        idx = text.find(keyword)
        start = max(0, idx - 30)
        end = min(len(text), idx + len(keyword) + 100)
        snippet = text[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."
        print(f"  {snippet}")
        print()
    
    if len(results) > 20:
        print(f"... 还有 {len(results) - 20} 条结果未显示，请缩小搜索范围。")


def get_article(number):
    """按条款编号查询"""
    if number not in ARTICLE_INDEX:
        print(f"未找到第{number}条。法典共有{len(ARTICLES)}条条款（含附则引用条款）。")
        return
    
    a = ARTICLE_INDEX[number]
    print(f"【{a['article_number_cn']}】")
    print(f"所属：{a['bian']}")
    if a.get("fenbian"):
        print(f"分编：{a['fenbian']}")
    if a.get("chapter"):
        print(f"章节：{a['chapter']}")
    if a.get("section"):
        print(f"节：{a['section']}")
    print()
    print(a["text"])


def show_structure():
    """输出法典五编章节结构概览"""
    print("=" * 60)
    print("《中华人民共和国生态环境法典》结构概览")
    print("（2026年3月12日通过，2026年8月15日施行）")
    print("共5编1242条，整合30多部单行法")
    print("=" * 60)
    print()
    
    bian_map = {}
    for a in ARTICLES:
        bian = a["bian"]
        if bian not in bian_map:
            bian_map[bian] = {"articles": [], "chapters": set(), "sections": set()}
        bian_map[bian]["articles"].append(a)
        if a.get("chapter"):
            bian_map[bian]["chapters"].add(a["chapter"])
        if a.get("section"):
            bian_map[bian]["sections"].add(a["section"])
    
    for bian, info in bian_map.items():
        print(f"{bian}（共{len(info['articles'])}条）")
        for ch in sorted(info["chapters"]):
            print(f"  {ch}")
            # 显示该章下的节
            ch_articles = [a for a in info["articles"] if a.get("chapter") == ch]
            ch_sections = set()
            for a in ch_articles:
                if a.get("section"):
                    ch_sections.add(a["section"])
            for sec in sorted(ch_sections):
                print(f"    {sec}")
        if info["sections"]:
            pass  # 已在章节下显示
        print()


def search_by_bian(bian_name):
    """按编查询"""
    bian_name = bian_name.strip()
    results = [a for a in ARTICLES if bian_name in a["bian"]]
    
    if not results:
        print(f"未找到包含 \"{bian_name}\" 的编。")
        print("可用选项：总则、污染防治、生态保护、绿色低碳发展、法律责任和附则")
        return
    
    print(f"{results[0]['bian']}（共{len(results)}条）\n")
    
    # 列出所有章节
    chapters = []
    for a in results:
        ch = a.get("chapter", "")
        if ch and ch not in chapters:
            chapters.append(ch)
    
    print("章节列表：")
    for ch in chapters:
        ch_arts = [a for a in results if a.get("chapter") == ch]
        start_num = ch_arts[0]["article_number"] if ch_arts else "?"
        end_num = ch_arts[-1]["article_number"] if ch_arts else "?"
        print(f"  {ch}（第{start_num}条-第{end_num}条，共{len(ch_arts)}条）")
    
    print(f"\n前3条预览：")
    for a in results[:3]:
        print(f"  【{a['article_number_cn']}】 {a['text'][:80]}...")


def search_by_chapter(keyword):
    """按章节关键词查询"""
    keyword = keyword.strip()
    results = []
    seen_chapters = set()
    
    for a in ARTICLES:
        ch = a.get("chapter", "") + " " + a.get("section", "") + " " + a.get("fenbian", "")
        if keyword in ch:
            if a.get("chapter") not in seen_chapters:
                seen_chapters.add(a.get("chapter"))
                ch_arts = [x for x in ARTICLES if x.get("chapter") == a.get("chapter")]
                results.append({
                    "chapter": a.get("chapter"),
                    "bian": a["bian"],
                    "fenbian": a.get("fenbian", ""),
                    "count": len(ch_arts),
                    "start": ch_arts[0]["article_number"] if ch_arts else 0,
                    "end": ch_arts[-1]["article_number"] if ch_arts else 0,
                    "articles": ch_arts[:3],  # 预览前3条
                })
    
    if not results:
        print(f"未找到包含 \"{keyword}\" 的章节。")
        return
    
    for r in results:
        print(f"【{r['chapter']}】")
        print(f"  所属：{r['bian']}" + (f" / {r['fenbian']}" if r['fenbian'] else ""))
        print(f"  条款范围：第{r['start']}条-第{r['end']}条，共{r['count']}条")
        print(f"  前3条预览：")
        for a in r["articles"]:
            print(f"    【{a['article_number_cn']}】 {a['text'][:60]}...")
        print()


def compliance_check(industry):
    """企业合规预检：根据行业类型输出合规检查清单"""
    industry = industry.strip()
    
    # 通用合规检查清单（所有行业适用）
    general_checks = [
        {"topic": "排污许可管理", "articles": [174, 175, 176, 178, 179, 180, 182, 183], "desc": "企业必须依法取得排污许可证，按证排污"},
        {"topic": "生态环境影响评价", "articles": [95, 96, 102, 105, 107], "desc": "建设项目必须依法进行环评，未批先建违法"},
        {"topic": "监测数据真实性", "articles": [78, 80], "desc": "企业对监测数据真实性负责，弄虚作假将受处罚"},
        {"topic": "突发生态环境事件应对", "articles": [117, 123], "desc": "企业须制定应急预案，发生事件须及时报告"},
        {"topic": "信息公开与公众参与", "articles": [137, 140, 145], "desc": "企业须依法公开环境信息，接受公众监督"},
        {"topic": "生态环境信用", "articles": [54], "desc": "违法信息记入信用记录，影响企业信用"},
        {"topic": "双罚制风险", "articles": [1064], "desc": "违法将同时处罚企业 和 法定代表人/直接责任人个人"},
        {"topic": "生态损害赔偿", "articles": [32], "desc": "造成生态环境损害须承担赔偿责任"},
    ]
    
    # 行业特定合规检查
    industry_checks = {
        "化工": [
            {"topic": "大气污染防治", "articles": [], "desc": "工业废气排放须达标，VOCs管控要求"},
            {"topic": "水污染防治", "articles": [], "desc": "工业废水排放须达标，禁止稀释排放有毒有害工业废水"},
            {"topic": "固废污染防治", "articles": [], "desc": "危险废物须依法处置，固废零进口"},
            {"topic": "化学物质风险管控", "articles": [], "desc": "新化学物质须登记，危险化学品须管控"},
            {"topic": "土壤污染防治", "articles": [], "desc": "建设用地土壤污染风险管控和修复"},
        ],
        "制药": [
            {"topic": "水污染防治", "articles": [], "desc": "制药废水处理须达标排放"},
            {"topic": "大气污染防治", "articles": [], "desc": "发酵尾气、VOCs排放管控"},
            {"topic": "固废污染防治", "articles": [], "desc": "制药废渣、危险废物处置"},
            {"topic": "化学物质风险管控", "articles": [], "desc": "原料药生产化学物质管控"},
        ],
        "电力": [
            {"topic": "大气污染防治", "articles": [], "desc": "燃煤电厂超低排放，脱硫脱硝除尘"},
            {"topic": "固废污染防治", "articles": [], "desc": "粉煤灰、脱硫石膏综合利用"},
            {"topic": "碳排放管理", "articles": [], "desc": "碳排放权交易、碳达峰碳中和义务"},
            {"topic": "放射性污染防治", "articles": [], "desc": "核电厂放射性废物管理"},
        ],
        "矿业": [
            {"topic": "生态保护", "articles": [], "desc": "矿产资源开发须保护生态，矿山生态修复义务"},
            {"topic": "土壤污染防治", "articles": [], "desc": "矿区土壤污染风险管控"},
            {"topic": "水污染防治", "articles": [], "desc": "矿坑水处理达标排放"},
            {"topic": "固废污染防治", "articles": [], "desc": "尾矿库安全管理"},
        ],
        "制造": [
            {"topic": "大气污染防治", "articles": [], "desc": "工业废气、焊接烟尘等排放管控"},
            {"topic": "水污染防治", "articles": [], "desc": "工业废水预处理和达标排放"},
            {"topic": "噪声污染防治", "articles": [], "desc": "工业噪声排放达标"},
            {"topic": "固废污染防治", "articles": [], "desc": "一般工业固废和危险废物分类管理"},
        ],
        "农业": [
            {"topic": "水污染防治", "articles": [], "desc": "农业面源污染防治，化肥农药减量"},
            {"topic": "土壤污染防治", "articles": [], "desc": "农用地土壤污染风险管控"},
            {"topic": "固废污染防治", "articles": [], "desc": "农业固体废物、畜禽粪污资源化利用"},
        ],
    }
    
    specific = industry_checks.get(industry, [])
    
    print("=" * 60)
    print(f"企业环保合规预检报告")
    print(f"行业类型：{industry}")
    print(f"依据：《中华人民共和国生态环境法典》（2026年8月15日施行）")
    print("=" * 60)
    print()
    print("【AI辅助参考，最终以法典原文为准】")
    print()
    
    print("一、通用合规检查清单（所有行业适用）")
    print("-" * 40)
    for i, check in enumerate(general_checks, 1):
        print(f"{i}. {check['topic']}")
        print(f"   说明：{check['desc']}")
        if check["articles"]:
            art_refs = "、".join([f"第{n}条" for n in check["articles"] if n in ARTICLE_INDEX])
            if art_refs:
                print(f"   法典依据：{art_refs}")
        print()
    
    if specific:
        print(f"二、{industry}行业专项合规检查")
        print("-" * 40)
        for i, check in enumerate(specific, 1):
            print(f"{i}. {check['topic']}")
            print(f"   说明：{check['desc']}")
            print()
    
    print("三、双罚制特别提醒")
    print("-" * 40)
    print("法典实施\"双罚制\"——不仅处罚企业，同时处罚法定代表人和直接责任人个人。")
    print("企业法定代表人和直接责任人须特别注意以下高风险事项：")
    print("  - 环评文件弄虚作假：对建设单位处50万-200万罚款，同时对个人处个人罚款")
    print("  - 监测数据弄虚作假：企业及负责人承担法律责任")
    print("  - 无证排污/超证排污：处罚企业并处罚责任人")
    print("  - 非法排放危险废物：可能触发刑事责任")
    print()
    print("建议：企业应定期开展环保合规自查，建立污染防治制度，")
    print("      确保监测数据真实准确，及时整改合规风险。")
    print()
    print("如需查询具体条款内容，可使用：python3 scripts/query.py article <条款编号>")


def show_abolished():
    """查询法典施行后废止的法律清单"""
    print("=" * 60)
    print("法典施行后废止的法律清单")
    print("=" * 60)
    print()
    print("根据《生态环境法典》第一千二百四十二条规定：")
    print("本法自2026年8月15日起施行，以下10部法律同时废止：")
    print()
    
    # 尝试从最后一条中提取废止法律原文
    last_article = ARTICLES[-1]
    print(f"【法典原文】{last_article['article_number_cn']}")
    print(last_article["text"])
    print()
    
    print("【废止法律清单】")
    for i, law in enumerate(ABOLISHED_LAWS, 1):
        print(f"  {i}. {law}")
    
    print()
    print("说明：法典施行后，以上10部法律的全部内容被整合进法典5编1242条中。")
    print("      原适用上述法律的执法活动，自2026年8月15日起统一适用法典规定。")


def show_hotspot():
    """输出法典核心热点条款"""
    print("=" * 60)
    print("法典核心热点条款")
    print("=" * 60)
    print()
    
    # 动态查找法律责任编中的双罚制等条款
    penalty_articles = [a for a in ARTICLES if "法律责任" in a.get("bian", "")]
    
    hotspot_items = [
        ("全国生态日", 15, "每年8月15日为全国生态日"),
        ("六项基本原则", 6, "预防为主、系统治理、生态优先、绿色发展、公众参与、损害担责"),
        ("统一监督管理", 17, "生态环境部对全国生态环境保护工作实施统一监督管理"),
        ("生态环境保护督察", 28, "中央和省两级督察体制"),
        ("生态环境损害赔偿", 32, "完善生态环境损害赔偿和生态环境公益诉讼制度"),
        ("行刑衔接", 33, "行政机关、监察机关、审判机关和检察机关协同配合"),
        ("现场检查权", 51, "监管部门有权对企业进行现场检查"),
        ("查封扣押权", 52, "监管部门可依法查封扣押有关场所、设施、设备"),
        ("派出机构执法", 53, "市级生态环境主管部门派出机构可独立实施行政处罚"),
        ("生态环境信用", 54, "企业违法信息记入信用记录"),
        ("监测数据禁止弄虚作假", 80, "禁止篡改、伪造监测数据"),
        ("环评分类管理", 95, "建设项目环评分报告书、报告表、登记表三级管理"),
        ("环评不予批准情形", 105, "五种情形下环评不予批准"),
        ("生态保护补偿制度", 111, "财政纵向+地区横向+市场机制三类补偿"),
        ("双罚制总则", 1064, "企业及法定代表人、直接责任人员均承担法律责任"),
        ("按日连续处罚", 1060, "拒绝、阻挠复查的，按原罚款数额按日连续处罚"),
    ]
    
    for title, num, desc in hotspot_items:
        if num in ARTICLE_INDEX:
            a = ARTICLE_INDEX[num]
            print(f"【{title}】 {a['article_number_cn']} [{a['bian']}]")
            print(f"  {desc}")
            print(f"  {a['text'][:120]}...")
            print()
        else:
            print(f"【{title}】 第{num}条")
            print(f"  {desc}")
            print()
    
    # 查找双罚制相关条款
    print("【双罚制相关条款（法律责任编）】")
    dual_penalty = [a for a in penalty_articles if "直接负责" in a["text"] or "主管人员" in a["text"] or "直接责任" in a["text"]]
    if dual_penalty:
        print(f"  找到{len(dual_penalty)}条涉及双罚制的条款，前5条：")
        for a in dual_penalty[:5]:
            print(f"  【{a['article_number_cn']}】 [{a.get('chapter', '')}]")
            print(f"    {a['text'][:100]}...")
            print()
    
    # 查找按日连续处罚
    daily = [a for a in ARTICLES if "按日" in a["text"] and "处罚" in a["text"]]
    if daily:
        print(f"【按日连续处罚条款】共{len(daily)}条：")
        for a in daily[:3]:
            print(f"  【{a['article_number_cn']}】 {a['text'][:100]}...")
        print()
    
    # 查找责令停产/关闭
    shutdown = [a for a in ARTICLES if "停产" in a["text"] or "责令关闭" in a["text"]]
    if shutdown:
        print(f"【责令停产/关闭条款】共{len(shutdown)}条")
        for a in shutdown[:3]:
            print(f"  【{a['article_number_cn']}】 {a['text'][:100]}...")
        print()


def query_subject(subject_name):
    """按主体视角查询法典权责义务"""
    subject_name = subject_name.strip()
    subjects = COMMENTARY.get("subjects", [])

    matched = None
    for s in subjects:
        if subject_name in s["name"] or s["id"] == subject_name:
            matched = s
            break

    if not matched:
        print(f"未找到主体 \"{subject_name}\"。")
        print("可用主体：")
        for s in subjects:
            print(f"  {s['name']}（{s['description'][:30]}...）")
        return

    print("=" * 60)
    print(f"主体视角：{matched['name']}")
    print(f"说明：{matched['description']}")
    print("=" * 60)
    print()

    if matched.get("key_functions"):
        print("【主要职能】")
        for fn in matched["key_functions"]:
            print(f"  - {fn}")
        print()

    if matched.get("rights"):
        print("【权利】")
        for r in matched["rights"]:
            print(f"  - {r}")
        print()

    if matched.get("obligations"):
        print("【义务】")
        for ob in matched["obligations"]:
            print(f"  - {ob}")
        print()

    if matched.get("responsibilities"):
        print("【违法责任】")
        for resp in matched["responsibilities"]:
            print(f"  - {resp}")
        print()

    if matched.get("key_articles"):
        print("【关联法典条款】")
        for num in matched["key_articles"]:
            if num in ARTICLE_INDEX:
                a = ARTICLE_INDEX[num]
                print(f"  【{a['article_number_cn']}】 [{a['bian']}] {a['text'][:80]}...")
            else:
                print(f"  第{num}条（未在知识库中找到）")
        print()

    print("如需查看具体条款全文，可使用：python3 scripts/query.py article <条款编号>")


def query_commentary(topic):
    """查询王灿发教授法典解读"""
    topic = topic.strip()
    commentaries = COMMENTARY.get("expert_commentary", [])

    if topic == "list" or topic == "全部":
        print("=" * 60)
        print("王灿发教授法典解读目录")
        print("=" * 60)
        print()
        for c in commentaries:
            print(f"  [{c['id']}] {c['title']}")
            print(f"    来源：{c.get('source', 'N/A')}")
            print()
        print(f"共{len(commentaries)}篇解读。")
        print("使用方式：python3 scripts/query.py commentary <id或关键词>")
        return

    matched = None
    for c in commentaries:
        if c["id"] == topic or topic in c["title"] or topic in c.get("id", ""):
            matched = c
            break

    if not matched:
        candidates = [c for c in commentaries if topic in c["title"] or topic in json.dumps(c.get("key_points", []), ensure_ascii=False)]
        if candidates:
            matched = candidates[0]
        else:
            print(f"未找到与 \"{topic}\" 相关的解读。")
            print("使用 'list' 查看全部解读目录：python3 scripts/query.py commentary list")
            return

    print("=" * 60)
    print(f"【法典解读】{matched['title']}")
    print(f"解读人：{matched.get('author', 'N/A')}（{matched.get('author_title', 'N/A')}）")
    print(f"来源：{matched.get('source', 'N/A')}")
    if matched.get("source_url"):
        print(f"原文链接：{matched['source_url']}")
    if matched.get("legal_basis"):
        print(f"法律依据：{matched.get('legal_basis')}")
    print("=" * 60)
    print()

    if matched.get("key_points"):
        print("【核心要点】")
        for i, point in enumerate(matched["key_points"], 1):
            print(f"  {i}. {point}")
        print()

    if matched.get("sub_functions"):
        print("【子职能详解】")
        for sf in matched["sub_functions"]:
            print(f"  [{sf['name']}] —— {sf['role']}")
            print(f"    内涵：{sf['connotation']}")
            print(f"    核心内容：")
            for cc in sf["core_content"]:
                print(f"      - {cc}")
            print()

    if matched.get("related_articles"):
        print("【关联法典条款】")
        for num in matched["related_articles"]:
            if num in ARTICLE_INDEX:
                a = ARTICLE_INDEX[num]
                print(f"  【{a['article_number_cn']}】 [{a['bian']}] {a['text'][:80]}...")
        print()

    if matched.get("related_bian"):
        print(f"【关联编章】{matched['related_bian']}")
        print()

    print("如需查看具体条款全文，可使用：python3 scripts/query.py article <条款编号>")


def show_book_info():
    """显示书籍信息"""
    book = COMMENTARY.get("book_info", {})
    print("=" * 60)
    print(f"《{book.get('title', 'N/A')}》")
    print("=" * 60)
    print()
    print(f"  主编：{book.get('editor', 'N/A')}")
    print(f"  出版社：{book.get('publisher', 'N/A')}")
    print(f"  出版时间：{book.get('publish_date', 'N/A')}")
    print(f"  页数/开本：{book.get('pages', 'N/A')}")
    print(f"  ISBN：{book.get('isbn', 'N/A')}")
    print(f"  定价：{book.get('price', 'N/A')}")
    print()
    print(f"  内容简介：{book.get('description', 'N/A')}")
    print()
    print(f"  核心价值：{book.get('core_value', 'N/A')}")
    print()
    if book.get("applicable_audiences"):
        print("  适用读者：")
        for aud in book["applicable_audiences"]:
            print(f"    - {aud}")
    print()
    if book.get("book_launch"):
        launch = book["book_launch"]
        print("  新书交流活动：")
        print(f"    时间：{launch.get('date', 'N/A')}")
        print(f"    地点：{launch.get('venue', 'N/A')}")
        print(f"    活动：{launch.get('event', 'N/A')}")
        print(f"    出席嘉宾：")
        for guest in launch.get("attendees", []):
            print(f"      - {guest}")
        print(f"    共识：{launch.get('consensus', 'N/A')[:80]}...")
    print()
    if COMMENTARY.get("expert_profile"):
        profile = COMMENTARY["expert_profile"]
        print("  主编简介：")
        print(f"    姓名：{profile.get('name', 'N/A')}")
        print(f"    职称：{profile.get('title', 'N/A')}")
        print(f"    兼职：")
        for pos in profile.get("positions", []):
            print(f"      - {pos}")
        print(f"    立法参与：{profile.get('legislative_participation', 'N/A')}")
        print(f"    法典编纂贡献：")
        for item in profile.get("codification_contribution", []):
            print(f"      - {item}")


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/query.py <action> [params]")
        print()
        print("支持的 action：")
        print("  search <keyword>       关键词检索法典条款")
        print("  article <number>       按条款编号查询")
        print("  structure              输出法典五编章节结构概览")
        print("  bian <name>            按编查询（如：总则、污染防治）")
        print("  chapter <keyword>      按章节关键词查询")
        print("  compliance <industry>  企业合规预检（如：化工、制药、电力）")
        print("  abolished              查询法典施行后废止的10部法律")
        print("  hotspot                输出法典核心热点条款")
        print("  subject <name>         按主体视角查询权责义务（国家/政府/部门/企事业单位/社会组织/个人）")
        print("  commentary <id|keyword>  查询王灿发教授法典解读（list查看目录）")
        print("  book                   显示《主体责任及权利义务全指引》书籍信息")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "search":
        if len(sys.argv) < 3:
            print("用法: python3 scripts/query.py search <keyword>")
            sys.exit(1)
        search_articles(sys.argv[2])
    
    elif action == "article":
        if len(sys.argv) < 3:
            print("用法: python3 scripts/query.py article <number>")
            sys.exit(1)
        try:
            num = int(sys.argv[2])
            get_article(num)
        except ValueError:
            print(f"条款编号必须是数字，收到：{sys.argv[2]}")
            sys.exit(1)
    
    elif action == "structure":
        show_structure()
    
    elif action == "bian":
        if len(sys.argv) < 3:
            print("用法: python3 scripts/query.py bian <name>")
            print("可用：总则、污染防治、生态保护、绿色低碳发展、法律责任和附则")
            sys.exit(1)
        search_by_bian(sys.argv[2])
    
    elif action == "chapter":
        if len(sys.argv) < 3:
            print("用法: python3 scripts/query.py chapter <keyword>")
            sys.exit(1)
        search_by_chapter(sys.argv[2])
    
    elif action == "compliance":
        if len(sys.argv) < 3:
            print("用法: python3 scripts/query.py compliance <industry>")
            print("可用：化工、制药、电力、矿业、制造、农业")
            sys.exit(1)
        compliance_check(sys.argv[2])
    
    elif action == "abolished":
        show_abolished()
    
    elif action == "hotspot":
        show_hotspot()
    
    elif action == "subject":
        if len(sys.argv) < 3:
            print("用法: python3 scripts/query.py subject <name>")
            print("可用主体：国家、政府、部门、企事业单位、社会组织、个人")
            sys.exit(1)
        query_subject(sys.argv[2])
    
    elif action == "commentary":
        if len(sys.argv) < 3:
            print("用法: python3 scripts/query.py commentary <id|keyword>")
            print("使用 'list' 查看全部解读目录")
            sys.exit(1)
        query_commentary(sys.argv[2])
    
    elif action == "book":
        show_book_info()
    
    else:
        print(f"未知的 action: {action}")
        print("支持的 action: search, article, structure, bian, chapter, compliance, abolished, hotspot, subject, commentary, book")
        sys.exit(1)


if __name__ == "__main__":
    main()
