#!/usr/bin/env python3
"""
高考作文诊断评分工具
功能：对已有作文进行多维度诊断，输出评分预测和改进建议
用法：python diagnose.py --essay "作文内容" 或 python diagnose.py --file 作文文件路径
"""

import argparse
import io
import json
import re
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

MAX_INPUT_LENGTH = 100000


def count_chars(text):
    """统计有效字符数（排除空格和标点）"""
    chinese_chars = re.findall(r'[一-鿿]', text)
    return len(chinese_chars)


def count_paragraphs(text):
    """统计段落数"""
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    return len(paragraphs)


def check_title(text):
    """检查是否有标题"""
    lines = text.strip().split('\n')
    if not lines:
        return False, ""
    first_line = lines[0].strip()
    if len(first_line) <= 20 and not first_line.startswith('　') and not first_line.startswith('  '):
        return True, first_line
    return False, ""


def check_word_count(text):
    """检查字数并计算扣分"""
    char_count = count_chars(text)
    deduction = 0
    if char_count < 800:
        shortage = 800 - char_count
        deduction = (shortage + 49) // 50
    return char_count, deduction


def check_application_format(text):
    """检查应用文体格式"""
    issues = []

    if any(kw in text for kw in ['大家好', '谢谢大家', '我的发言']):
        if '尊敬的' not in text and '亲爱的' not in text:
            issues.append("演讲稿/发言稿缺少称呼语（如'尊敬的XX'）")
        if '大家好' not in text:
            issues.append("演讲稿/发言稿缺少问候语'大家好'")
        if '谢谢大家' not in text and '我的发言' not in text:
            issues.append("演讲稿/发言稿缺少结束语")

    if '倡议' in text:
        if '此致' not in text:
            issues.append("倡议书建议添加'此致敬礼'")
        has_date = re.search(r'\d{4}年\d{1,2}月\d{1,2}日', text)
        if not has_date:
            issues.append("倡议书缺少落款日期")

    if any(kw in text for kw in ['您好', '此致', '敬礼']):
        if '尊敬的' not in text and '亲爱的' not in text:
            issues.append("书信缺少称呼")
        if '此致' not in text:
            issues.append("书信缺少'此致'")
        if '敬礼' not in text:
            issues.append("书信缺少'敬礼'")

    return issues


def analyze_structure(text):
    """分析文章结构"""
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    total = len(paragraphs)
    analysis = {
        "total_paragraphs": total,
        "has_opening": False,
        "has_body": False,
        "has_closing": False,
        "body_paragraphs": 0,
        "issues": []
    }

    if total < 3:
        analysis["issues"].append("段落过少，文章结构不完整")
        return analysis

    analysis["has_opening"] = True
    analysis["has_closing"] = True
    analysis["body_paragraphs"] = max(0, total - 2)
    analysis["has_body"] = analysis["body_paragraphs"] >= 2

    if analysis["body_paragraphs"] < 2:
        analysis["issues"].append("主体段落不足，建议至少2-3个主体段落")

    if analysis["body_paragraphs"] > 6:
        analysis["issues"].append("主体段落过多，可能论述不够充分，建议合并精简")

    transition_words = ['然而', '但是', '不过', '因此', '所以', '总之', '综上',
                        '首先', '其次', '再次', '最后', '一方面', '另一方面',
                        '不仅如此', '更重要的是', '与此同时', '换言之']
    transition_count = sum(text.count(w) for w in transition_words)
    char_count = count_chars(text)
    if char_count > 0:
        transition_density = transition_count / (char_count / 100)
        if transition_density < 2:
            analysis["issues"].append(f"过渡连接词偏少（约{transition_density:.1f}个/百字），建议≥3个/百字以增强逻辑连贯性")

    return analysis


def analyze_language(text):
    """分析语言表达（五维度全覆盖）"""
    issues = []
    suggestions = []
    dimensions = {}

    # 维度1：空泛表达检测
    hollow_patterns = [
        r'我们要[一-鿿]{2,6}',
        r'我们应该[一-鿿]{2,6}',
        r'我们必须[一-鿿]{2,6}',
        r'让我们[一-鿿]{2,6}',
        r'只有这样.{0,5}才能',
        r'综上所述.{0,10}因此',
    ]
    hollow_count = sum(len(re.findall(p, text)) for p in hollow_patterns)

    slogans = ['不忘初心', '砥砺前行', '牢记使命', '奋勇前进',
               '众志成城', '凝心聚力', '携手共进', '共创辉煌']
    slogan_count = sum(text.count(s) for s in slogans)

    hollow_total = hollow_count + slogan_count
    char_count = count_chars(text)
    hollow_ratio = hollow_total / max(1, char_count / 100)

    if hollow_ratio > 3:
        issues.append("空泛表达过多：口号套话密度过高，缺乏具体论述和个人思考")
        dimensions["空泛表达"] = "严重"
    elif hollow_ratio > 1.5:
        suggestions.append("存在较多空泛表达（如'我们要/应该...'句式、口号套话），建议用具体论据和分析替代")
        dimensions["空泛表达"] = "中等"
    else:
        dimensions["空泛表达"] = "良好"

    # 维度2：口语化问题检测
    oral_patterns = [
        (r'很[好大多少强弱高低长短快慢难易]', "使用'很+形容词'结构"),
        (r'[的时候]{3}', "使用'的时候'口语化连词"),
        (r'然后.{0,5}然后', "重复使用'然后'"),
        (r'就是说', "使用口语化表达'就是说'"),
        (r'其实吧', "使用口语化表达'其实吧'"),
        (r'不要放弃', "使用口语化表达'不要放弃'，可改为'坚守/坚持'"),
        (r'想办法', "使用口语化表达'想办法'，可改为'谋策/探寻路径'"),
        (r'这样的话', "使用口语化连词'这样的话'"),
        (r'说实话', "使用口语化表达'说实话'"),
        (r'反正', "使用口语化表达'反正'"),
    ]
    oral_issues = []
    oral_count = 0
    for pattern, desc in oral_patterns:
        matches = re.findall(pattern, text)
        if matches:
            oral_count += len(matches)
            oral_issues.append(desc)

    if oral_count > 5:
        issues.append(f"口语化问题严重：{'; '.join(oral_issues[:3])}等，缺乏书面语的凝练与正式感")
        dimensions["口语化问题"] = "严重"
    elif oral_count > 2:
        suggestions.append(f"存在口语化倾向：{'; '.join(oral_issues[:2])}，建议改用更凝练的书面表达")
        dimensions["口语化问题"] = "中等"
    else:
        dimensions["口语化问题"] = "良好"

    # 维度3：句式单一检测
    sentences = re.split(r'[。！？]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]

    if len(sentences) >= 5:
        lengths = [len(s) for s in sentences]
        avg_len = sum(lengths) / len(lengths)
        variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)

        same_start_count = 0
        for i in range(1, len(sentences)):
            if len(sentences[i]) >= 2 and len(sentences[i-1]) >= 2:
                if sentences[i][:2] == sentences[i-1][:2]:
                    same_start_count += 1

        same_start_ratio = same_start_count / max(1, len(sentences) - 1)

        if variance < 20 and same_start_ratio > 0.3:
            issues.append("句式严重单一：句子长度雷同且开头重复，缺乏长短交替和节奏变化")
            dimensions["句式单一"] = "严重"
        elif variance < 50 or same_start_ratio > 0.2:
            suggestions.append("句式变化不足：建议交替使用长句与短句，变换句子开头方式，增强阅读节奏感")
            dimensions["句式单一"] = "中等"
        else:
            dimensions["句式单一"] = "良好"
    else:
        dimensions["句式单一"] = "无法判断（句子过少）"

    # 维度4：修辞缺失检测
    rhetoric_marks = 0
    rhetoric_marks += len(re.findall(r'如同|像是|仿佛|犹如|好似|宛如|恰似', text))
    rhetoric_marks += len(re.findall(r'像[一-鿿]{1,10}一样', text))

    parallelism = 0
    for i in range(len(sentences) - 2):
        if len(sentences[i]) > 5 and abs(len(sentences[i]) - len(sentences[i+1])) <= 3:
            if abs(len(sentences[i+1]) - len(sentences[i+2])) <= 3:
                parallelism += 1

    rhetoric_total = rhetoric_marks + parallelism
    if rhetoric_total < 1:
        issues.append("修辞手法严重缺失：全文无比喻、排比等修辞，语言平淡缺乏感染力")
        dimensions["修辞缺失"] = "严重"
    elif rhetoric_total < 3:
        suggestions.append("修辞手法偏少：建议适当运用比喻（化抽象为具象）、排比（增强气势）等修辞增强文采")
        dimensions["修辞缺失"] = "中等"
    else:
        dimensions["修辞缺失"] = "良好"

    # 维度5：逻辑跳跃检测
    logic_connectors = ['因为', '所以', '因此', '于是', '故而', '由此可见',
                        '换言之', '也就是说', '这说明', '可见']
    connector_count = sum(text.count(w) for w in logic_connectors)

    paragraphs = [p.strip() for p in text.split('\n') if len(p.strip()) > 10]
    jump_count = 0
    for i in range(1, len(paragraphs)):
        has_transition = any(paragraphs[i].startswith(w) or w in paragraphs[i][:20]
                           for w in ['然而', '但是', '因此', '所以', '同时', '此外',
                                    '不仅如此', '更重要的是', '与此同时', '相反',
                                    '由此', '正因如此', '诚然', '固然'])
        if not has_transition:
            jump_count += 1

    if len(paragraphs) > 3:
        jump_ratio = jump_count / (len(paragraphs) - 1)
        if jump_ratio > 0.7 and connector_count < 2:
            issues.append("逻辑跳跃明显：段落间缺少过渡衔接，句与句之间存在逻辑断裂")
            dimensions["逻辑跳跃"] = "严重"
        elif jump_ratio > 0.5 or connector_count < 3:
            suggestions.append("逻辑衔接可加强：部分段落间缺少过渡词/过渡句，建议增强论证的连贯性")
            dimensions["逻辑跳跃"] = "中等"
        else:
            dimensions["逻辑跳跃"] = "良好"
    else:
        dimensions["逻辑跳跃"] = "无法判断（段落过少）"

    # 附加检测：名言引用
    quote_patterns = [r'"[^"]{5,30}"', r'「[^」]{5,30}」', r'——.*?[。，]', r'古人云', r'正如.*?所说']
    quote_count = sum(len(re.findall(p, text)) for p in quote_patterns)
    if quote_count < 1:
        suggestions.append("缺少名言引用，建议引用1-2处贴切的名言增强说服力和文化底蕴")
    elif quote_count > 5:
        issues.append("名言引用过多，可能显得堆砌，建议控制在2-3处")

    return issues, suggestions, dimensions


def score_essay(text, topic=""):
    """综合评分"""
    result = {
        "题目": topic if topic else "未指定",
        "字数诊断": {},
        "标题诊断": {},
        "结构诊断": {},
        "格式诊断": {},
        "语言诊断": {},
        "扣分汇总": {},
        "改进建议": [],
        "预估分数": {}
    }

    # 1. 字数诊断
    char_count, word_deduction = check_word_count(text)
    result["字数诊断"] = {
        "有效字数": char_count,
        "是否达标": char_count >= 800,
        "扣分": word_deduction
    }
    if char_count < 800:
        result["改进建议"].append(f"字数不足！当前{char_count}字，距800字还差{800-char_count}字，将扣{word_deduction}分")

    # 2. 标题诊断
    has_title, title = check_title(text)
    result["标题诊断"] = {
        "是否有标题": has_title,
        "标题": title if has_title else "未检测到",
        "扣分": 2 if not has_title else 0
    }
    if not has_title:
        result["改进建议"].append("缺少标题，将扣2分！请添加一个精准提炼材料内核的标题")

    # 3. 结构诊断
    structure = analyze_structure(text)
    result["结构诊断"] = {
        "总段落数": structure["total_paragraphs"],
        "主体段落数": structure["body_paragraphs"],
        "问题": structure["issues"]
    }
    for issue in structure["issues"]:
        result["改进建议"].append(f"结构问题：{issue}")

    # 4. 格式诊断（应用文体）
    format_issues = check_application_format(text)
    result["格式诊断"] = {"问题": format_issues}
    for issue in format_issues:
        result["改进建议"].append(f"格式问题：{issue}")

    # 5. 语言诊断（五维度）
    lang_issues, lang_suggestions, lang_dimensions = analyze_language(text)
    result["语言诊断"] = {
        "五维度评估": lang_dimensions,
        "问题": lang_issues,
        "建议": lang_suggestions
    }
    for issue in lang_issues:
        result["改进建议"].append(f"语言问题：{issue}")
    for suggestion in lang_suggestions:
        result["改进建议"].append(f"语言建议：{suggestion}")

    # 6. 扣分汇总
    total_deduction = word_deduction + (2 if not has_title else 0)
    result["扣分汇总"] = {
        "字数扣分": word_deduction,
        "标题扣分": 2 if not has_title else 0,
        "总扣分": total_deduction
    }

    # 7. 预估分数
    base_score = 45
    adjustments = 0

    if char_count >= 800:
        adjustments += 2
    else:
        adjustments -= 5

    if structure["body_paragraphs"] >= 3:
        adjustments += 2
    elif structure["body_paragraphs"] < 2:
        adjustments -= 3

    if has_title:
        adjustments += 1

    transition_words = ['然而', '但是', '因此', '所以', '首先', '其次', '再次', '最后']
    transition_count = sum(text.count(w) for w in transition_words)
    if transition_count >= 5:
        adjustments += 2

    # 语言质量调整
    severe_dims = sum(1 for v in lang_dimensions.values() if v == "严重")
    good_dims = sum(1 for v in lang_dimensions.values() if v == "良好")
    if severe_dims >= 3:
        adjustments -= 4
    elif severe_dims >= 2:
        adjustments -= 2
    if good_dims >= 4:
        adjustments += 3
    elif good_dims >= 3:
        adjustments += 1

    estimated = max(20, min(60, base_score + adjustments - total_deduction))

    if estimated >= 55:
        level = "一类文（55-60分）"
    elif estimated >= 50:
        level = "二类上文（50-54分）"
    elif estimated >= 46:
        level = "二类下文（46-49分）"
    elif estimated >= 42:
        level = "三类上文（42-45分）"
    elif estimated >= 36:
        level = "四类文（36-41分）"
    else:
        level = "五类文（35分以下）"

    result["预估分数"] = {
        "预估分": estimated,
        "等级": level,
        "说明": "此为基于可量化指标的初步预估，实际分数需结合立意深度、思辨水平、文采等主观维度综合评判"
    }

    return result


def main():
    parser = argparse.ArgumentParser(description='高考作文诊断评分工具')
    parser.add_argument('--essay', type=str, help='作文内容（直接输入）')
    parser.add_argument('--file', type=str, help='作文文件路径')
    parser.add_argument('--topic', type=str, default='', help='作文题目（可选）')
    parser.add_argument('--json', action='store_true', help='以JSON格式输出')
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                essay_text = f.read()
        except FileNotFoundError:
            print(f"错误：文件不存在 - {args.file}")
            sys.exit(1)
        except PermissionError:
            print(f"错误：无权限读取文件 - {args.file}")
            sys.exit(1)
        except UnicodeDecodeError:
            print(f"错误：文件编码不是UTF-8，请转换编码后重试 - {args.file}")
            sys.exit(1)
    elif args.essay:
        essay_text = args.essay
    else:
        print("错误：请提供作文内容(--essay)或文件路径(--file)")
        sys.exit(1)

    if not essay_text.strip():
        print("错误：作文内容为空，请提供有效内容")
        sys.exit(1)

    if len(essay_text) > MAX_INPUT_LENGTH:
        print(f"错误：输入内容超过上限（{MAX_INPUT_LENGTH}字符），请检查输入")
        sys.exit(1)

    result = score_essay(essay_text, args.topic)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 50)
        print("       高考作文诊断报告")
        print("=" * 50)

        if args.topic:
            print(f"\n题目：{args.topic}")

        # 字数
        wd = result["字数诊断"]
        status = "达标" if wd['是否达标'] else "不足"
        print(f"\n【字数诊断】有效字数 {wd['有效字数']} 字 [{status}]")
        if wd['扣分'] > 0:
            print(f"   扣分：-{wd['扣分']}分")

        # 标题
        td = result["标题诊断"]
        print(f"\n【标题诊断】{'有标题: ' + td['标题'] if td['是否有标题'] else '缺少标题'}")
        if td['扣分'] > 0:
            print(f"   扣分：-{td['扣分']}分")

        # 结构
        sd = result["结构诊断"]
        print(f"\n【结构诊断】总段落 {sd['总段落数']} 段，主体段落 {sd['主体段落数']} 段")
        for issue in sd["问题"]:
            print(f"   ! {issue}")

        # 格式
        fd = result["格式诊断"]
        if fd["问题"]:
            print(f"\n【格式诊断】")
            for issue in fd["问题"]:
                print(f"   ! {issue}")

        # 语言（五维度）
        ld = result["语言诊断"]
        print(f"\n【语言诊断 - 五维度评估】")
        for dim, status in ld["五维度评估"].items():
            indicator = "[!]" if status == "严重" else "[~]" if status == "中等" else "[OK]"
            print(f"   {indicator} {dim}：{status}")
        if ld["问题"]:
            print("   ------")
            for issue in ld["问题"]:
                print(f"   ! {issue}")
        if ld["建议"]:
            for suggestion in ld["建议"]:
                print(f"   > {suggestion}")

        # 扣分汇总
        dd = result["扣分汇总"]
        print(f"\n【扣分汇总】字数-{dd['字数扣分']} + 标题-{dd['标题扣分']} = 总扣{dd['总扣分']}分")

        # 预估分数
        es = result["预估分数"]
        print(f"\n【预估分数】{es['预估分']} 分 — {es['等级']}")
        print(f"   说明：{es['说明']}")

        # 改进建议
        if result["改进建议"]:
            print(f"\n【改进建议】")
            for i, suggestion in enumerate(result["改进建议"], 1):
                print(f"   {i}. {suggestion}")

        print("\n" + "=" * 50)


if __name__ == '__main__':
    main()
