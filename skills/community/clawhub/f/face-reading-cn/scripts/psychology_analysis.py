#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
面相心理分析工具 v1.0
结合传统面相与现代心理学分析（娱乐参考）

使用方法:
    python psychology_analysis.py [面部特征]
    python psychology_analysis.py --mbti "眉毛浓密 额头高广 颧骨高"
    python psychology_analysis.py --suggestion "鼻子塌"
    python psychology_analysis.py --emotion "面色发黄"
    
示例:
    python psychology_analysis.py "眉毛浓密 眼睛有神 下巴方圆"
"""

import sys
import json
from typing import List, Dict

# MBTI 映射数据库
MBTI_MAPPING = {
    "E": {
        "features": ["眉毛浓密", "眉毛上扬", "眼睛大", "眼睛有神", "嘴巴大", "嘴角上扬"],
        "description": "外向型 (Extraversion) - 能量来自外部世界",
        "traits": ["喜欢社交", "表达直接", "行动快", "乐观开朗"],
        "career": ["销售", "市场", "公关", "管理", "培训"]
    },
    "I": {
        "features": ["眉毛稀疏", "眉毛下垂", "眼睛小", "眼神内敛", "嘴巴小", "嘴角平直"],
        "description": "内向型 (Introversion) - 能量来自内心世界",
        "traits": ["喜欢独处", "深思熟虑", "观察入微", "专注深入"],
        "career": ["研究", "编程", "写作", "设计", "分析"]
    },
    "N": {
        "features": ["额头高广", "眉眼间距宽", "耳朵位置高", "眼神飘忽"],
        "description": "直觉型 (Intuition) - 关注可能性和未来",
        "traits": ["想象力丰富", "关注未来", "喜欢抽象", "创新思维"],
        "career": ["策划", "创意", "研究", "咨询", "创业"]
    },
    "S": {
        "features": ["额头低平", "眉眼间距窄", "耳朵位置适中", "眼神专注"],
        "description": "感觉型 (Sensing) - 关注现实和细节",
        "traits": ["务实实际", "关注细节", "经验导向", "脚踏实地"],
        "career": ["会计", "审计", "工程", "医疗", "技工"]
    },
    "T": {
        "features": ["颧骨高", "颧骨线条明显", "嘴唇薄", "嘴角紧", "眼神锐利"],
        "description": "思考型 (Thinking) - 理性分析，逻辑优先",
        "traits": ["理性客观", "逻辑分析", "目标导向", "公平公正"],
        "career": ["法律", "金融", "IT", "工程", "咨询"]
    },
    "F": {
        "features": ["颧骨柔和", "颧骨有肉", "嘴唇厚", "嘴角软", "眼神柔和"],
        "description": "情感型 (Feeling) - 重情重义，共情能力强",
        "traits": ["情感丰富", "善解人意", "关系导向", "和谐追求"],
        "career": ["人力资源", "教育", "心理咨询", "护理", "艺术"]
    },
    "J": {
        "features": ["眉毛整齐", "眉毛有序", "下巴方圆", "下巴饱满", "面部线条清晰"],
        "description": "判断型 (Judging) - 喜欢结构和计划",
        "traits": ["计划性强", "条理分明", "追求完成", "守时可靠"],
        "career": ["管理", "行政", "项目管理", "会计", "法律"]
    },
    "P": {
        "features": ["眉毛自然", "眉毛杂乱", "下巴尖", "下巴柔和", "面部线条柔和"],
        "description": "知觉型 (Perceiving) - 喜欢灵活和开放",
        "traits": ["灵活随性", "适应力强", "喜欢开放", "享受过程"],
        "career": ["创意", "艺术", "自由职业", "咨询", "销售"]
    }
}

# 心理暗示数据库
SUGGESTION_DB = {
    "额头低": {
        "reframe": "务实脚踏实地，厚积薄发",
        "morning": "我的额头代表务实和脚踏实地，这是成功的重要品质。我相信厚积薄发，大器晚成。",
        "challenge": "我不需要比别人聪明，我只需要比别人坚持。我的务实会带我走向成功。",
        "action": ["每天学习30分钟", "记录小成就", "抬头挺胸增加自信"]
    },
    "额头高": {
        "reframe": "聪明智慧，有远见",
        "morning": "我拥有智慧和远见，今天我会用这些天赋创造价值，同时保持谦逊和学习的心态。",
        "challenge": "聪明是礼物也是责任，我需要用智慧帮助他人，而不是炫耀或傲慢。",
        "action": ["分享知识帮助他人", "持续学习", "培养谦逊"]
    },
    "眉毛稀疏": {
        "reframe": "独立专注，深度交往",
        "morning": "我的眉毛代表独立和深度，我不需要很多朋友，我只需要几个真正的朋友。我的独立是我的力量。",
        "challenge": "我可以选择深入交流而非泛泛而谈，质量胜过数量，我珍视每一段深度关系。",
        "action": ["维护核心关系", "培养独处能力", "深耕专业领域"]
    },
    "眉毛浓密": {
        "reframe": "人缘好，重情义",
        "morning": "我拥有良好的人缘和情义，今天我会用这些连接创造价值，同时注意保护自己的能量。",
        "challenge": "我可以对人好，但不必牺牲自己。我的善良需要有边界。",
        "action": ["学会说'不'", "平衡社交与独处", "选择深度而非广度"]
    },
    "眼睛小": {
        "reframe": "洞察力强，深思熟虑",
        "morning": "我的眼睛虽小但洞察力强，我观察到别人忽略的细节，这是我的天赋。我无需羡慕大眼睛的人。",
        "challenge": "我可以选择何时表达，我的沉默是金，当我说话时，别人会认真听。",
        "action": ["练习眼神交流", "提升表达能力", "善用观察力"]
    },
    "眼睛大": {
        "reframe": "开朗热情，感情丰富",
        "morning": "我的眼睛明亮有神，我能看到世界的美好，我会用这个能力发现机会和美好。",
        "challenge": "我的感情丰富是礼物，但我可以学会管理情绪，不让情绪控制我。",
        "action": ["情绪管理练习", "培养专注力", "学习深度思考"]
    },
    "鼻子塌陷": {
        "reframe": "务实节俭，稳健致富",
        "morning": "我的鼻子代表务实和节俭，这是财富积累的基础。我相信积少成多，稳健致富。财运来自努力而非鼻子形状。",
        "challenge": "我善于理财，我不冒不必要的风险，我的稳健会保护我的财富。",
        "action": ["建立储蓄习惯", "学习理财知识", "稳健投资"]
    },
    "鼻子高挺": {
        "reframe": "有领导力，财运好",
        "morning": "我有赚钱的能力和领导力，今天我会用这些能力创造价值，同时记住财富是工具而非目的。",
        "challenge": "我有赚钱能力，但也需要守财能力。谨慎投资，不贪不急。",
        "action": ["学习财富管理", "培养守财意识", "理性投资"]
    },
    "嘴角下垂": {
        "reframe": "深度思考，可以选择快乐",
        "morning": "我的嘴角并不代表悲观，它代表深度思考。我可以选择微笑，我选择今天保持乐观。",
        "challenge": "我嘴角上扬时，心情也会变好。微笑是我的选择，我选择快乐。",
        "action": ["每天微笑练习", "记录三件好事", "培养乐观思维"]
    },
    "下巴尖": {
        "reframe": "艺术气质，敏感细腻",
        "morning": "我的下巴代表艺术气质和敏感，我有独特的审美和感受力，我珍惜这份天赋。同时我会为晚年做规划。",
        "challenge": "我活在当下，也为未来做准备。储蓄和规划让我安心。",
        "action": ["培养艺术兴趣", "建立长期储蓄计划", "关注健康"]
    },
    "下巴方圆": {
        "reframe": "稳定可靠，有领导力",
        "morning": "我的下巴代表稳定和可靠，我是值得信赖的人，我的稳定给他人安全感。我会用这个品质帮助更多人。",
        "challenge": "我的可靠是我的优势，我需要学会适时放松，不必承担所有责任。",
        "action": ["发挥领导力", "学会 delegation", "培养灵活性"]
    }
}

# 情绪-面色关联
EMOTION_COMPLEXION = {
    "面色红润": {
        "emotion": "兴奋、愉悦或焦虑",
        "positive": "气血充足，身心和谐",
        "negative": "可能情绪激动或焦虑",
        "advice": ["深呼吸", "正念冥想", "区分是健康红润还是焦虑红润"]
    },
    "面色苍白": {
        "emotion": "恐惧、悲伤、疲劳",
        "psychology": "情绪性苍白源于恐惧时血管收缩，悲伤时能量低沉",
        "advice": ["识别恐惧/悲伤源头", "情绪表达", "建立安全感", "规律运动提升阳气"]
    },
    "面色发黄": {
        "emotion": "思虑过度、担忧、压抑",
        "psychology": "过度思考消耗能量，担忧影响消化系统",
        "advice": ["设定思考时间限制", "行动胜于完美", "运动疏泄", "培养行动力"]
    },
    "面色发青": {
        "emotion": "愤怒、压抑、长期压力",
        "psychology": "压抑愤怒导致肝气郁结",
        "advice": ["识别愤怒源头", "安全释放愤怒", "压力管理", "⚠️ 长期发青建议就医"]
    },
    "面色暗沉": {
        "emotion": "抑郁、压抑、睡眠不足",
        "psychology": "能量极低，情绪压抑",
        "advice": ["寻求专业帮助", "社交支持", "规律作息", "光照疗法"]
    }
}

def analyze_mbti(features: List[str]) -> Dict:
    """分析 MBTI 类型"""
    scores = {"E": 0, "I": 0, "N": 0, "S": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    
    for feature in features:
        for mbti_type, data in MBTI_MAPPING.items():
            if any(f in feature for f in data["features"]):
                scores[mbti_type] += 1
    
    # 确定类型
    ei = "E" if scores["E"] >= scores["I"] else "I"
    ns = "N" if scores["N"] >= scores["S"] else "S"
    tf = "T" if scores["T"] >= scores["F"] else "F"
    jp = "J" if scores["J"] >= scores["P"] else "P"
    
    mbti_type = f"{ei}{ns}{tf}{jp}"
    
    # 获取类型描述
    type_desc = {
        "ISTJ": "检查者 - 务实可靠，注重细节",
        "ISFJ": "保护者 - 温暖负责，忠诚体贴",
        "INFJ": "提倡者 - 理想主义，洞察力强",
        "INTJ": "建筑师 - 战略思维，独立果断",
        "ISTP": "鉴赏家 - 灵活务实，善于分析",
        "ISFP": "探险家 - 敏感艺术，活在当下",
        "INFP": "调停者 - 理想主义，情感丰富",
        "INTP": "逻辑学家 - 好奇分析，追求真理",
        "ESTP": "企业家 - 行动导向，适应力强",
        "ESFP": "表演者 - 热情活泼，享受生活",
        "ENFP": "竞选者 - 创意无限，热情洋溢",
        "ENTP": "辩论家 - 机智创新，喜欢挑战",
        "ESTJ": "总经理 - 务实高效，组织能力强",
        "ESFJ": "执政官 - 热心助人，重视和谐",
        "ENFJ": "主人公 - 魅力领导，关怀他人",
        "ENTJ": "指挥官 - 战略领导，果断高效"
    }
    
    return {
        "type": mbti_type,
        "description": type_desc.get(mbti_type, "独特个性"),
        "scores": scores,
        "dimensions": {
            "EI": {"result": ei, "E": scores["E"], "I": scores["I"]},
            "NS": {"result": ns, "N": scores["N"], "S": scores["S"]},
            "TF": {"result": tf, "T": scores["T"], "F": scores["F"]},
            "JP": {"result": jp, "J": scores["J"], "P": scores["P"]}
        }
    }

def get_suggestion(feature: str) -> Dict:
    """获取心理暗示"""
    for key, value in SUGGESTION_DB.items():
        if key in feature:
            return value
    return None

def analyze_emotion_complexion(complexion: str) -> Dict:
    """分析情绪-面色关联"""
    for key, value in EMOTION_COMPLEXION.items():
        if key in complexion or complexion in key:
            return value
    return None

def print_mbti_analysis(features: List[str]):
    """打印 MBTI 分析"""
    result = analyze_mbti(features)
    
    print("\n" + "="*60)
    print("🧠 面相-MBTI 性格分析")
    print("="*60)
    
    print(f"\n📊 您的 MBTI 类型: {result['type']}")
    print(f"💡 类型描述: {result['description']}")
    
    print("\n📈 维度分析:")
    for dim, data in result['dimensions'].items():
        if dim == "EI":
            label = "外向(E) ←→ 内向(I)"
        elif dim == "NS":
            label = "直觉(N) ←→ 感觉(S)"
        elif dim == "TF":
            label = "思考(T) ←→ 情感(F)"
        else:
            label = "判断(J) ←→ 知觉(P)"
        
        total = data[list(data.keys())[1]] + data[list(data.keys())[2]]
        if total > 0:
            print(f"  {label}: {data['result']} (支持度: 特征匹配)")
    
    print("\n🎯 性格画像:")
    for mbti_type, data in MBTI_MAPPING.items():
        if mbti_type in [result['type'][0], result['type'][1], result['type'][2], result['type'][3]]:
            if data["traits"]:
                print(f"  • {data['description'].split(' - ')[0]}: {', '.join(data['traits'][:3])}")
    
    print("\n💼 适合职业方向:")
    careers = set()
    for mbti_type, data in MBTI_MAPPING.items():
        if mbti_type in [result['type'][0], result['type'][1], result['type'][2], result['type'][3]]:
            careers.update(data["career"])
    print(f"  {', '.join(list(careers)[:5])}")
    
    print("\n💡 成长建议:")
    if result['type'][0] == 'E':
        print("  • 发挥外向优势，同时学会独处充电")
    else:
        print("  • 珍惜独处时光，同时适度社交")
    
    if result['type'][1] == 'N':
        print("  • 发挥想象力，同时注意落地执行")
    else:
        print("  • 发挥务实精神，同时保持开放")
    
    if result['type'][2] == 'T':
        print("  • 发挥理性分析，同时关注他人感受")
    else:
        print("  • 发挥共情能力，同时保持理性")
    
    if result['type'][3] == 'J':
        print("  • 发挥计划能力，同时保持灵活性")
    else:
        print("  • 发挥适应能力，同时适当规划")

def print_suggestion(feature: str):
    """打印心理暗示"""
    suggestion = get_suggestion(feature)
    
    if not suggestion:
        print(f"\n❌ 未找到 '{feature}' 的心理暗示")
        return
    
    print("\n" + "="*60)
    print("✨ 面相心理暗示")
    print("="*60)
    
    print(f"\n🎯 特征: {feature}")
    print(f"🔄 转化解读: {suggestion['reframe']}")
    
    print("\n🌅 晨间暗示:")
    print(f"  \"{suggestion['morning']}\"")
    
    print("\n⚡ 挑战应对暗示:")
    print(f"  \"{suggestion['challenge']}\"")
    
    print("\n📝 配套行动:")
    for i, action in enumerate(suggestion['action'], 1):
        print(f"  {i}. {action}")
    
    print("\n💡 使用建议:")
    print("  • 每天早上朗读晨间暗示")
    print("  • 遇到困难时默念挑战暗示")
    print("  • 坚持配套行动至少21天")

def print_emotion_analysis(complexion: str):
    """打印情绪-面色分析"""
    result = analyze_emotion_complexion(complexion)
    
    if not result:
        print(f"\n❌ 未找到 '{complexion}' 的情绪分析")
        return
    
    print("\n" + "="*60)
    print("😊😰 情绪-面色关联分析")
    print("="*60)
    
    print(f"\n🎨 面色: {complexion}")
    print(f"💭 情绪状态: {result['emotion']}")
    
    if 'positive' in result:
        print(f"\n✅ 积极解读: {result['positive']}")
    if 'negative' in result:
        print(f"⚠️  需注意: {result['negative']}")
    if 'psychology' in result:
        print(f"🧠 心理机制: {result['psychology']}")
    
    print("\n💡 调节建议:")
    for i, advice in enumerate(result['advice'], 1):
        print(f"  {i}. {advice}")

def main():
    if len(sys.argv) < 2:
        print("""
用法:
    python psychology_analysis.py [面部特征]     # 综合心理分析
    python psychology_analysis.py --mbti "特征"  # MBTI性格分析
    python psychology_analysis.py --suggestion "特征"  # 心理暗示
    python psychology_analysis.py --emotion "面色"   # 情绪-面色分析

示例:
    python psychology_analysis.py "眉毛浓密 额头高广 颧骨高"
    python psychology_analysis.py --mbti "眉毛浓密 眼睛有神 下巴方圆"
    python psychology_analysis.py --suggestion "鼻子塌"
    python psychology_analysis.py --emotion "面色发黄"
        """)
        return
    
    arg = sys.argv[1]
    
    if arg == "--mbti" and len(sys.argv) > 2:
        features = sys.argv[2].split()
        print_mbti_analysis(features)
    elif arg == "--suggestion" and len(sys.argv) > 2:
        print_suggestion(sys.argv[2])
    elif arg == "--emotion" and len(sys.argv) > 2:
        print_emotion_analysis(sys.argv[2])
    else:
        # 综合心理分析
        features = arg.split()
        print("\n" + "="*60)
        print("🔮 面相玄学心理综合分析")
        print("="*60)
        print_mbti_analysis(features)
        
        print("\n" + "-"*60)
        print("\n✨ 心理暗示建议:")
        for feature in features[:3]:
            suggestion = get_suggestion(feature)
            if suggestion:
                print(f"\n  【{feature}】")
                print(f"  暗示: {suggestion['morning'][:50]}...")

if __name__ == "__main__":
    main()
