#!/usr/bin/env python3
"""
父母的功课 - 家庭教育分析器

核心功能：
1. 分析父母说这句话的原因
2. 分析小孩行为的原因
3. 解释背后的逻辑
4. 预测对小孩未来成长的影响

用法:
    python3 scripts/education_analyzer.py
"""

import sys
from typing import Dict, Optional

# 父母话语分析库
PARENT_STATEMENTS = [
    {
        "key": "你真笨",
        "parent_reason": "父母感到挫败，用贬低来表达自己的无力感；可能自己童年也被这样对待",
        "child_reason": "孩子可能真的遇到了超出能力的困难，或有学习差异",
        "logic": "标签会变成孩子的身份认同——「我笨」成为自我定义",
        "future_impact": "低自尊、习得性无助、害怕尝试、完美主义或彻底放弃"
    },
    {
        "key": "你怎么这么不听话",
        "parent_reason": "父母感到失去控制，用「听话」来维护权威；把服从等同于爱",
        "child_reason": "孩子在发展自主性，或有不理解的规则，或有被压抑的需求",
        "logic": "听话是为了避免惩罚，不是内化规则；越控制越反抗",
        "future_impact": "表面顺从内心叛逆，或失去自主性，或建立虚假顺从人格"
    },
    {
        "key": "再不听话就不要你了",
        "parent_reason": "父母感到失控，用抛弃威胁来获得控制；可能自己也有被抛弃的恐惧",
        "child_reason": "孩子可能真的感到不安全，或在测试爱的边界，或有情感需求",
        "logic": "爱是有条件的——必须做什么才能被爱；被抛弃的恐惧会刻入潜意识",
        "future_impact": "焦虑型依恋、害怕被抛弃、难以建立健康关系、讨好型人格"
    },
    {
        "key": "看看别人家孩子",
        "parent_reason": "父母想激励孩子，但不知道如何正面表达；可能自己也在被比较中长大",
        "child_reason": "孩子可能在某方面确实有困难，或与父母期望有差距",
        "logic": "比较摧毁自尊，激发嫉妒而非动力；竞争=我永远不够好",
        "future_impact": "嫉妒、无法欣赏他人、低自尊、过度竞争或完全放弃"
    },
    {
        "key": "我为你好",
        "parent_reason": "父母真的相信这是为孩子好，但可能不清楚孩子真正需要什么",
        "child_reason": "孩子有自己的感受和判断，可能与父母的「好」不同",
        "logic": "以爱为名的控制还是控制；孩子的感受被否定",
        "future_impact": "情感隔离、难以识别自己感受、或过度顺从或极度叛逆"
    },
    {
        "key": "你怎么这么没出息",
        "parent_reason": "父母对自己或孩子有未实现的期望，恐惧孩子会失败",
        "child_reason": "孩子可能有自己的节奏，或在探索自我，或在某方面确实困难",
        "logic": "投射焦虑——父母把自己的恐惧放在孩子身上",
        "future_impact": "成就焦虑、无法享受成功、持续不满足、耗竭感"
    },
    {
        "key": "别烦我",
        "parent_reason": "父母自己疲惫、压力大、或情感需求未被满足；可能童年也在被忽视中长大",
        "child_reason": "孩子有真实的需求，可能是情感、关注、或基本需要",
        "logic": "我的需求>孩子的需求；孩子应该理解；情感忽视会代际传递",
        "future_impact": "情感忽视创伤、难以识别自己需求、假性独立或过度依赖"
    },
    {
        "key": "我这么辛苦都是为了你",
        "parent_reason": "父母感到不被认可，用牺牲来索取情感债务",
        "child_reason": "孩子感到被情感绑架，产生深深的愧疚感",
        "logic": "爱=牺牲=债务；孩子欠父母一辈子；愧疚是控制工具",
        "future_impact": "愧疚型人格、难以拒绝、边界不清、为别人而活、抑郁风险"
    },
    {
        "key": "你必须按我说的做",
        "parent_reason": "父母感到不确定，需要通过控制来获得安全感",
        "child_reason": "孩子在发展自主性，需要练习做决定和承担后果",
        "logic": "控制=保护；不允许犯错=不允许成长；决定=责任=恐惧",
        "future_impact": "决策困难、依赖他人、无法承受错误、或极度反叛"
    },
    {
        "key": "不准哭",
        "parent_reason": "父母无法处理孩子的情绪，认为情绪=软弱",
        "child_reason": "孩子有真实的情绪需要被表达和释放",
        "logic": "情绪是坏的；哭泣=软弱；情绪不被允许=感受被切断",
        "future_impact": "情绪压抑、述情障碍、无法识别/表达情绪、躯体化症状"
    },
    {
        "key": "你一定能考第一名",
        "parent_reason": "父母把自己的价值建立在孩子的成就上",
        "child_reason": "孩子承受巨大压力，害怕失败",
        "logic": "我成功=你成功；成就=价值；失败=不被爱",
        "future_impact": "考试焦虑、成就焦虑、无法接受失败、完美主义、抑郁风险"
    },
]

# 小孩行为分析库
CHILD_BEHAVIORS = [
    {
        "key": "发脾气",
        "parent_reason": "父母感到失控、尴尬、或认为孩子在「操控」",
        "child_reason": "情绪调节能力未发展完成；有未被满足的需求；表达能力有限",
        "logic": "发脾气是唯一能让大人听见的方式；情绪太强烈无法用语言表达",
        "future_impact": "如果被惩罚=学会用更强的方式表达；如果被倾听=学会情绪管理"
    },
    {
        "key": "说谎",
        "parent_reason": "父母感到被背叛、愤怒、恐惧（孩子变坏）",
        "child_reason": "害怕惩罚；想保护自己；想符合父母期望；不知道真相是什么",
        "logic": "真话=惩罚；假话=安全；真话不被接受=撒谎是生存策略",
        "future_impact": "复杂谎言、羞耻感、无法信任、或者完全失去自我认同"
    },
    {
        "key": "打人或破坏东西",
        "parent_reason": "父母感到恐惧、愤怒、失控",
        "child_reason": "无法用语言表达强烈情绪；感到挫败；感官处理差异；模仿家里的互动模式",
        "logic": "暴力=表达感受的唯一方式；或者这是我的挫败感出口",
        "future_impact": "攻击性问题行为；或完全压抑攻击性导致其他问题；人际关系困难"
    },
    {
        "key": "不听话",
        "parent_reason": "父母感到权威受到挑战、失控",
        "child_reason": "发展自主性；有不同意见；测试界限；不理解规则原因",
        "logic": "我有自己的想法；父母的规则不一定合理；我要做我自己",
        "future_impact": "健康的自主性发展；或演变成权力斗争；或完全顺从失去自我"
    },
    {
        "key": "沉迷手机",
        "parent_reason": "父母感到恐惧（成瘾、影响成绩、孩子「变坏」）",
        "child_reason": "逃避现实压力；获得在现实中没有的成就感/连接感；习惯性逃避",
        "logic": "手机=唯一能让我感觉好的东西；现实=痛苦/无聊/被否定",
        "future_impact": "真性或假性成瘾；学业/社交受损；或青春期后自愈；或家庭关系破裂"
    },
    {
        "key": "说恨父母",
        "parent_reason": "父母感到被背叛、伤心、愤怒、恐惧（孩子不爱我）",
        "child_reason": "孩子感到被误解/控制/不被允许有负面情绪；用激烈方式表达痛苦",
        "logic": "我在表达痛苦，不一定是恨父母；或者我在测试你是否爱我",
        "future_impact": "如果被惩罚=学会压抑；如果被倾听=学会表达感受；或变成持续对抗"
    },
    {
        "key": "不写作业",
        "parent_reason": "父母感到焦虑（孩子的未来）、失控、作为父母的失败",
        "child_reason": "作业太难/太无聊；有学习困难；动力问题；反抗控制；逃避挫败感",
        "logic": "作业=惩罚；或者我真的做不到；或者这是我能控制的",
        "future_impact": "学习动力下降；学业困难；亲子关系恶化；或者学会应付了事"
    },
    {
        "key": "欺负其他小朋友",
        "parent_reason": "父母感到羞耻、恐惧（孩子是「霸凌者」）、愤怒",
        "child_reason": "可能是受害者在反击；模仿家里的互动模式；寻求权力/关注；社交技能缺失",
        "logic": "欺负=有力量；或者我不被理解只能用这种方式沟通",
        "future_impact": "攻击性问题行为；人际关系困难；行为问题持续；或干预后改善"
    },
]


class EducationAnalyzer:
    """家庭教育分析器"""

    def analyze(self, text: str) -> Optional[Dict]:
        """分析一句话或行为"""
        # 检查父母话语
        for item in PARENT_STATEMENTS:
            if item["key"] in text:
                return {
                    "type": "parent_statement",
                    "matched": item["key"],
                    "parent_reason": item["parent_reason"],
                    "child_reason": item["child_reason"],
                    "logic": item["logic"],
                    "future_impact": item["future_impact"]
                }

        # 检查小孩行为
        for item in CHILD_BEHAVIORS:
            if item["key"] in text:
                return {
                    "type": "child_behavior",
                    "matched": item["key"],
                    "parent_reason": item["parent_reason"],
                    "child_reason": item["child_reason"],
                    "logic": item["logic"],
                    "future_impact": item["future_impact"]
                }

        return None

    def format_result(self, result: Optional[Dict]) -> str:
        """格式化分析结果"""
        if not result:
            return "未找到相关分析，请尝试其他表述。"

        output = []
        output.append("")
        output.append("=" * 50)
        output.append("分析报告")
        output.append("=" * 50)

        matched = result["matched"]
        if result["type"] == "parent_statement":
            output.append("\n【父母的话】")
            output.append("\"" + matched + "\"")
        else:
            output.append("\n【孩子的行为】")
            output.append("\"" + matched + "\"")

        output.append("")
        output.append("-" * 50)
        output.append("\n父母说这句话的原因：")
        output.append("   " + result["parent_reason"])
        output.append("\n孩子这样做的原因：")
        output.append("   " + result["child_reason"])
        output.append("\n背后的逻辑：")
        output.append("   " + result["logic"])
        output.append("\n对孩子未来成长的影响：")
        output.append("   " + result["future_impact"])
        output.append("")
        output.append("-" * 50)

        return "".join(output)


def main():
    print("\n" + "=" * 50)
    print("父母的功课 - 家庭教育分析器")
    print("=" * 50)

    analyzer = EducationAnalyzer()

    print("\n请输入一句话或行为，我来帮你分析：")
    print("示例：")
    print("  父母：再不听话就不要你了")
    print("  父母：你真笨")
    print("  孩子：发脾气、说谎、不听话")
    print("  孩子：沉迷手机")
    print("\n输入 quit 退出\n")

    while True:
        try:
            user_input = input("输入: ").strip()
        except EOFError:
            break

        if user_input.lower() == "quit":
            print("\n再见！")
            break

        if user_input:
            result = analyzer.analyze(user_input)
            output = analyzer.format_result(result)
            print(output)


if __name__ == "__main__":
    main()
