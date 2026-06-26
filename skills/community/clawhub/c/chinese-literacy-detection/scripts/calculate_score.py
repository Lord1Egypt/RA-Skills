#!/usr/bin/env python3
"""
识字量分数计算与验证工具

输入各层级测试结果，计算加权识字量 W 值并输出详细报告。
可用于：
1. 开发时验证计算逻辑的正确性
2. 对已有测试结果进行复盘
3. 模拟不同测试场景的预期结果

用法:
    # 交互式输入
    python calculate_score.py

    # 从 JSON 文件加载测试结果
    python calculate_score.py --input results.json

    # 快速模拟：指定各层级认识数
    python calculate_score.py --known 48 40 20 10 3 1

    # 模拟熔断场景：L3 第 8 个字触发熔断，已知 1 个
    python calculate_score.py --known 50 40 1 0 0 0 --fuse-level 3 --fuse-tested 8

    # 输出 JSON 格式
    python calculate_score.py --known 48 40 20 10 3 1 --format json
"""

import json
import argparse
import sys


# ============================================================
# 六层分级配置（与 SKILL.md 保持完全一致）
# ============================================================
LEVEL_CONFIGS = [
    {"level": 1, "name": "核心字", "rankStart": 1,    "rankEnd": 50,   "testCount": 50,  "weight": 1,   "totalChars": 50},
    {"level": 2, "name": "常用字", "rankStart": 51,   "rankEnd": 200,  "testCount": 50,  "weight": 3,   "totalChars": 150},
    {"level": 3, "name": "扩展字", "rankStart": 201,  "rankEnd": 500,  "testCount": 30,  "weight": 10,  "totalChars": 300},
    {"level": 4, "name": "进阶字", "rankStart": 501,  "rankEnd": 1000, "testCount": 25,  "weight": 20,  "totalChars": 500},
    {"level": 5, "name": "提高字", "rankStart": 1001, "rankEnd": 1500, "testCount": 10,  "weight": 50,  "totalChars": 500},
    {"level": 6, "name": "拓展字", "rankStart": 1501, "rankEnd": 2500, "testCount": 10,  "weight": 100, "totalChars": 1000},
]

# 年龄参考表
AGE_REFERENCE = [
    {"age": "3-4岁",  "min": 50,   "max": 200,  "stage": "启蒙期"},
    {"age": "4-5岁",  "min": 200,  "max": 500,  "stage": "兴趣培养期"},
    {"age": "5-6岁",  "min": 500,  "max": 800,  "stage": "入学准备期"},
    {"age": "6-7岁",  "min": 800,  "max": 1200, "stage": "一年级水平"},
    {"age": "7-8岁",  "min": 1200, "max": 1600, "stage": "二年级水平"},
    {"age": "8-9岁",  "min": 1600, "max": 2000, "stage": "三年级水平"},
    {"age": "9-10岁", "min": 2000, "max": 2500, "stage": "四年级水平"},
    {"age": "10-12岁","min": 2500, "max": 2500, "stage": "五年级及以上水平"},
]


def calculate_score(level_results, fuse_level=None, fuse_tested=None):
    """
    计算加权识字量。
    
    Args:
        level_results: 各层级结果列表，每项包含 {level, known, tested}
        fuse_level: 熔断层级（None 表示未熔断）
        fuse_tested: 熔断层级已测字数（仅在 fuse_level 设置时有效）
    
    Returns:
        dict: 包含 W 值、各层级详情等完整计算结果
    """
    results = []
    total_vocabulary = 0
    total_tested = 0
    total_known = 0
    total_unknown = 0

    for config in LEVEL_CONFIGS:
        level = config["level"]
        
        # 查找该层级的输入数据
        level_data = next((r for r in level_results if r["level"] == level), None)
        
        if level_data is None:
            # 没有提供该层级数据，视为跳过
            known = 0
            tested = 0
        else:
            known = level_data["known"]
            tested = level_data.get("tested", config["testCount"])

        # 处理熔断场景
        fuse_triggered = False
        fuse_reason = ""
        
        if fuse_level is not None:
            if level == fuse_level:
                fuse_triggered = True
                if fuse_tested is not None:
                    tested = fuse_tested
                fuse_reason = f"在第 {tested} 个字触发熔断"
            elif level > fuse_level:
                # 熔断后的层级全部跳过
                known = 0
                tested = 0
                fuse_reason = "熔断后跳过"

        # 计算
        unknown = tested - known
        known_rate = known / tested if tested > 0 else 0
        estimated_known = known * config["weight"]

        total_vocabulary += estimated_known
        total_tested += tested
        total_known += known
        total_unknown += unknown

        results.append({
            "level": level,
            "name": config["name"],
            "totalChars": config["totalChars"],
            "testCount": config["testCount"],
            "weight": config["weight"],
            "tested": tested,
            "known": known,
            "unknown": unknown,
            "knownRate": round(known_rate, 4),
            "estimatedKnown": estimated_known,
            "fuseTriggered": fuse_triggered,
            "fuseReason": fuse_reason,
        })

    accuracy = total_known / total_tested if total_tested > 0 else 0

    return {
        "totalVocabulary": total_vocabulary,
        "totalTested": total_tested,
        "totalKnown": total_known,
        "totalUnknown": total_unknown,
        "accuracy": round(accuracy, 4),
        "fuseTriggered": fuse_level is not None,
        "fuseLevel": fuse_level,
        "levelResults": results,
    }


def get_age_assessment(vocabulary, age=None):
    """根据年龄参考表生成评估语"""
    if age is None:
        return "未提供年龄，无法对比同龄参考"

    ref = None
    for r in AGE_REFERENCE:
        age_range = r["age"]
        # 解析年龄范围
        if "-" in age_range:
            parts = age_range.replace("岁", "").split("-")
            low = int(parts[0])
            high = int(parts[1])
            if low <= age < high:
                ref = r
                break
        elif "+" in age_range:
            low = int(age_range.replace("岁+", "").replace("+", ""))
            if age >= low:
                ref = r
                break

    if ref is None:
        return f"{age}岁不在参考范围（3-12岁）内"

    expected_range = f"{ref['min']}-{ref['max']}"
    if vocabulary > ref["max"]:
        return f"太厉害了！远超{ref['age']}的平均水平（{expected_range}字），你是一个出色的小读者！"
    elif vocabulary >= ref["min"]:
        return f"非常棒！认字量在{ref['age']}的正常范围内（{ref['stage']}），继续保持阅读习惯！"
    else:
        return f"每个孩子都有自己的成长节奏，{age}岁认识{vocabulary}字也很不错，保持对文字的兴趣最重要！"


def format_text_report(result, age=None):
    """生成文本格式的报告"""
    lines = []
    lines.append("=" * 60)
    lines.append("📊 识字量计算结果")
    lines.append("=" * 60)
    lines.append("")

    if age:
        lines.append(f"👤 年龄：{age} 岁")
    lines.append(f"📝 测试字数：{result['totalTested']}")
    lines.append(f"✅ 认识：{result['totalKnown']}  ❌ 不认识：{result['totalUnknown']}")
    lines.append(f"📈 正确率：{result['accuracy'] * 100:.1f}%")
    if result["fuseTriggered"]:
        lines.append(f"⚡ 熔断：是（L{result['fuseLevel']}）")
    lines.append("")
    lines.append(f"🎯 估算认字量：{result['totalVocabulary']} 字")
    lines.append("")

    # 计算公式展示
    formula_parts = []
    for lr in result["levelResults"]:
        formula_parts.append(f"{lr['known']}×{lr['weight']}")
    formula = " + ".join(formula_parts)
    lines.append(f"📐 计算公式：W = {formula} = {result['totalVocabulary']}")
    lines.append("")

    # 各层级详情
    lines.append("─" * 60)
    lines.append(f"{'层级':>8}  {'结果':>10}  {'正确率':>8}  {'估算':>10}  {'备注':>10}")
    lines.append("─" * 60)

    for lr in result["levelResults"]:
        if lr["tested"] == 0 and lr["fuseReason"]:
            result_str = "跳过"
            rate_str = "—"
        else:
            result_str = f"{lr['known']}/{lr['tested']}"
            rate_str = f"{lr['knownRate'] * 100:.0f}%"

        note = ""
        if lr["fuseTriggered"]:
            note = "⚡ 熔断"
        elif lr["fuseReason"]:
            note = lr["fuseReason"]

        lines.append(
            f"  L{lr['level']} {lr['name']:>4}  {result_str:>8}  {rate_str:>6}  "
            f"{lr['estimatedKnown']:>6} 字  {note}"
        )

    lines.append("─" * 60)
    lines.append("")

    # 年龄评估
    if age:
        assessment = get_age_assessment(result["totalVocabulary"], age)
        lines.append(f"💪 评估：{assessment}")
        lines.append("")

    return "\n".join(lines)


def interactive_input():
    """交互式输入测试结果"""
    print("📝 交互式输入模式")
    print("请输入各层级的「认识数」（输入 -1 表示该层级跳过）\n")

    level_results = []
    fuse_level = None

    for config in LEVEL_CONFIGS:
        prompt = f"  L{config['level']} {config['name']} (共测 {config['testCount']} 字，权重 ×{config['weight']}): "
        try:
            known_str = input(prompt).strip()
            if known_str == "-1" or known_str == "":
                if fuse_level is None:
                    fuse_level = config["level"]
                continue

            known = int(known_str)
            if known < 0 or known > config["testCount"]:
                print(f"    ⚠️ 认识数应在 0-{config['testCount']} 之间，已自动修正为 {max(0, min(known, config['testCount']))}")
                known = max(0, min(known, config["testCount"]))

            level_results.append({
                "level": config["level"],
                "known": known,
                "tested": config["testCount"],
            })
        except ValueError:
            print("    ⚠️ 请输入数字，已跳过该层级")
            if fuse_level is None:
                fuse_level = config["level"]

    # 可选输入年龄
    age = None
    try:
        age_str = input("\n  👤 被测儿童年龄（可选，直接回车跳过）: ").strip()
        if age_str:
            age = int(age_str)
    except ValueError:
        pass

    return level_results, fuse_level, age


def main():
    parser = argparse.ArgumentParser(
        description="识字量分数计算与验证工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 各层级认识数分别为 48, 40, 20, 10, 3, 1
  python calculate_score.py --known 48 40 20 10 3 1

  # 模拟 L3 熔断
  python calculate_score.py --known 50 40 1 0 0 0 --fuse-level 3 --fuse-tested 8

  # 加上年龄对比
  python calculate_score.py --known 48 40 20 10 3 1 --age 7
        """
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        default=None,
        help="从 JSON 文件加载测试结果"
    )
    parser.add_argument(
        "--known", "-k",
        type=int,
        nargs=6,
        default=None,
        metavar=("L1", "L2", "L3", "L4", "L5", "L6"),
        help="各层级认识数（6 个整数，对应 L1-L6）"
    )
    parser.add_argument(
        "--fuse-level",
        type=int,
        default=None,
        help="熔断层级编号（1-6）"
    )
    parser.add_argument(
        "--fuse-tested",
        type=int,
        default=None,
        help="熔断层级已测字数"
    )
    parser.add_argument(
        "--age",
        type=int,
        default=None,
        help="被测儿童年龄（用于年龄对比评估）"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="输出格式: text(可读文本), json(JSON 格式)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="输出文件路径（默认输出到 stdout）"
    )
    args = parser.parse_args()

    # 确定输入来源
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            input_data = json.load(f)
        level_results = input_data.get("levelResults", [])
        fuse_level = input_data.get("fuseLevel", args.fuse_level)
        fuse_tested = input_data.get("fuseTested", args.fuse_tested)
        age = input_data.get("age", args.age)
    elif args.known:
        level_results = []
        for i, known in enumerate(args.known):
            config = LEVEL_CONFIGS[i]
            tested = config["testCount"]
            
            # 如果指定了熔断层级，调整该层及后续层级
            if args.fuse_level and config["level"] == args.fuse_level:
                tested = args.fuse_tested if args.fuse_tested else tested
            elif args.fuse_level and config["level"] > args.fuse_level:
                known = 0
                tested = 0
            
            level_results.append({
                "level": config["level"],
                "known": known,
                "tested": tested,
            })
        fuse_level = args.fuse_level
        fuse_tested = args.fuse_tested
        age = args.age
    else:
        # 交互式输入
        level_results, fuse_level, age = interactive_input()
        fuse_tested = args.fuse_tested

    # 计算
    result = calculate_score(level_results, fuse_level, fuse_tested)

    # 格式化输出
    if args.format == "json":
        if age:
            result["age"] = age
            result["assessment"] = get_age_assessment(result["totalVocabulary"], age)
        output = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        output = format_text_report(result, age)

    # 写入
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"💾 结果已保存到: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
