# -*- coding: utf-8 -*-
"""大乐透理性购彩 · 权威事实数据模块（教育/防骗用途）。

本模块仅汇总来自官方/权威来源的、已核实的彩票随机性与责任购彩事实。
无任何"预测号码""稳赚策略"等内容 —— 彩票开奖完全随机、相互独立，
任何宣称可预测中奖号码的说法均为不实信息。

所有数值均引自下方 sources 列出的来源，不编造、不引申。
"""

import json


def get_facts():
    """返回一份权威事实数据的全新副本（dict）。

    字段含义见各键名；所有数值均与 cited sources 一致。
    """
    return {
        # 大乐透头奖中奖概率（官方公布的整数注头奖概率）
        "jackpot_odds": "1/21,425,712",
        "jackpot_odds_human": "约2142万分之一",

        # 被雷击中的概率（天津体彩「津彩安全课」对比用）
        "lightning_odds": "1/1,750,000",
        "lightning_odds_human": "约175万分之一",

        # AI 能否预测：不能。每次开奖是完全独立、随机的物理事件。
        "ai_cannot_predict": True,
        "ai_cannot_predict_note": (
            "体彩官网(gstc)明确：即便是 AI 也无法从历史数据预测中奖号码；"
            "每次开奖是完全独立、随机的物理事件。来源: "
            "https://www.gstc.org.cn/newsDetail/010300/77254"
        ),

        # 各期开奖相互独立，历史数据对未来结果无影响
        "draws_independent": True,
        "draws_independent_note": (
            "人民网/中新网专家观点：数字型彩票开奖结果完全随机，是常识；"
            "历史开奖数据对下一期结果没有任何影响。"
        ),

        # 常见认知陷阱解释
        "gambler_fallacy": (
            "概率补偿谬误（赌徒谬误）：某号码久未开出，不等于它下一期更可能开出；"
            "每期开奖相互独立，历史遗漏不提高该号出现概率。"
        ),
        "sunk_cost": (
            "沉没成本效应：已经投入的购彩成本与未来中奖概率毫无关系；"
            "不要为'回本'而继续追投，追损只会扩大支出。"
        ),
        "illusion_of_control": (
            "控制幻觉：选号方式（机选/自选/冷热号/生日号）均不改变中奖概率；"
            "没有任何方法或 AI 工具能预测开奖结果。"
        ),

        # 公益金比例：每注 2 元中约 0.72 元进入公益金
        "charity_per_ticket": "0.72元/2元",

        # 官方理性购彩建议（要点）
        "official_advice": [
            "量力而行设预算：把购彩当小额娱乐，预设可承受上限，不超支不借贷",
            "认清公益属性：彩票是国家公益彩票，主要价值在支持公益而非投资获利",
            "警惕预测专家与倍投陷阱：不信'包中/AI选号'，不参与非法线上售彩与计划投注",
            "只用正规实体店渠道：仅在官方授权实体店购买，远离非官方APP与私人代购",
        ],

        # 来源清单
        "sources": [
            {
                "name": "体彩官网「责任体彩」《彩票没有\"预言家\",理性才是\"护身符\"》",
                "url": "https://www.gstc.org.cn/newsDetail/010300/77254",
            },
            {
                "name": "人民网彩票频道（专家观点：随机性是常识、历史数据无影响）",
                "url": "https://caipiao.people.com.cn/",
            },
            {
                "name": "中新网报道（专家观点）",
                "url": "https://m.chinanews.com/wap/detail/cht/zw/7577417.shtml",
            },
            {
                "name": "广东体彩 黄永志专访《安心购彩,是对公益的尊重,也是对生活的守护》",
                "url": "https://www.gdlottery.cn/html/ticaidongtai/20260630/94350.html",
            },
            {
                "name": "天津体彩《\"津\"彩安全课》（雷击概率对比、公益金比例）",
                "url": "https://www.tjtc.org.cn/c/2026-03-10/37865279.shtml",
            },
        ],
    }


# 模块级便捷别名：FACTS 为当前事实数据的一份副本
FACTS = get_facts()


def main():
    """打印事实数据为 JSON，供验证使用（ensure_ascii=False 保留中文）。"""
    print(json.dumps(get_facts(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
