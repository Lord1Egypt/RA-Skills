#!/usr/bin/env python3
"""
高考作文结构框架生成工具
功能：根据题目和立意，生成文章结构框架
用法：python structure.py --topic "题目" --thesis "立意" --type "递进|并列|对比" --format "议论文|演讲稿|倡议书|辩论稿|书信"
"""

import argparse
import io
import json
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 结构模板
TEMPLATES = {
    "递进式": {
        "议论文": {
            "name": "递进式议论文",
            "description": "是什么→为什么→怎么办，层层深入",
            "sections": [
                {"name": "开头", "ratio": "15%", "content": "引述材料，提炼核心矛盾，亮明观点", "tips": "用设问/场景描写/名言引用制造张力，观点句要鲜明果断"},
                {"name": "是什么", "ratio": "20%", "content": "界定核心概念内涵，明确讨论范围", "tips": "对材料关键词做概念阐释，建立论述基点"},
                {"name": "为什么", "ratio": "30%", "content": "分析原因、意义、价值，这是论证主体", "tips": "分2-3层递进论证，每层=论点句+论据+分析句，注意过渡"},
                {"name": "怎么办", "ratio": "20%", "content": "提出路径、方法、对策", "tips": "结合当代青年身份，给出可操作的思考方向"},
                {"name": "结尾", "ratio": "15%", "content": "升华主题，回扣材料和观点", "tips": "关联时代背景，用金句收束，避免简单重复开头"}
            ]
        },
        "演讲稿": {
            "name": "递进式演讲稿",
            "description": "是什么→为什么→怎么办，口语化表达",
            "sections": [
                {"name": "开场", "ratio": "10%", "content": "称呼+问候+引入主题", "tips": "尊敬的XX，亲爱的XX：大家好！用设问或故事开场，拉近与听众距离"},
                {"name": "是什么", "ratio": "15%", "content": "界定核心概念，明确讨论范围", "tips": "口语化表达，可用'大家想一想'等互动句"},
                {"name": "为什么", "ratio": "35%", "content": "分析原因、意义，这是演讲主体", "tips": "融入个人经历增强感染力，用排比增强气势"},
                {"name": "怎么办", "ratio": "25%", "content": "提出行动方向和方法", "tips": "结合'我们'的身份，发出号召，增强现场感"},
                {"name": "结尾", "ratio": "15%", "content": "升华+号召+致谢", "tips": "以金句或排比收束，'让我们……！谢谢大家！'"}
            ]
        }
    },
    "并列式": {
        "议论文": {
            "name": "并列式议论文",
            "description": "多角度并列展开，每个分论点独立支撑总论点",
            "sections": [
                {"name": "开头", "ratio": "15%", "content": "引述材料，亮明总论点", "tips": "总论点要能涵盖所有分论点"},
                {"name": "分论点一", "ratio": "20%", "content": "从角度A论证", "tips": "论点句+论据+分析句，段落结尾回扣总论点"},
                {"name": "分论点二", "ratio": "20%", "content": "从角度B论证", "tips": "与分论点一有逻辑关联（如递进、互补），不是简单重复"},
                {"name": "分论点三", "ratio": "20%", "content": "从角度C论证", "tips": "三个角度最好有递进关系：个人→社会→时代"},
                {"name": "结尾", "ratio": "15%", "content": "归纳三个分论点，升华总论点", "tips": "不能简单重复，要有所升华和拓展"}
            ]
        },
        "演讲稿": {
            "name": "并列式演讲稿",
            "description": "多角度并列展开，口语化互动表达",
            "sections": [
                {"name": "开场", "ratio": "10%", "content": "称呼+问候+引入主题，亮明总论点", "tips": "尊敬的XX，亲爱的XX：大家好！用提问或故事引出主题"},
                {"name": "角度一", "ratio": "25%", "content": "从第一个角度展开论证", "tips": "口语化表达，可用'让我先说第一点'等过渡，融入个人经历"},
                {"name": "角度二", "ratio": "25%", "content": "从第二个角度展开论证", "tips": "用'接下来/同样重要的是'过渡，与角度一形成互补"},
                {"name": "角度三", "ratio": "25%", "content": "从第三个角度展开论证", "tips": "用'更进一步说'过渡，升华到更高层面"},
                {"name": "结尾", "ratio": "15%", "content": "归纳总结+号召行动+致谢", "tips": "以排比收束，发出号召，'让我们……！谢谢大家！'"}
            ]
        },
        "倡议书": {
            "name": "并列式倡议书",
            "description": "多条倡议并列展开，措施具体可操作",
            "sections": [
                {"name": "标题与称呼", "ratio": "5%", "content": "标题+称呼", "tips": "标题简洁明确，称呼顶格写"},
                {"name": "背景与理由", "ratio": "20%", "content": "说明为什么发起倡议，阐述背景和必要性", "tips": "结合现实问题，让读者认同倡议的意义"},
                {"name": "倡议一", "ratio": "20%", "content": "第一条具体倡议措施", "tips": "措施要具体可操作，不能空泛"},
                {"name": "倡议二", "ratio": "20%", "content": "第二条具体倡议措施", "tips": "与第一条形成互补，覆盖不同方面"},
                {"name": "倡议三", "ratio": "20%", "content": "第三条具体倡议措施", "tips": "可从精神层面升华"},
                {"name": "结尾与落款", "ratio": "15%", "content": "号召+署名+日期", "tips": "'让我们……！' 落款写倡议人和日期"}
            ]
        },
        "书信": {
            "name": "并列式书信",
            "description": "多角度并列阐述观点或建议",
            "sections": [
                {"name": "称呼与问候", "ratio": "5%", "content": "称呼+您好", "tips": "称呼顶格，正文空两格"},
                {"name": "引入主题", "ratio": "15%", "content": "说明写信目的，引出核心话题", "tips": "简洁点明缘由，自然过渡到正文"},
                {"name": "观点/建议一", "ratio": "25%", "content": "从第一个角度阐述", "tips": "论点+论据+分析，语气得体"},
                {"name": "观点/建议二", "ratio": "25%", "content": "从第二个角度阐述", "tips": "与第一点互补，增强说服力"},
                {"name": "观点/建议三", "ratio": "15%", "content": "从第三个角度阐述或总结升华", "tips": "可适当升华到更高层面"},
                {"name": "结尾与落款", "ratio": "15%", "content": "总结+祝愿+此致敬礼+署名+日期", "tips": "此致空两格，敬礼顶格，落款写姓名和日期"}
            ]
        }
    },
    "对比式": {
        "议论文": {
            "name": "对比式议论文",
            "description": "正反对比论证，突出观点正确性",
            "sections": [
                {"name": "开头", "ratio": "15%", "content": "引述材料，亮明观点", "tips": "观点要鲜明，为正反对比做好铺垫"},
                {"name": "正面论证", "ratio": "25%", "content": "正面事例+分析，证明观点的正确性", "tips": "事例要典型，分析要深入揭示本质"},
                {"name": "反面论证", "ratio": "25%", "content": "反面事例+分析，证明偏离观点的危害", "tips": "反面事例与正面形成鲜明对比，分析危害和原因"},
                {"name": "辩证综合", "ratio": "20%", "content": "正反对比提炼规律，辩证分析", "tips": "不能简单说'所以要XX'，要提炼出深层规律"},
                {"name": "结尾", "ratio": "15%", "content": "总结升华，回扣材料", "tips": "关联时代，以金句收束"}
            ]
        },
        "演讲稿": {
            "name": "对比式演讲稿",
            "description": "正反对比论证，口语化增强说服力",
            "sections": [
                {"name": "开场", "ratio": "10%", "content": "称呼+问候+引入话题", "tips": "尊敬的XX，亲爱的XX：大家好！用对比性问题开场引发思考"},
                {"name": "正面论证", "ratio": "30%", "content": "正面典型事例+分析启示", "tips": "融入感染力，用'让我们看看XX'等互动句，引发共鸣"},
                {"name": "反面论证", "ratio": "25%", "content": "反面事例+危害分析", "tips": "用'然而/相反'过渡，语气可适当加重，引发警醒"},
                {"name": "辩证升华", "ratio": "20%", "content": "正反对比提炼规律，回归主题", "tips": "从对比中总结规律，联系听众自身"},
                {"name": "结尾", "ratio": "15%", "content": "号召行动+致谢", "tips": "以金句收束，发出号召，'谢谢大家！'"}
            ]
        },
        "辩论稿": {
            "name": "对比式辩论稿",
            "description": "正反立论，破立结合",
            "sections": [
                {"name": "开场与立论", "ratio": "15%", "content": "称呼+问候+明确我方观点", "tips": "尊敬的主席，各位辩友：大家好！开篇明确'我方的观点是……'"},
                {"name": "正面立论", "ratio": "30%", "content": "我方观点的正面论证，用事例和道理证明", "tips": "分2-3层递进论证，每层论据有力"},
                {"name": "驳斥对方", "ratio": "25%", "content": "预设对方观点并逐一反驳", "tips": "用'对方可能会说……但是……'句式，逻辑严密"},
                {"name": "辩证总结", "ratio": "15%", "content": "综合正反，升华观点", "tips": "从更高维度整合正反两面，展示思辨深度"},
                {"name": "结尾", "ratio": "15%", "content": "重申观点+致谢", "tips": "'综上所述，我方坚持认为……谢谢大家！'"}
            ]
        },
        "书信": {
            "name": "对比式书信",
            "description": "正反对比阐述观点，增强说服力",
            "sections": [
                {"name": "称呼与问候", "ratio": "5%", "content": "称呼+您好", "tips": "称呼顶格，正文空两格"},
                {"name": "引入话题", "ratio": "15%", "content": "说明写信目的，引出要讨论的问题", "tips": "简洁明了，自然过渡"},
                {"name": "正面阐述", "ratio": "25%", "content": "从正面论证观点，举例说明益处", "tips": "语气诚恳，论据贴切"},
                {"name": "反面警示", "ratio": "25%", "content": "从反面说明不这样做的后果或危害", "tips": "用'反观/相反'过渡，形成鲜明对比"},
                {"name": "建议总结", "ratio": "15%", "content": "综合正反给出建议或期望", "tips": "态度诚恳，不居高临下"},
                {"name": "结尾与落款", "ratio": "15%", "content": "祝愿+此致敬礼+署名+日期", "tips": "此致空两格，敬礼顶格"}
            ]
        }
    }
}

# 应用文体完整模板
FORMAT_TEMPLATES = {
    "演讲稿": {
        "opening": "尊敬的XX，亲爱的XX：\n大家好！",
        "closing": "我的演讲（发言）完毕，谢谢大家！",
        "tips": ["称呼顶格写", "问候语空两格", "正文口语化，有互动感", "结尾标准致谢"]
    },
    "倡议书": {
        "opening": "尊敬的XX：\n……（倡议背景）\n为此，我们倡议：",
        "closing": "让我们……！\n\n倡议人：XX\nXXXX年XX月XX日",
        "tips": ["背景要写清为什么倡议", "措施要具体可操作", "结尾要有号召力", "落款写倡议人和日期"]
    },
    "辩论稿": {
        "opening": "尊敬的主席，各位辩友，观众：\n大家好！\n我今天是正（反）方代表，我方的观点是……",
        "closing": "综上所述，我方坚持认为……\n我的发言到此结束，谢谢主席，谢谢评委，谢谢对方辩友！",
        "tips": ["开头必须明确表明立场", "论证分层：首先/其次/再次", "可以预设对方观点进行反驳", "结尾重申观点"]
    },
    "书信": {
        "opening": "尊敬的XX：\n您好！",
        "closing": "此致\n敬礼！\n\nXX\nXXXX年XX月XX日",
        "tips": ["称呼顶格", "正文每段空两格", "此致空两格，敬礼顶格", "落款写姓名和日期"]
    }
}


def generate_structure(topic, thesis, struct_type, essay_format):
    """生成文章结构框架"""
    result = {
        "题目": topic,
        "立意": thesis,
        "结构类型": struct_type,
        "文体": essay_format,
        "框架": None,
        "应用文体格式": None,
        "写作提示": []
    }

    # 获取结构模板
    if struct_type in TEMPLATES:
        if essay_format in TEMPLATES[struct_type]:
            result["框架"] = TEMPLATES[struct_type][essay_format]
        elif "议论文" in TEMPLATES[struct_type]:
            # 降级到议论文模板
            result["框架"] = TEMPLATES[struct_type]["议论文"]
            result["写作提示"].append(f"当前结构类型无'{essay_format}'专用模板，已使用议论文模板，请根据文体要求调整语言风格")

    if result["框架"] is None:
        # 默认使用递进式议论文
        result["框架"] = TEMPLATES["递进式"]["议论文"]
        result["写作提示"].append("已使用默认递进式议论文模板")

    # 应用文体格式
    if essay_format in FORMAT_TEMPLATES:
        result["应用文体格式"] = FORMAT_TEMPLATES[essay_format]

    # 通用写作提示
    result["写作提示"].extend([
        "每段遵循'论点句+论据+分析句'的黄金三角",
        "段间使用过渡词/过渡句确保逻辑连贯",
        "论据选择贴切的事例，避免堆砌",
        "结尾要回扣材料，不能另起炉灶"
    ])

    return result


def main():
    parser = argparse.ArgumentParser(description='高考作文结构框架生成工具')
    parser.add_argument('--topic', type=str, required=True, help='作文题目')
    parser.add_argument('--thesis', type=str, required=True, help='立意/核心观点')
    parser.add_argument('--type', type=str, default='递进式',
                        choices=['递进式', '并列式', '对比式'], help='结构类型')
    parser.add_argument('--format', type=str, default='议论文',
                        choices=['议论文', '演讲稿', '倡议书', '辩论稿', '书信'],
                        help='文体格式')
    parser.add_argument('--json', action='store_true', help='以JSON格式输出')
    args = parser.parse_args()

    result = generate_structure(args.topic, args.thesis, args.type, args.format)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 50)
        print("       高考作文结构框架")
        print("=" * 50)
        print(f"\n📌 题目：{result['题目']}")
        print(f"🎯 立意：{result['立意']}")
        print(f"📐 结构：{result['结构类型']} · {result['文体']}")

        framework = result["框架"]
        print(f"\n📖 {framework['name']}（{framework['description']}）\n")

        for i, section in enumerate(framework["sections"], 1):
            print(f"  第{i}部分：{section['name']}（{section['ratio']}）")
            print(f"    📝 内容：{section['content']}")
            print(f"    💡 提示：{section['tips']}")
            print()

        if result["应用文体格式"]:
            fmt = result["应用文体格式"]
            print("📝 应用文体格式要求：")
            print(f"  开头格式：{fmt['opening']}")
            print(f"  结尾格式：{fmt['closing']}")
            print(f"  注意事项：")
            for tip in fmt["tips"]:
                print(f"    · {tip}")
            print()

        print("🔑 通用写作提示：")
        for tip in result["写作提示"]:
            print(f"  · {tip}")

        print("\n" + "=" * 50)


if __name__ == '__main__':
    main()
