#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dalio Macro Analyzer — 达利欧宏观分析工具
基于"五大力量"框架进行宏观形势评估与投资组合建议

用法：
  python macro_analyzer.py --country US --cycle stagflation
  python macro_analyzer.py --portfolio --risk-mode stagflation
  python macro_analyzer.py --forces --country US
"""

import sys
import argparse

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ─────────────────────────────────────────────
# 五大力量评估数据库（当前预设：2026年美国）
# ─────────────────────────────────────────────

COUNTRY_PROFILES = {
    "US": {
        "name": "美国",
        "forces": {
            "debt_monetary": {
                "score": 8,
                "key_signals": [
                    "债务/GDP ≈ 130%（警戒线 100%）",
                    "财政赤字 2万亿/年，占GDP约7%",
                    "利息支付占政府收入约18%",
                    "美债海外持有比例持续下降",
                    "美联储信誉面临考验，降息受制于通胀"
                ],
                "cycle_stage": "滞胀期（Stagflation）"
            },
            "domestic_politics": {
                "score": 7,
                "key_signals": [
                    "左右翼极化达历史高位",
                    "中期选举共和党可能失去众议院",
                    "财富差距扩大，AI加剧分化",
                    "60%美国人阅读水平低于6年级",
                    "财富税讨论升温，可能触发资产抛售"
                ],
                "cycle_stage": "高度撕裂期"
            },
            "world_order": {
                "score": 7,
                "key_signals": [
                    "从多边秩序 → 强权竞争秩序",
                    "霍尔木兹海峡控制权未明",
                    "各国重评美国军事保护能力",
                    "人民币结算交易快速增加",
                    "全球领导人质疑：美国还能赢吗？"
                ],
                "cycle_stage": "权力转移加速期"
            },
            "natural_shocks": {
                "score": 4,
                "key_signals": [
                    "石油占全球GDP约4%（历史危机期10%）",
                    "新能源替代加速，永久性结构调整",
                    "中东冲突造成短期能源扰动",
                    "供应链多元化进行中"
                ],
                "cycle_stage": "中等压力"
            },
            "technology": {
                "score": 6,
                "key_signals": [
                    "AI快速提升生产率，同时大幅削减就业",
                    "技术财富集中效应，加剧贫富差距",
                    "财富税可能成为AI时代泡沫破裂触发点",
                    "美中AI竞争进入关键阶段",
                    "达利欧本人用AI重建桥水决策系统"
                ],
                "cycle_stage": "革命性变革期"
            }
        }
    },
    "CN": {
        "name": "中国",
        "forces": {
            "debt_monetary": {
                "score": 6,
                "key_signals": [
                    "地方政府隐性债务风险依然存在",
                    "房地产去杠杆持续",
                    "外贸顺差积累大量外汇储备",
                    "人民币国际化稳步推进"
                ],
                "cycle_stage": "去杠杆中期"
            },
            "domestic_politics": {
                "score": 4,
                "key_signals": [
                    "政治体制稳定，无明显内部撕裂",
                    "经济下行压力带来社会情绪压力",
                    "青年失业率偏高需关注"
                ],
                "cycle_stage": "稳定期（有压力）"
            },
            "world_order": {
                "score": 7,
                "key_signals": [
                    "美中贸易博弈持续",
                    "大量资金积累，全球再配置中",
                    "一带一路提升地缘影响力",
                    "中东石油约占中国能源进口6%"
                ],
                "cycle_stage": "崛起挑战期"
            },
            "natural_shocks": {
                "score": 3,
                "key_signals": [
                    "能源多元化进展较好",
                    "太阳能等新能源快速扩张"
                ],
                "cycle_stage": "低压力"
            },
            "technology": {
                "score": 7,
                "key_signals": [
                    "AI竞争全面加速，DeepSeek等崛起",
                    "半导体自主化攻坚",
                    "数字人民币推进"
                ],
                "cycle_stage": "高速追赶期"
            }
        }
    }
}

# ─────────────────────────────────────────────
# 投资组合配置建议库
# ─────────────────────────────────────────────

PORTFOLIO_CONFIGS = {
    "all_weather_base": {
        "name": "达利欧全天候基础组合",
        "description": "适用于无法判断经济环境时，风险平价分配",
        "weights": {
            "A股/全球股票": 30,
            "长期国债（20年+）": 40,
            "中期国债（7-10年）": 15,
            "黄金": 7.5,
            "大宗商品": 7.5
        }
    },
    "stagflation": {
        "name": "滞胀环境组合（当前美国 2026）",
        "description": "高通胀+低增长，债券受损，实物资产受益",
        "weights": {
            "全球股票（防御型）": 20,
            "长期国债": 20,
            "中期国债/TIPS": 15,
            "黄金": 15,
            "大宗商品（能源/农业）": 15,
            "现金/短债": 10,
            "另类资产/对冲基金": 5
        }
    },
    "deflation": {
        "name": "通缩萧条组合",
        "description": "需求崩溃，持有现金和短期高质量债券",
        "weights": {
            "现金及等价物": 35,
            "短期高评级国债": 35,
            "黄金": 15,
            "防御型股票（必需消费）": 10,
            "大宗商品": 5
        }
    },
    "boom": {
        "name": "繁荣扩张组合",
        "description": "信贷扩张、经济强劲、通胀温和",
        "weights": {
            "成长股/科技股": 40,
            "中期国债": 25,
            "大宗商品": 15,
            "黄金": 10,
            "现金": 10
        }
    }
}

# ─────────────────────────────────────────────
# 核心分析函数
# ─────────────────────────────────────────────

def print_forces_analysis(country_code="US"):
    """输出五大力量评估报告"""
    profile = COUNTRY_PROFILES.get(country_code.upper())
    if not profile:
        print(f"暂无 {country_code} 数据，当前支持: {', '.join(COUNTRY_PROFILES.keys())}")
        return

    name = profile["name"]
    forces = profile["forces"]

    print(f"\n{'='*60}")
    print(f"  达利欧五大力量分析 — {name} (2026年4月)")
    print(f"{'='*60}")

    force_names = {
        "debt_monetary": "Force 1  债务与货币周期",
        "domestic_politics": "Force 2  国内政治秩序撕裂",
        "world_order": "Force 3  大国秩序重组",
        "natural_shocks": "Force 4  自然冲击",
        "technology": "Force 5  技术变革"
    }

    total_score = 0
    scores = []
    for key, display in force_names.items():
        data = forces[key]
        score = data["score"]
        total_score += score
        scores.append(score)
        bar = "█" * score + "░" * (10 - score)
        print(f"\n  {display}")
        print(f"  风险压力: [{bar}] {score}/10  ({data['cycle_stage']})")
        for signal in data["key_signals"][:3]:
            print(f"    • {signal}")

    avg_score = total_score / 5
    print(f"\n{'─'*60}")
    print(f"  综合风险指数: {avg_score:.1f}/10")

    if avg_score >= 7:
        level = "高风险 — 建议防御配置"
    elif avg_score >= 5:
        level = "中高风险 — 建议均衡配置"
    elif avg_score >= 3:
        level = "中等风险 — 可适度进攻"
    else:
        level = "低风险 — 可积极配置"

    print(f"  风险级别: {level}")
    print(f"{'='*60}\n")


def print_portfolio(risk_mode="all_weather_base"):
    """输出投资组合配置建议"""
    config = PORTFOLIO_CONFIGS.get(risk_mode)
    if not config:
        available = ', '.join(PORTFOLIO_CONFIGS.keys())
        print(f"未知模式 '{risk_mode}'，可选: {available}")
        return

    print(f"\n{'='*60}")
    print(f"  {config['name']}")
    print(f"  {config['description']}")
    print(f"{'='*60}")
    print(f"  {'资产类别':<25} {'权重':>6}  {'可视化'}")
    print(f"  {'─'*50}")

    for asset, weight in config["weights"].items():
        bar = "█" * (weight // 3) + ("▌" if weight % 3 >= 1 else "")
        print(f"  {asset:<25} {weight:>5}%  {bar}")

    print(f"  {'─'*50}")
    total = sum(config["weights"].values())
    print(f"  {'合计':<25} {total:>5}%")

    print(f"\n  达利欧核心提示：")
    print(f"  • 构建真正平衡、高度分散的组合，不要择时")
    print(f"  • 黄金应占组合的 5%-15%（法定货币对冲）")
    print(f"  • 现在降息是错误——滞胀环境需保持货币信誉")
    print(f"  • 注意外汇管制、财富税等游戏规则变化风险")
    print(f"{'='*60}\n")


def print_debt_cycle_check(country_code="US"):
    """债务周期快速定位检查"""
    print(f"\n{'='*60}")
    print(f"  债务周期快速定位 — {'美国' if country_code.upper()=='US' else country_code}")
    print(f"{'='*60}")

    checklist = {
        "政府债务/GDP > 100%": True,
        "财政赤字/GDP > 5%": True,
        "利息支付/收入 > 15%": True,
        "通胀 > 目标 1.5 倍": True,
        "央行资产负债表仍大": True,
        "实际利率长期偏低": True,
        "国债海外持有比例下降": True,
        "央行购金加速": True,
        "货币信誉受到质疑": True,
        "经常账户赤字 > 3%": False,
    }

    triggered = 0
    print(f"\n  {'指标':<35} {'状态'}")
    print(f"  {'─'*45}")
    for item, status in checklist.items():
        mark = "✓ 是" if status else "✗ 否"
        if status:
            triggered += 1
        print(f"  {item:<35} {mark}")

    print(f"\n  触发数量: {triggered}/10")
    print(f"  {'─'*45}")

    if triggered >= 7:
        stage = "债务周期后期高风险区 — 滞胀/去杠杆临界"
    elif triggered >= 5:
        stage = "债务周期中后期 — 泡沫积累/顶部阶段"
    elif triggered >= 3:
        stage = "债务周期中期 — 扩张放缓"
    else:
        stage = "债务周期早期 — 扩张阶段"

    print(f"  当前阶段判断: {stage}")
    print(f"{'='*60}\n")


def print_holmuz_checklist():
    """霍尔木兹海峡胜利清单"""
    print(f"\n{'='*60}")
    print(f"  达利欧：美国在中东的'胜利清单'")
    print(f"{'='*60}")
    items = [
        ("霍尔木兹海峡控制权问题解决", False),
        ("伊朗核项目问题得到解决", False),
        ("导弹问题得到解决", False),
    ]
    for item, done in items:
        mark = "☑" if done else "☐"
        status = "已解决" if done else "未解决 — 全球影响持续"
        print(f"\n  {mark} {item}")
        print(f"     → {status}")

    print(f"\n  达利欧警告：")
    print(f"  '如果这些勾没有打全，影响就不会只停留在中东，")
    print(f"   而会外溢到全球资产价格、能源供应、货币流动，")
    print(f"   甚至各国对美国保护能力的重新评估。'")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="达利欧宏观分析工具")
    parser.add_argument("--forces", action="store_true", help="输出五大力量评估")
    parser.add_argument("--portfolio", action="store_true", help="输出投资组合建议")
    parser.add_argument("--debt-cycle", action="store_true", help="债务周期定位")
    parser.add_argument("--holmuz", action="store_true", help="霍尔木兹清单")
    parser.add_argument("--all", action="store_true", help="完整报告")
    parser.add_argument("--country", default="US", help="国家代码 (US/CN)")
    parser.add_argument("--risk-mode", default="stagflation",
                        choices=list(PORTFOLIO_CONFIGS.keys()),
                        help="投资组合模式")

    args = parser.parse_args()

    if not any([args.forces, args.portfolio, args.debt_cycle, args.holmuz, args.all]):
        args.all = True

    print(f"\n  达利欧宏观分析框架 v1.0.0")
    print(f"  基于《原则》《债务危机》《变化中的世界秩序》")
    print(f"  + 2026年4月CNBC最新发声")

    if args.all or args.forces:
        print_forces_analysis(args.country)

    if args.all or args.debt_cycle:
        print_debt_cycle_check(args.country)

    if args.all or args.portfolio:
        print_portfolio(args.risk_mode)

    if args.all or args.holmuz:
        print_holmuz_checklist()

    if args.all:
        print(f"\n  达利欧核心投资哲学：")
        print(f"  ─────────────────────────────────────────")
        print(f"  '投资就是现金流的现值。'")
        print(f"  '你必须有一个平衡、高度分散的组合，不要择时。'")
        print(f"  '储备货币的本质，是别人愿不愿意持有你发行的债务。'")
        print(f"  '历史在五大力量推动下不断重复。'")
        print()


if __name__ == "__main__":
    main()
