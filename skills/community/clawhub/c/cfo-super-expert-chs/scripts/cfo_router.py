#!/usr/bin/env python3
"""CFO Super Expert - Intelligent Router
Author: WANG DONG JIE (@yjkj999999)
"""
import sys, os

SKILLS_BASE = os.environ.get("SKILLS_BASE", "/data/user/skills")

SKILLS_REGISTRY = {
    "stock-master-hunter": {"name":"AI Stock Master (Stock Master Hunter)","domain":"Investment Analysis","keywords":["stock analysis","stock diagnosis","master model","Buffett","Lynch","Graham","sector ranking","hot money","market sentiment","dragon tiger","limit up","quant screening","stock picks","trend","leader","greed","fear","bull bear","股票分析","个股诊断","大师模型","巴菲特","林奇","格雷厄姆","行业排行","游资","大盘情绪","龙虎榜","涨停","连板","量化选股"],"description":"5 master model diagnostics, industry momentum, hot money monitoring, sentiment analysis, quant screening"},
    "cgma-finance": {"name":"CGMA Financial Management","domain":"Financial Management","keywords":["financial management","CGMA","management accounting","financial system","financial transformation","财务管理","CGMA","管理会计","财务体系"],"description":"Build/restructure financial management system based on CGMA principles"},
    "financial-statement-reading": {"name":"Financial Statement Reading","domain":"Financial Management","keywords":["financial statements","accounting estimates","ratio analysis","cash flow","balance sheet","income statement","财报","财务报表","会计估计","比率分析","现金流"],"description":"Systematic analysis of financial statement structure and cash flow"},
    "cas-china-mastery": {"name":"CAS China Mastery","domain":"Financial Management","keywords":["accounting standards","CAS","revenue recognition","lease","financial instruments","business combination","会计准则","CAS","收入确认","租赁"],"description":"China 1 basic + 40 specific accounting standards full coverage"},
    "cpa-china-2026-pro": {"name":"CPA China 2026 Pro","domain":"Financial Management","keywords":["CPA","certified accountant","audit","tax","financial management","six subjects","CPA","注册会计师","审计","税法","六科"],"description":"2026 CPA six-subject comprehensive coverage"},
    "cpa-china-2026": {"name":"CPA China 2026","domain":"Financial Management","keywords":["CPA","certified accountant","professional stage","standards interpretation","CPA","注册会计师","专业阶段","准则解读"],"description":"CPA six-subject knowledge Q&A and standards interpretation"},
    "cgma-global-management-accountant": {"name":"CGMA Global Management Accountant","domain":"Financial Management","keywords":["CGMA","management accounting","AICPA","CIMA","global management accounting","CGMA","管理会计","AICPA","CIMA"],"description":"AICPA & CIMA global management accounting principles"},
    "wangdongjie-cfo-skill": {"name":"Wang Dongjie CFO Expert","domain":"Capital Operations","keywords":["IPO","capital operations","capital leverage","business finance integration","digital risk control","A+H","listing","CFO","IPO","资本运作","资本杠杆","业财融合","数字化风控"],"description":"A+H dual-market IPO execution and capital leverage design"},
    "valuation-mastery": {"name":"Valuation Mastery","domain":"Capital Operations","keywords":["valuation","DCF","comparable","replacement cost","real options","SOTP","enterprise value","EV","估值","DCF","可比公司","重置成本","实物期权"],"description":"Full valuation methodology: DCF/comparable/replacement/real options"},
    "ms-financial-model": {"name":"MS Financial Model","domain":"Capital Operations","keywords":["financial model","Excel","DCF model","SOTP","sensitivity analysis","PE Band","Morgan Stanley","财务模型","Excel","DCF模型","敏感性分析","摩根士丹利"],"description":"Morgan Stanley style DCF/SOTP investment-grade Excel model"},
    "ms-investment-deck": {"name":"MS Investment Deck","domain":"Capital Operations","keywords":["investment deck","roadshow","PPT","Pitch Book","investment committee","Morgan Stanley","投资演示","路演","PPT","Pitch Book","摩根士丹利"],"description":"Morgan Stanley style roadshow PPT / Pitch Book generation"},
    "ms-research-report": {"name":"MS Research Report","domain":"Investment Analysis","keywords":["research report","industry report","initiation","sell-side research","buy-side memo","earnings review","Morgan Stanley","研究报告","行业报告","首次覆盖","卖方研究","摩根士丹利"],"description":"Morgan Stanley style equity research report Word generation"},
    "dongmi": {"name":"Board Secretary Expert","domain":"Governance & Compliance","keywords":["board secretary","disclosure","investor relations","corporate governance","capital operations","董秘","信息披露","投资者关系","公司治理"],"description":"Listed company board secretary four core functions"},
    "sse-listed-company-mastery": {"name":"SSE Listed Company Mastery","domain":"Governance & Compliance","keywords":["SSE","listing rules","disclosure","Shanghai Stock Exchange","listed company","上交所","上市规则","信披","沪市"],"description":"Shanghai Stock Exchange listed company rules and operations"},
    "legal-risk-shield": {"name":"Legal Risk Shield","domain":"Governance & Compliance","keywords":["legal risk","compliance","contract","equity","company formation","financing","exit","法律风险","合规","合同","股权","公司设立"],"description":"Full corporate lifecycle legal risk prevention"},
    "sasac-performance-analyst": {"name":"SASAC Performance Analyst","domain":"Governance & Compliance","keywords":["SASAC","performance evaluation","SOE","state-owned","国资委","绩效评价","央企","国企"],"description":"SASAC enterprise performance evaluation analysis"},
    "internal-audit-mastery": {"name":"Internal Audit Mastery","domain":"Audit & Risk","keywords":["internal audit","IIA","audit standards","audit workflow","internal control","内部审计","IIA","内审","审计准则","内控"],"description":"IIA global standards + China practical cases"},
    "fraud-examination-mastery": {"name":"Fraud Examination Mastery","domain":"Audit & Risk","keywords":["fraud","anti-fraud","ACFE","fraud investigation","financial fraud","舞弊","反舞弊","ACFE","舞弊调查","财务造假"],"description":"ACFE fraud examination: identification/investigation/prosecution"},
    "gceo-global-ceo-skill-system": {"name":"Global CEO Mastery","domain":"Strategy","keywords":["CEO","strategy","leadership","mastery","executive","decision","vision","CEO","战略","领导力","帝王学","高管","决策"],"description":"CEO-level strategy/finance/leadership framework"},
    "super-advisor-investment-banking": {"name":"Super Advisor Investment Banking","domain":"Strategy","keywords":["investment banking","advisory","M&A","restructuring","consulting","framework","best practices","投行","咨询","并购","重组","M&A"],"description":"Top consulting frameworks + IB best practices"},
    "mckinsey-100y-knowledge-base": {"name":"McKinsey 100-Year Knowledge Base","domain":"Strategy","keywords":["McKinsey","pyramid principle","structured thinking","strategic thinking","industry insight","麦肯锡","金字塔原理","结构化思维","战略思维"],"description":"191 curated articles, pyramid principle / structured thinking"},
    "super-middle-manager-academy": {"name":"Super Middle Manager Academy","domain":"Strategy","keywords":["middle management","team management","work management","strategy management","中层管理","团队管理","工作管理","管理能力"],"description":"Middle manager capability building"},
    "midea-management": {"name":"Midea Management Practice","domain":"Strategy","keywords":["Midea","management practice","operations","R&D","human resources","美的","管理实践","运营","研发","人力资源"],"description":"Midea Group integrated management practices"},
    "dbs-danaher-business-system": {"name":"DBS Danaher Business System","domain":"Strategy","keywords":["Danaher","DBS","lean","kaizen","business system","丹纳赫","DBS","精益","改善"],"description":"Danaher Business System core skill framework"},
    "ms-ppt-style": {"name":"MS-PPT-Style","domain":"Presentation Output","keywords":["PPT","presentation","roadshow","Morgan Stanley","bilingual","gradient","chart","PPT","演示文稿","路演","摩根士丹利","双语"],"description":"Morgan Stanley classic PPT style generator"},
    "dfp-skill": {"name":"Digital Finance Presentation","domain":"Presentation Output","keywords":["SAP","digital finance","ultra-wide","presentation","AI-powered","SAP","数字财务","超宽屏","演示"],"description":"SAP enterprise ultra-wide presentation generator"},
}

SCENARIOS = {
    "Investment Decision": ["stock-master-hunter", "valuation-mastery", "ms-financial-model"],
    "IPO Full Process": ["wangdongjie-cfo-skill", "valuation-mastery", "ms-financial-model", "ms-investment-deck", "dongmi", "sse-listed-company-mastery"],
    "M&A Restructuring": ["super-advisor-investment-banking", "valuation-mastery", "ms-financial-model", "legal-risk-shield"],
    "Annual Report Analysis": ["financial-statement-reading", "stock-master-hunter", "ms-research-report"],
    "Internal Control System": ["internal-audit-mastery", "fraud-examination-mastery", "legal-risk-shield"],
    "Digital Transformation": ["cgma-finance", "dfp-skill", "dbs-danaher-business-system", "midea-management"],
    "CEO Strategic Decision": ["gceo-global-ceo-skill-system", "mckinsey-100y-knowledge-base", "super-advisor-investment-banking"],
    "SOE Performance Improvement": ["sasac-performance-analyst", "cgma-finance", "internal-audit-mastery"],
}

def list_skills():
    print("="*70)
    print(f"CFO Super Expert - Sub-Skills List ({len(SKILLS_REGISTRY)} total)")
    print("="*70)
    domains = {}
    for slug, info in SKILLS_REGISTRY.items():
        domains.setdefault(info["domain"], []).append((slug, info))
    for domain, skills in domains.items():
        print(f"\n[{domain}]")
        for slug, info in skills:
            ok = "OK" if os.path.isfile(f"{SKILLS_BASE}/{slug}/SKILL.md") else "--"
            print(f"  [{ok}] {slug}: {info['name']}")

def search_skills(query):
    q = query.lower()
    matches = []
    for slug, info in SKILLS_REGISTRY.items():
        score = sum(2 for kw in info["keywords"] if kw.lower() in q or q in kw.lower())
        if slug.lower() in q: score += 3
        if info["name"].lower() in q: score += 3
        if score > 0: matches.append((score, slug, info))
    scenario_hits = [s for s, skills in SCENARIOS.items() if any(m[1] in skills for m in matches)]
    if not matches:
        print(f"No sub-skills matching '{query}'"); return
    matches.sort(key=lambda x: x[0], reverse=True)
    print(f"\nSearch results for '{query}':")
    print("="*60)
    for score, slug, info in matches:
        ok = "OK" if os.path.isfile(f"{SKILLS_BASE}/{slug}/SKILL.md") else "--"
        print(f"\n  [{ok}] {slug} (match:{'*'*min(score,5)})")
        print(f"       Domain: {info['domain']} | Name: {info['name']}")
        print(f"       {info['description']}")
    if scenario_hits:
        print(f"\n  Recommended scenarios: {', '.join(set(scenario_hits))}")

def show_info(slug):
    if slug not in SKILLS_REGISTRY:
        print(f"Not found: {slug}\nAvailable: {', '.join(SKILLS_REGISTRY.keys())}"); return
    info = SKILLS_REGISTRY[slug]
    ok = "Installed" if os.path.isfile(f"{SKILLS_BASE}/{slug}/SKILL.md") else "Not installed"
    print(f"\n{'='*60}\nSub-Skill: {slug}\n{'='*60}")
    print(f"  Name: {info['name']}\n  Domain: {info['domain']}")
    print(f"  Description: {info['description']}")
    print(f"  Keywords: {', '.join(info['keywords'][:8])}")
    print(f"  Status: {ok}")

def show_scenarios():
    print("\nCFO Super Expert - Collaboration Scenarios")
    print("="*60)
    for s, skills in SCENARIOS.items():
        print(f"\n  {s}")
        for sk in skills:
            n = SKILLS_REGISTRY.get(sk, {}).get("name", sk)
            print(f"    -> {sk}: {n}")

def show_stats():
    total = len(SKILLS_REGISTRY)
    installed = sum(1 for s in SKILLS_REGISTRY if os.path.isfile(f"{SKILLS_BASE}/{s}/SKILL.md"))
    domains = len(set(i["domain"] for i in SKILLS_REGISTRY.values()))
    print(f"\nCFO Super Expert Statistics\n{'='*40}")
    print(f"  Total skills: {total} | Installed: {installed} | Domains: {domains} | Scenarios: {len(SCENARIOS)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 cfo_router.py [list|search|info|scenarios|stats]"); sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "list": list_skills()
    elif cmd == "search": search_skills(" ".join(sys.argv[2:])) if len(sys.argv)>2 else print("Please provide a keyword")
    elif cmd == "info": show_info(sys.argv[2]) if len(sys.argv)>2 else print("Please provide a skill name")
    elif cmd == "scenarios": show_scenarios()
    elif cmd == "stats": show_stats()
    else: print(f"Unknown command: {cmd}")
