#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌍 全球地缘政治博弈冲突分析引擎 v1.0
Global Geopolitical Conflict Analysis Engine

用于所有52国方案中的地缘政治评估。
For geopolitical risk assessment in all 52-country trading plans.

⚠️ 本引擎基于公开新闻信息进行分析，不构成投资建议。
This engine analyzes based on public news. Not investment advice.
"""

import json
import os
from datetime import datetime

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, "market_config.json")

# ============================================================
# 全球冲突热点数据库 / Global Conflict Hotspots Database
# ============================================================
CONFLICT_DATABASE = {
    "中东": {
        "name_cn": "中东冲突",
        "name_en": "Middle East Conflict",
        "key_hotspots": {
            "伊朗-以色列": {
                "cn": "伊朗与以色列对抗，霍尔木兹海峡封锁风险",
                "en": "Iran-Israel confrontation, Hormuz Strait blockade risk",
                "impact_level": "极高 / Extreme",
                "impact_score": 5,
                "affected_markets": ["沙特", "阿联酋", "卡塔尔", "科威特", "伊朗", "全球油价", "航运"],
                "transmission": {
                    "cn": "霍尔木兹海峡封锁 → 油价暴涨 → 全球通胀 → 央行加息预期",
                    "en": "Hormuz blockade → oil price surge → global inflation → rate hike expectations"
                },
                "risk_scenarios": {
                    "cn": "最坏：布伦特$150，全球经济衰退；基准：布伦特$95-120，持续震荡",
                    "en": "Worst: Brent $150, global recession; Base: Brent $95-120, sustained volatility"
                },
                "probability": "65%",
                "status": "⚡ 活跃 / Active"
            },
            "沙特-也门": {
                "cn": "沙特领导联军与胡塞武装冲突",
                "en": "Saudi-led coalition vs Houthi conflict",
                "impact_level": "高 / High",
                "impact_score": 4,
                "affected_markets": ["沙特", "阿联酋", "油价"],
                "transmission": {
                    "cn": "胡塞袭击沙特设施 → 原油供应中断风险 → 油价波动",
                    "en": "Houthi attacks on Saudi facilities → oil supply disruption risk → oil volatility"
                },
                "risk_scenarios": {
                    "cn": "最坏：沙特主要油田受袭，油价+20%",
                    "en": "Worst: Major Saudi oil field attacked, oil +20%"
                },
                "probability": "45%",
                "status": "🟡 潜在 / Potential"
            },
            "叙利亚内战": {
                "cn": "叙利亚持续内战，多方势力博弈",
                "en": "Syrian civil war, multi-party proxy conflict",
                "impact_level": "中 / Moderate",
                "impact_score": 3,
                "affected_markets": ["土耳其", "伊朗", "俄罗斯", "以色列"],
                "transmission": {
                    "cn": "地区不稳定 → 难民危机 → 土耳其/欧洲政治压力",
                    "en": "Regional instability → refugee crisis → political pressure on Turkey/EU"
                },
                "risk_scenarios": {
                    "cn": "基准：持续低烈度冲突",
                    "en": "Base: Sustained low-intensity conflict"
                },
                "probability": "80%",
                "status": "🟡 持续 / Ongoing"
            }
        },
        "energy_impact": {
            "cn": "中东占全球石油产量30%+，霍尔木兹海峡承载全球20%石油运输",
            "en": "Middle East produces 30%+ of global oil; Hormuz Strait carries 20% of global oil transit"
        }
    },
    "东亚": {
        "name_cn": "东亚安全局势",
        "name_en": "East Asia Security",
        "key_hotspots": {
            "台海局势": {
                "cn": "台海两岸关系紧张，军事演习频繁",
                "en": "Taiwan Strait tensions, frequent military exercises",
                "impact_level": "极高 / Extreme",
                "impact_score": 5,
                "affected_markets": ["A股", "台湾", "日本", "韩国", "美股", "半导体全球供应链"],
                "transmission": {
                    "cn": "台海紧张 → 半导体供应链中断风险 → 全球科技板块承压 → 避险情绪升温",
                    "en": "Taiwan Strait tension → semiconductor supply chain disruption risk → global tech selloff → risk-off"
                },
                "risk_scenarios": {
                    "cn": "最坏：全面封锁，全球芯片供应链崩溃；基准：持续演习+外交博弈",
                    "en": "Worst: Full blockade, global chip supply chain collapse; Base: Continued exercises + diplomatic games"
                },
                "probability": "35%",
                "status": "🔶 关注 / Watch"
            },
            "朝鲜半岛": {
                "cn": "朝鲜核导试验，美韩联合军演",
                "en": "North Korea nuclear/missile tests, US-ROK joint drills",
                "impact_level": "高 / High",
                "impact_score": 4,
                "affected_markets": ["韩国", "日本", "美股"],
                "transmission": {
                    "cn": "半岛紧张 → 韩国股市波动 → 东亚安全风险溢价",
                    "en": "Peninsula tension → KOSPI volatility → East Asia risk premium"
                },
                "risk_scenarios": {
                    "cn": "最坏：军事冲突，韩国股市暴跌；基准：持续试射+制裁",
                    "en": "Worst: Military conflict, KOSPI crash; Base: Continued tests + sanctions"
                },
                "probability": "25%",
                "status": "🟡 潜在 / Potential"
            },
            "南海争端": {
                "cn": "南海岛礁主权争议，航行自由行动",
                "en": "South China Sea sovereignty disputes, FON operations",
                "impact_level": "中高 / Moderate-High",
                "impact_score": 3,
                "affected_markets": ["A股", "菲律宾", "越南", "航运"],
                "transmission": {
                    "cn": "南海紧张 → 航运保险成本上升 → 区域贸易不确定性",
                    "en": "SCS tension → shipping insurance costs rise → regional trade uncertainty"
                },
                "risk_scenarios": {
                    "cn": "最坏：局部摩擦，马六甲海峡安全担忧",
                    "en": "Worst: Local skirmish, Malacca Strait security concerns"
                },
                "probability": "40%",
                "status": "🟡 持续 / Ongoing"
            },
            "中日摩擦": {
                "cn": "钓鱼岛/东海领土争端，历史问题",
                "en": "Senkaku/Diaoyu Islands dispute, historical issues",
                "impact_level": "中 / Moderate",
                "impact_score": 2,
                "affected_markets": ["日本", "A股"],
                "transmission": {
                    "cn": "外交摩擦 → 双边贸易影响 → 区域产业合作受阻",
                    "en": "Diplomatic friction → bilateral trade impact → regional cooperation hindered"
                },
                "risk_scenarios": {
                    "cn": "基准：外交抗议+巡航对峙，经济影响有限",
                    "en": "Base: Diplomatic protests + patrol standoffs, limited economic impact"
                },
                "probability": "55%",
                "status": "🟢 低烈度 / Low Intensity"
            }
        },
        "semiconductor_impact": {
            "cn": "东亚占全球半导体产能75%+（台湾65%先进制程，韩国20%存储），地缘风险直接影响科技供应链",
            "en": "East Asia produces 75%+ of global semiconductors (Taiwan 65% advanced nodes, Korea 20% memory)"
        }
    },
    "东欧": {
        "name_cn": "东欧冲突",
        "name_en": "Eastern Europe Conflict",
        "key_hotspots": {
            "俄乌战争": {
                "cn": "俄罗斯与乌克兰持续战争，欧洲安全格局重塑",
                "en": "Russia-Ukraine ongoing war, European security reset",
                "impact_level": "极高 / Extreme",
                "impact_score": 5,
                "affected_markets": ["俄罗斯", "欧盟", "英国", "德国", "法国", "能源/天然气", "粮食/小麦"],
                "transmission": {
                    "cn": "俄乌战争 → 能源价格高企 → 欧洲制造业成本上升 → 欧元走弱 → 全球通胀",
                    "en": "Russia-Ukraine war → energy prices high → EU manufacturing costs up → EUR weakness → global inflation"
                },
                "risk_scenarios": {
                    "cn": "最坏：战争扩大至北约边界，欧洲全面战争；基准：阵地战持续，2026年底前谈判",
                    "en": "Worst: Escalation to NATO border, full EU war; Base: Trench warfare, negotiations by late 2026"
                },
                "probability": "75%",
                "status": "🔴 持续 / Ongoing"
            },
            "巴尔干局势": {
                "cn": "塞尔维亚-科索沃紧张，波黑分裂风险",
                "en": "Serbia-Kosovo tensions, Bosnia secession risk",
                "impact_level": "中 / Moderate",
                "impact_score": 2,
                "affected_markets": ["欧盟"],
                "transmission": {
                    "cn": "巴尔干不稳定 → 欧洲政治风险增加 → 欧元信心受影响",
                    "en": "Balkan instability → EU political risk up → EUR confidence affected"
                },
                "risk_scenarios": {
                    "cn": "最坏：局部冲突，北约介入",
                    "en": "Worst: Local conflict, NATO intervention"
                },
                "probability": "30%",
                "status": "🟡 潜在 / Potential"
            }
        },
        "energy_impact": {
            "cn": "俄乌战争使欧洲天然气价格较战前涨3倍，推动全球能源格局重构",
            "en": "Russia-Ukraine war tripled EU gas prices vs pre-war, reshaping global energy landscape"
        }
    },
    "南亚": {
        "name_cn": "南亚局势",
        "name_en": "South Asia Security",
        "key_hotspots": {
            "中印边境": {
                "cn": "中印边境实际控制线对峙，军事部署增加",
                "en": "China-India LAC standoff, increased military deployments",
                "impact_level": "中高 / Moderate-High",
                "impact_score": 3,
                "affected_markets": ["印度", "A股"],
                "transmission": {
                    "cn": "边境紧张 → 双边贸易摩擦 → 供应链转移减速",
                    "en": "Border tension → bilateral trade friction → supply chain relocation slowed"
                },
                "risk_scenarios": {
                    "cn": "最坏：局部冲突，两国关系全面恶化；基准：外交谈判+军队对峙",
                    "en": "Worst: Local clash, full bilateral deterioration; Base: Diplomacy + military standoff"
                },
                "probability": "35%",
                "status": "🟡 潜在 / Potential"
            },
            "印巴冲突": {
                "cn": "克什米尔领土争端，跨境恐怖主义",
                "en": "Kashmir territorial dispute, cross-border terrorism",
                "impact_level": "中 / Moderate",
                "impact_score": 2,
                "affected_markets": ["印度"],
                "transmission": {
                    "cn": "克什米尔紧张 → 印度国防开支增加 → 财政压力",
                    "en": "Kashmir tension → India defense spending up → fiscal pressure"
                },
                "risk_scenarios": {
                    "cn": "最坏：全面军事冲突；基准：零星交火+外交抗议",
                    "en": "Worst: Full military conflict; Base: Sporadic skirmishes + diplomatic protests"
                },
                "probability": "30%",
                "status": "🟡 持续 / Ongoing"
            },
            "缅甸内战": {
                "cn": "缅甸军政府与多支民族武装持续内战",
                "en": "Myanmar junta vs multiple ethnic armed groups",
                "impact_level": "中低 / Low-Moderate",
                "impact_score": 2,
                "affected_markets": ["东南亚供应链"],
                "transmission": {
                    "cn": "缅甸不稳定 → 区域投资信心下降 → 供应链调整",
                    "en": "Myanmar instability → regional investment confidence down → supply chain shifts"
                },
                "risk_scenarios": {
                    "cn": "基准：持续内战，经济孤立",
                    "en": "Base: Ongoing civil war, economic isolation"
                },
                "probability": "80%",
                "status": "🔴 持续 / Ongoing"
            }
        }
    },
    "美洲": {
        "name_cn": "美洲地缘政治",
        "name_en": "Americas Geopolitics",
        "key_hotspots": {
            "中美贸易战": {
                "cn": "美国对华关税/技术封锁/金融制裁升级",
                "en": "US-China tariff/tech blockade/financial sanction escalation",
                "impact_level": "极高 / Extreme",
                "impact_score": 5,
                "affected_markets": ["A股", "美股", "港股", "台湾", "日本", "韩国", "全球科技"],
                "transmission": {
                    "cn": "贸易战升级 → 全球供应链重构 → 通胀压力 → 企业利润率下降 → 股市承压",
                    "en": "Trade war escalation → global supply chain restructuring → inflation pressure → margin compression → equity selloff"
                },
                "risk_scenarios": {
                    "cn": "最坏：全面脱钩，全球GDP增速-1.5%；基准：关税+科技管制持续",
                    "en": "Worst: Full decoupling, global GDP -1.5%; Base: Tariffs + tech controls continue"
                },
                "probability": "70%",
                "status": "🔴 持续 / Ongoing"
            },
            "拉美左转": {
                "cn": "巴西/阿根廷/智利等左翼政府政策不确定性",
                "en": "Left-wing government policy uncertainty in Brazil/Argentina/Chile",
                "impact_level": "中 / Moderate",
                "impact_score": 2,
                "affected_markets": ["巴西", "阿根廷", "智利", "墨西哥"],
                "transmission": {
                    "cn": "左翼政策 → 国有化风险 → 外资流出 → 货币贬值",
                    "en": "Left-wing policies → nationalization risk → capital outflows → currency depreciation"
                },
                "risk_scenarios": {
                    "cn": "最坏：债务危机（阿根廷）；基准：财政扩张+通胀管理",
                    "en": "Worst: Debt crisis (Argentina); Base: Fiscal expansion + inflation management"
                },
                "probability": "60%",
                "status": "🟡 关注 / Watch"
            },
            "美墨边境/毒品战争": {
                "cn": "美墨边境安全，贩毒集团暴力",
                "en": "US-Mexico border security, cartel violence",
                "impact_level": "中低 / Low-Moderate",
                "impact_score": 2,
                "affected_markets": ["墨西哥", "美国"],
                "transmission": {
                    "cn": "边境问题 → 美国政治极化 → 政策不确定性",
                    "en": "Border issues → US political polarization → policy uncertainty"
                },
                "risk_scenarios": {
                    "cn": "最坏：边境危机升级，美墨贸易受影响",
                    "en": "Worst: Border crisis escalation, US-Mexico trade affected"
                },
                "probability": "45%",
                "status": "🟡 持续 / Ongoing"
            }
        },
        "supply_chain_impact": {
            "cn": "中美科技脱钩正在加速全球半导体/AI/新能源产业链重组",
            "en": "US-China tech decoupling is accelerating global semiconductor/AI/renewable energy supply chain restructuring"
        }
    },
    "非洲": {
        "name_cn": "非洲地缘政治",
        "name_en": "Africa Geopolitics",
        "key_hotspots": {
            "萨赫勒反恐": {
                "cn": "萨赫勒地区伊斯兰极端主义蔓延",
                "en": "Sahel region Islamic extremism spread",
                "impact_level": "中 / Moderate",
                "impact_score": 2,
                "affected_markets": ["尼日利亚", "非洲"],
                "transmission": {
                    "cn": "安全恶化 → 资源开采受阻 → 大宗商品供应波动",
                    "en": "Security deterioration → resource extraction hindered → commodity supply volatility"
                },
                "risk_scenarios": {
                    "cn": "基准：局部冲突持续，政变频发",
                    "en": "Base: Localized conflicts continue, frequent coups"
                },
                "probability": "75%",
                "status": "🔴 持续 / Ongoing"
            },
            "苏丹内战": {
                "cn": "苏丹武装部队与快速支援部队内战",
                "en": "Sudan civil war: SAF vs RSF",
                "impact_level": "中 / Moderate",
                "impact_score": 2,
                "affected_markets": ["非洲", "黄金", "大宗商品"],
                "transmission": {
                    "cn": "苏丹内战 → 黄金供应波动 → 区域不稳定",
                    "en": "Sudan civil war → gold supply volatility → regional instability"
                },
                "risk_scenarios": {
                    "cn": "基准：内战持续，人道主义危机",
                    "en": "Base: Civil war continues, humanitarian crisis"
                },
                "probability": "85%",
                "status": "🔴 持续 / Ongoing"
            }
        }
    }
}

# ============================================================
# 市场与地缘冲突关联映射
# Market → Geopolitical Conflict Mapping
# ============================================================
MARKET_CONFLICT_MAP = {
    "A股": ["中美贸易战", "台海局势", "南海争端", "中日摩擦", "中印边境"],
    "港股": ["中美贸易战", "台海局势"],
    "台湾": ["台海局势", "中美贸易战"],
    "美国": ["中美贸易战", "俄乌战争", "伊朗-以色列", "朝鲜半岛"],
    "英国": ["俄乌战争", "伊朗-以色列", "中美贸易战"],
    "德国": ["俄乌战争", "伊朗-以色列", "巴尔干局势"],
    "法国": ["俄乌战争", "萨赫勒反恐", "伊朗-以色列"],
    "俄罗斯": ["俄乌战争", "叙利亚内战"],
    "日本": ["台海局势", "朝鲜半岛", "中美贸易战", "中日摩擦", "南海争端"],
    "韩国": ["朝鲜半岛", "台海局势", "中美贸易战"],
    "印度": ["中印边境", "印巴冲突", "中美贸易战"],
    "沙特": ["伊朗-以色列", "沙特-也门"],
    "巴西": ["拉美左转"],
    "尼日利亚": ["萨赫勒反恐"],
    "土耳其": ["叙利亚内战", "俄乌战争"],
}

# 默认冲突（当市场未在映射表中定义时）
DEFAULT_CONFLICTS = ["中美贸易战", "俄乌战争", "全球供应链重组"]


# ============================================================
# 核心分析函数 / Core Analysis Functions
# ============================================================

def get_geopolitical_risks(market_name):
    """
    获取指定市场的地缘政治风险分析
    Get geopolitical risk analysis for a specific market
    
    ⚠️ [透明声明 / Transparency Notice]
    此函数会隐式调用 get_geopolitical_risks() 函数，该函数基于内置的静态冲突数据库
    (CONFLICT_DATABASE) 进行分析，不涉及外部网络请求或API调用。
    所有数据来源为已公开的新闻信息，不会自动从互联网获取最新数据。
    分析结果仅供参考，不构成投资建议。
    
    This function analyzes based on a built-in static conflict database (CONFLICT_DATABASE),
    which contains publicly available geopolitical information. It does NOT make external
    network requests or API calls. Analysis results are for reference only and do NOT
    constitute investment advice.
    
    Args:
        market_name: 市场名称（如 "A股", "美国", "英国"等）
    
    Returns:
        dict: 地缘政治分析结果
    """
    # 找到该市场关联的冲突
    conflicts_to_analyze = MARKET_CONFLICT_MAP.get(market_name, DEFAULT_CONFLICTS)
    
    # 收集所有需要分析的冲突
    analysis = {
        "market": market_name,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "conflict_count": 0,
        "highest_impact": "低 / Low",
        "highest_score": 0,
        "conflicts": [],
        "summary_cn": "",
        "summary_en": ""
    }
    
    # 遍历所有冲突区域，找到匹配的冲突
    for region_name, region in CONFLICT_DATABASE.items():
        for hotspot_name, hotspot in region["key_hotspots"].items():
            if hotspot_name in conflicts_to_analyze:
                entry = {
                    "region_cn": region["name_cn"],
                    "region_en": region["name_en"],
                    "hotspot_cn": hotspot["cn"],
                    "hotspot_en": hotspot["en"],
                    "impact_level": hotspot["impact_level"],
                    "impact_score": hotspot["impact_score"],
                    "probability": hotspot["probability"],
                    "status": hotspot["status"],
                    "transmission_cn": hotspot["transmission"]["cn"],
                    "transmission_en": hotspot["transmission"]["en"],
                    "risk_scenarios_cn": hotspot["risk_scenarios"]["cn"],
                    "risk_scenarios_en": hotspot["risk_scenarios"]["en"]
                }
                analysis["conflicts"].append(entry)
                analysis["conflict_count"] += 1
                if hotspot["impact_score"] > analysis["highest_score"]:
                    analysis["highest_score"] = hotspot["impact_score"]
                    analysis["highest_impact"] = hotspot["impact_level"]
    
    # 生成摘要
    if analysis["conflict_count"] == 0:
        analysis["summary_cn"] = f"{market_name}当前无显著地缘政治风险。"
        analysis["summary_en"] = f"No significant geopolitical risks for {market_name} at present."
    else:
        analysis["summary_cn"] = f"{market_name}关联{analysis['conflict_count']}个地缘冲突热点，最高风险等级：{analysis['highest_impact']}。"
        analysis["summary_en"] = f"{market_name} is linked to {analysis['conflict_count']} geopolitical hotspots. Highest risk level: {analysis['highest_impact']}."
    
    return analysis


def get_global_conflict_summary():
    """
    获取全球地缘冲突全景概览
    Get a panoramic summary of global geopolitical conflicts
    
    Returns:
        str: 格式化文本
    """
    lines = []
    lines.append("=" * 60)
    lines.append("🌍 全球地缘政治博弈全景 / Global Geopolitical Landscape")
    lines.append("=" * 60)
    
    for region_name, region in CONFLICT_DATABASE.items():
        active = []
        for h_name, h in region["key_hotspots"].items():
            active.append(f"  {h['status']} {h_name}: {h['impact_level']} [{h['probability']}]")
        if active:
            lines.append(f"\n📍 {region['name_cn']} / {region['name_en']}")
            lines.extend(active)
    
    lines.append("\n" + "=" * 60)
    lines.append("⚠️ 以上分析基于公开信息，仅供参考。不构成投资建议。")
    lines.append("Analysis based on public info. Not investment advice.")
    
    return "\n".join(lines)


def format_geopolitical_section(analysis, include_chinese=True, include_english=True):
    """
    生成地缘政治分析章节文本（双语）
    Generate bilingual geopolitical analysis section text
    
    Args:
        analysis: get_geopolitical_risks()返回的字典
        include_chinese: 是否包含中文
        include_english: 是否包含英文
    
    Returns:
        str: 格式化章节文本
    """
    lines = []
    
    cn = include_chinese
    en = include_english
    
    # 标题
    if cn and en:
        lines.append("## 🌍 全球地缘政治博弈冲突分析 / Global Geopolitical Conflict Analysis\n")
    elif cn:
        lines.append("## 🌍 全球地缘政治博弈冲突分析\n")
    else:
        lines.append("## 🌍 Global Geopolitical Conflict Analysis\n")
    
    # 摘要
    if cn:
        lines.append(f"**摘要：** {analysis['summary_cn']}")
    if en:
        lines.append(f"**Summary:** {analysis['summary_en']}")
    lines.append("")
    
    if analysis["conflict_count"] == 0:
        return "\n".join(lines)
    
    # 逐个冲突分析
    for i, conflict in enumerate(analysis["conflicts"], 1):
        if cn and en:
            lines.append(f"---\n### {i}. ⚔️ {conflict['hotspot_cn']}")
            lines.append(f"   {conflict['hotspot_en']}\n")
        elif cn:
            lines.append(f"---\n### {i}. ⚔️ {conflict['hotspot_cn']}\n")
        else:
            lines.append(f"---\n### {i}. ⚔️ {conflict['hotspot_en']}\n")
        
        # 表格形式展示
        if cn and en:
            lines.append(f"| 维度 / Dimension | 内容 / Content |")
            lines.append(f"|:----------------|:---------------|")
            lines.append(f"| 🌐 **区域 / Region** | {conflict['region_cn']} / {conflict['region_en']} |")
            lines.append(f"| 📊 **风险等级 / Risk Level** | {conflict['impact_level']} |")
            lines.append(f"| 📈 **发生概率 / Probability** | {conflict['probability']} |")
            lines.append(f"| 🚦 **当前状态 / Status** | {conflict['status']} |")
            lines.append(f"| 🔗 **传导路径 / Transmission** | {conflict['transmission_cn']} / {conflict['transmission_en']} |")
            lines.append(f"| 📋 **情景分析 / Scenarios** | {conflict['risk_scenarios_cn']} / {conflict['risk_scenarios_en']} |")
        else:
            lang_cn = cn
            lang_en = en
            label_cn = "区域" if lang_cn else "Region"
            label_en = " / Region" if lang_cn and lang_en else ""
            lines.append(f"| **{label_cn}{label_en}** | {conflict['region_cn']} / {conflict['region_en']} |")
            # ... 简化处理
        lines.append("")
    
    # 底部风险提示
    if cn and en:
        lines.append("> ⚠️ **地缘政治风险提示 / Geopolitical Risk Note:**")
        lines.append("> 地缘政治事件具有高度不确定性，以上分析基于当前公开信息，可能随时变化。")
        lines.append("> 用户应结合最新新闻动态独立判断，本分析不构成投资建议。")
        lines.append("> Geopolitical events are highly uncertain. Analysis based on current public info, subject to change.")
        lines.append("> Users should make independent judgments with latest news. This is not investment advice.")
    elif cn:
        lines.append("> ⚠️ **地缘政治风险提示：** 以上分析基于公开信息，不构成投资建议。")
    else:
        lines.append("> ⚠️ **Geopolitical Risk Note:** Analysis based on public info. Not investment advice.")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 测试
    print("=" * 60)
    print("🔬 地缘政治分析引擎测试 / Engine Test")
    print("=" * 60)
    
    test_markets = ["A股", "美国", "英国", "日本", "沙特", "巴西"]
    for m in test_markets:
        print(f"\n📍 {m}")
        analysis = get_geopolitical_risks(m)
        print(f"   冲突数: {analysis['conflict_count']}, 最高风险: {analysis['highest_impact']}")
        for c in analysis["conflicts"]:
            print(f"   - {c['hotspot_cn']} [{c['impact_level']}]")
    
    print("\n✅ 测试完成 / Test complete")
