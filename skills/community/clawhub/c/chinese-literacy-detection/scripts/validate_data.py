#!/usr/bin/env python3
"""
汉字数据资产完整性验证工具

验证 assets/top_2500_chars_with_words.json 的数据完整性，包括：
1. rank_id 1-2500 连续完整
2. char 字段非空且为单个汉字
3. words 数组非空且每条至少 2 个词组
4. frequency / frequency_cumulative 合理性
5. literacy_rate 字段取值范围 0-100

用法:
    python validate_data.py
    python validate_data.py --data /path/to/chars.json
    python validate_data.py --strict  # 严格模式，warnings 也视为失败
"""

import json
import argparse
import os
import sys
import re


def load_data(data_path):
    """加载并返回 JSON 数据"""
    if not os.path.exists(data_path):
        print(f"❌ 数据文件不存在: {data_path}")
        sys.exit(1)

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"❌ 数据格式错误: 期望 JSON 数组，实际为 {type(data).__name__}")
        sys.exit(1)

    return data


def is_cjk_char(char):
    """判断是否为 CJK 统一汉字"""
    if len(char) != 1:
        return False
    cp = ord(char)
    # CJK Unified Ideographs: U+4E00 - U+9FFF
    # CJK Extension A: U+3400 - U+4DBF
    # CJK Extension B: U+20000 - U+2A6DF
    return (0x4E00 <= cp <= 0x9FFF or
            0x3400 <= cp <= 0x4DBF or
            0x20000 <= cp <= 0x2A6DF)


def validate_data(data):
    """
    验证数据完整性，返回 (errors, warnings) 元组。
    
    Args:
        data: JSON 数组数据
        
    Returns:
        tuple: (errors: list[str], warnings: list[str])
    """
    errors = []
    warnings = []

    # ===== 检查 1: 记录总数 =====
    if len(data) != 2500:
        errors.append(f"记录总数应为 2500，实际为 {len(data)}")

    # ===== 检查 2: 必要字段存在性 =====
    required_fields = {"rank_id", "char", "words", "frequency", "frequency_cumulative", "literacy_rate"}
    for i, entry in enumerate(data):
        missing = required_fields - set(entry.keys())
        if missing:
            errors.append(f"第 {i+1} 条记录缺少字段: {missing}")
            if i >= 10:  # 只报前 10 条的字段缺失
                errors.append(f"...（后续记录的字段缺失检查已省略）")
                break

    # ===== 检查 3: rank_id 连续完整 =====
    rank_ids = sorted([d.get("rank_id", -1) for d in data])
    expected_ids = list(range(1, 2501))

    if len(data) == 2500:
        if rank_ids == expected_ids:
            pass  # 完美
        else:
            missing_ids = set(expected_ids) - set(rank_ids)
            duplicate_ids = [r for r in rank_ids if rank_ids.count(r) > 1]
            if missing_ids:
                sample = sorted(list(missing_ids))[:10]
                errors.append(f"rank_id 缺失 {len(missing_ids)} 个，示例: {sample}")
            if duplicate_ids:
                unique_dups = sorted(set(duplicate_ids))[:10]
                errors.append(f"rank_id 重复 {len(set(duplicate_ids))} 个，示例: {unique_dups}")

    # ===== 检查 4: char 字段 =====
    non_cjk_chars = []
    empty_chars = []
    multi_chars = []
    for entry in data:
        char = entry.get("char", "")
        if not char:
            empty_chars.append(entry.get("rank_id", "?"))
        elif len(char) > 1:
            multi_chars.append((entry.get("rank_id", "?"), char))
        elif not is_cjk_char(char):
            non_cjk_chars.append((entry.get("rank_id", "?"), char))

    if empty_chars:
        errors.append(f"char 字段为空的条目: rank_id = {empty_chars[:10]}")
    if multi_chars:
        errors.append(f"char 字段包含多个字符: {multi_chars[:10]}")
    if non_cjk_chars:
        warnings.append(f"char 字段非 CJK 汉字: {non_cjk_chars[:10]}")

    # ===== 检查 5: words 数组 =====
    empty_words = []
    single_word = []
    words_lengths = []
    for entry in data:
        words = entry.get("words", [])
        rank_id = entry.get("rank_id", "?")
        if not words or len(words) == 0:
            empty_words.append(rank_id)
        else:
            words_lengths.append(len(words))
            if len(words) < 2:
                single_word.append((rank_id, entry.get("char", "?")))

    if empty_words:
        errors.append(f"words 为空的条目 ({len(empty_words)} 个): rank_id = {empty_words[:10]}")
    if single_word:
        warnings.append(f"words 只有 1 个词组 ({len(single_word)} 个): {single_word[:10]}")

    if words_lengths:
        min_len = min(words_lengths)
        max_len = max(words_lengths)
        avg_len = sum(words_lengths) / len(words_lengths)
        print(f"  📊 words 长度分布: min={min_len}, max={max_len}, avg={avg_len:.1f}")

    # ===== 检查 6: frequency 合理性 =====
    frequencies = [d.get("frequency", 0) for d in data]
    if frequencies:
        # 前面的字频率应该更高（大体上）
        if frequencies[0] < frequencies[-1]:
            warnings.append(
                f"frequency 排序可能有误: 第1条({frequencies[0]}) < 最后一条({frequencies[-1]})"
            )
        # 频率应为正数
        neg_freqs = [(d.get("rank_id"), d.get("frequency")) for d in data if d.get("frequency", 0) < 0]
        if neg_freqs:
            errors.append(f"frequency 为负数: {neg_freqs[:5]}")

    # ===== 检查 7: frequency_cumulative 递增性 =====
    sorted_by_rank = sorted(data, key=lambda x: x.get("rank_id", 0))
    prev_cum = 0
    non_increasing = []
    for entry in sorted_by_rank:
        cum = entry.get("frequency_cumulative", 0)
        if cum < prev_cum:
            non_increasing.append((entry.get("rank_id"), cum, prev_cum))
        prev_cum = cum

    if non_increasing:
        warnings.append(
            f"frequency_cumulative 非递增 ({len(non_increasing)} 处): {non_increasing[:5]}"
        )

    # ===== 检查 8: literacy_rate 取值范围 =====
    rates = [d.get("literacy_rate", None) for d in data]
    valid_rates = [r for r in rates if r is not None]
    if valid_rates:
        min_rate = min(valid_rates)
        max_rate = max(valid_rates)
        print(f"  📊 literacy_rate 范围: {min_rate} ~ {max_rate}")
        if min_rate < 0:
            errors.append(f"literacy_rate 存在负值: min = {min_rate}")
        if max_rate > 100:
            errors.append(f"literacy_rate 超过 100: max = {max_rate}")
    else:
        warnings.append("所有记录的 literacy_rate 字段为空")

    # ===== 检查 9: 层级分布 =====
    level_ranges = [
        (1, "核心字", 1, 50, 50),
        (2, "常用字", 51, 200, 150),
        (3, "扩展字", 201, 500, 300),
        (4, "进阶字", 501, 1000, 500),
        (5, "提高字", 1001, 1500, 500),
        (6, "拓展字", 1501, 2500, 1000),
    ]

    print(f"\n  📊 层级分布检查:")
    for level, name, start, end, expected_count in level_ranges:
        actual = len([d for d in data if start <= d.get("rank_id", 0) <= end])
        status = "✅" if actual == expected_count else "❌"
        print(f"    L{level} {name} (rank {start}-{end}): {actual}/{expected_count} {status}")
        if actual != expected_count:
            errors.append(f"L{level} {name}: 期望 {expected_count} 条，实际 {actual} 条")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="汉字数据资产完整性验证")
    parser.add_argument(
        "--data",
        type=str,
        default=None,
        help="汉字数据源 JSON 路径（默认自动查找 assets/top_2500_chars_with_words.json）"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="严格模式：warnings 也视为验证失败"
    )
    args = parser.parse_args()

    # 确定数据源路径
    if args.data:
        data_path = args.data
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        skill_dir = os.path.dirname(script_dir)
        data_path = os.path.join(skill_dir, "assets", "top_2500_chars_with_words.json")

    print(f"🔍 验证数据资产完整性: {data_path}\n")

    # 加载数据
    data = load_data(data_path)
    print(f"  📂 已加载 {len(data)} 条记录\n")

    # 执行验证
    errors, warnings = validate_data(data)

    # 输出结果
    if warnings:
        print(f"\n⚠️  警告 ({len(warnings)}):")
        for w in warnings:
            print(f"   - {w}")

    if errors:
        print(f"\n❌ 错误 ({len(errors)}):")
        for e in errors:
            print(f"   - {e}")
        print("\n❌ 数据验证失败！请修复以上错误。")
        sys.exit(1)
    elif args.strict and warnings:
        print("\n❌ 严格模式下，存在警告视为验证失败。")
        sys.exit(1)
    else:
        print("\n✅ 数据验证通过！所有检查项均正常。")
        sys.exit(0)


if __name__ == "__main__":
    main()
