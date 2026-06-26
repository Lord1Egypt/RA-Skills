#!/usr/bin/env python3
"""
测试序列即时生成器（分层抽样）

基于 assets/top_2500_chars_with_words.json 真实汉字数据源，
按六层分级配置执行 Fisher-Yates 洗牌 + 分层抽样，
即时生成一组测试序列（最多 175 字）。

用法:
    python generate_test_sequence.py
    python generate_test_sequence.py --output test_sequence.json
    python generate_test_sequence.py --seed 42        # 可复现
    python generate_test_sequence.py --format compact  # 紧凑输出
    python generate_test_sequence.py --data /path/to/chars.json  # 自定义数据源

输出:
    按 L1→L6 层级顺序排列的测试序列 JSON 数组，每条包含:
    - rank_id: 词频排名
    - char: 汉字
    - words: 组词示例
    - level: 层级编号 (1-6)
    - level_name: 层级名称
    - weight: 该层权重
"""

import json
import random
import argparse
import os
import sys


# ============================================================
# 六层分级配置（与 SKILL.md 保持完全一致）
# ============================================================
LEVEL_CONFIGS = [
    {"level": 1, "name": "核心字", "rankStart": 1,    "rankEnd": 50,   "testCount": 50,  "weight": 1},
    {"level": 2, "name": "常用字", "rankStart": 51,   "rankEnd": 200,  "testCount": 50,  "weight": 3},
    {"level": 3, "name": "扩展字", "rankStart": 201,  "rankEnd": 500,  "testCount": 30,  "weight": 10},
    {"level": 4, "name": "进阶字", "rankStart": 501,  "rankEnd": 1000, "testCount": 25,  "weight": 20},
    {"level": 5, "name": "提高字", "rankStart": 1001, "rankEnd": 1500, "testCount": 10,  "weight": 50},
    {"level": 6, "name": "拓展字", "rankStart": 1501, "rankEnd": 2500, "testCount": 10,  "weight": 100},
]

TOTAL_TEST_COUNT = 175  # 所有层级 testCount 之和


def load_character_data(data_path):
    """
    加载汉字数据源。
    
    Args:
        data_path: JSON 文件路径
        
    Returns:
        list: 2500 条汉字记录
        
    Raises:
        FileNotFoundError: 数据文件不存在
        ValueError: 数据格式不正确或记录数不足
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"数据源文件不存在: {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"数据格式错误: 期望 JSON 数组，实际为 {type(data).__name__}")

    if len(data) < 2500:
        raise ValueError(f"数据不完整: 期望 2500 条记录，实际 {len(data)} 条")

    # 验证必要字段
    required_fields = {"rank_id", "char", "words"}
    for i, entry in enumerate(data[:5]):  # 抽查前 5 条
        missing = required_fields - set(entry.keys())
        if missing:
            raise ValueError(f"第 {i+1} 条记录缺少字段: {missing}")

    return data


def fisher_yates_shuffle(array, rng=None):
    """
    Fisher-Yates 洗牌算法（原地打乱的副本）。
    
    等概率生成每种排列，时间复杂度 O(n)。
    
    Args:
        array: 待洗牌的数组
        rng: random.Random 实例（可选，用于可复现随机）
        
    Returns:
        list: 打乱后的新数组
    """
    if rng is None:
        rng = random.Random()

    result = list(array)
    n = len(result)
    for i in range(n - 1, 0, -1):
        j = rng.randint(0, i)
        result[i], result[j] = result[j], result[i]
    return result


def stratified_sample(all_characters, level_configs, rng=None):
    """
    分层抽样：按六层配置从 2500 汉字中抽取测试序列。
    
    算法流程:
    1. 按 rank_id 将汉字分配到 6 个层级
    2. 每层内用 Fisher-Yates 洗牌随机打乱
    3. 若层级 testCount ≥ 层级总字数，全量保留（如 L1）
    4. 否则取前 testCount 个（无放回抽样）
    5. 为每个抽出的字标注层级信息和权重
    6. 按 L1→L6 顺序拼接，层内随机排列
    
    Args:
        all_characters: 完整的 2500 汉字数据列表
        level_configs: 六层配置列表
        rng: random.Random 实例
        
    Returns:
        list: 测试序列（最多 175 条），每条含 rank_id, char, words, level, level_name, weight
    """
    if rng is None:
        rng = random.Random()

    test_sequence = []

    for config in level_configs:
        # Step 1: 过滤该层级的汉字
        level_chars = [
            c for c in all_characters
            if config["rankStart"] <= c["rank_id"] <= config["rankEnd"]
        ]

        if not level_chars:
            print(f"  ⚠️  L{config['level']} ({config['name']}): 无匹配汉字", file=sys.stderr)
            continue

        # Step 2: Fisher-Yates 洗牌
        shuffled = fisher_yates_shuffle(level_chars, rng)

        # Step 3: 抽样（testCount ≥ 总数时为全量）
        sample_count = min(config["testCount"], len(shuffled))
        selected = shuffled[:sample_count]

        # Step 4: 标注层级信息
        for char_entry in selected:
            test_sequence.append({
                "rank_id": char_entry["rank_id"],
                "char": char_entry["char"],
                "words": char_entry["words"],
                "level": config["level"],
                "level_name": config["name"],
                "weight": config["weight"],
            })

    return test_sequence


def format_sequence_summary(sequence, level_configs):
    """生成测试序列的文本摘要"""
    lines = []
    lines.append(f"📋 测试序列已生成: 共 {len(sequence)} 字\n")
    lines.append(f"{'层级':>4}  {'名称':>6}  {'抽样数':>6}  {'示例字':>20}")
    lines.append("─" * 50)

    for config in level_configs:
        level_chars = [s for s in sequence if s["level"] == config["level"]]
        sample_chars = "、".join(c["char"] for c in level_chars[:5])
        if len(level_chars) > 5:
            sample_chars += "…"
        lines.append(
            f"  L{config['level']}  {config['name']:>4}  "
            f"{len(level_chars):>5}字  {sample_chars}"
        )

    lines.append("─" * 50)
    lines.append(f"  总计          {len(sequence):>5}字")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="基于真实汉字数据的分层抽样测试序列生成器"
    )
    parser.add_argument(
        "--data",
        type=str,
        default=None,
        help="汉字数据源 JSON 路径（默认自动查找 assets/top_2500_chars_with_words.json）"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="输出文件路径（默认输出到 stdout）"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="随机种子（用于可复现的测试序列）"
    )
    parser.add_argument(
        "--format",
        choices=["full", "compact", "chars_only"],
        default="full",
        help="输出格式: full(完整JSON), compact(紧凑JSON), chars_only(仅汉字列表)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="静默模式，不输出摘要信息"
    )
    args = parser.parse_args()

    # 确定数据源路径
    if args.data:
        data_path = args.data
    else:
        # 自动查找：当前脚本所在目录的兄弟目录 assets/
        script_dir = os.path.dirname(os.path.abspath(__file__))
        skill_dir = os.path.dirname(script_dir)
        data_path = os.path.join(skill_dir, "assets", "top_2500_chars_with_words.json")

    # 设置随机种子
    rng = random.Random(args.seed) if args.seed is not None else random.Random()

    if not args.quiet:
        print(f"📂 数据源: {data_path}", file=sys.stderr)
        if args.seed is not None:
            print(f"🎲 随机种子: {args.seed}", file=sys.stderr)

    # 加载数据
    try:
        all_characters = load_character_data(data_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    if not args.quiet:
        print(f"✅ 已加载 {len(all_characters)} 条汉字记录", file=sys.stderr)

    # 执行分层抽样
    sequence = stratified_sample(all_characters, LEVEL_CONFIGS, rng)

    # 输出摘要
    if not args.quiet:
        print(f"\n{format_sequence_summary(sequence, LEVEL_CONFIGS)}", file=sys.stderr)

    # 格式化输出
    if args.format == "full":
        output = json.dumps(sequence, ensure_ascii=False, indent=2)
    elif args.format == "compact":
        output = json.dumps(sequence, ensure_ascii=False, separators=(",", ":"))
    elif args.format == "chars_only":
        # 按层级分组，输出纯汉字列表
        lines = []
        for config in LEVEL_CONFIGS:
            level_chars = [s["char"] for s in sequence if s["level"] == config["level"]]
            lines.append(f"L{config['level']} {config['name']}: {'、'.join(level_chars)}")
        output = "\n".join(lines)

    # 写入文件或 stdout
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        if not args.quiet:
            print(f"\n💾 已保存到: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
