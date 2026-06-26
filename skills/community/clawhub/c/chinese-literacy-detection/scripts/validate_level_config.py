#!/usr/bin/env python3
"""
层级配置一致性验证工具

验证 levelConfig.js 中的分层抽样配置是否满足以下约束：
1. 排名区间连续无重叠
2. 各层级 testCount 总和等于 TOTAL_TEST_COUNT
3. 权重与抽样间隔一致
4. 排名覆盖 1-2500

用法:
    python validate_level_config.py [--json config.json]
    
不带参数时使用内置默认配置进行验证。
"""

import sys
import json
import argparse


# 默认配置（与 src/utils/levelConfig.js 保持同步）
DEFAULT_LEVEL_CONFIGS = [
    {"level": 1, "name": "核心字", "rankStart": 1,    "rankEnd": 50,   "sampleInterval": 1,   "testCount": 50,  "weight": 1},
    {"level": 2, "name": "常用字", "rankStart": 51,   "rankEnd": 200,  "sampleInterval": 3,   "testCount": 50,  "weight": 3},
    {"level": 3, "name": "扩展字", "rankStart": 201,  "rankEnd": 500,  "sampleInterval": 10,  "testCount": 30,  "weight": 10},
    {"level": 4, "name": "进阶字", "rankStart": 501,  "rankEnd": 1000, "sampleInterval": 20,  "testCount": 25,  "weight": 20},
    {"level": 5, "name": "提高字", "rankStart": 1001, "rankEnd": 1500, "sampleInterval": 50,  "testCount": 10,  "weight": 50},
    {"level": 6, "name": "拓展字", "rankStart": 1501, "rankEnd": 2500, "sampleInterval": 100, "testCount": 10,  "weight": 100},
]

DEFAULT_FUSE_CONFIG = {
    "consecutiveUnknownLimit": 5,
    "errorRateLimit": 0.8,
    "minTestCountForErrorRate": 5,
}

EXPECTED_TOTAL_TEST_COUNT = 175
EXPECTED_TOTAL_CHARS = 2500


def validate_configs(level_configs, fuse_config, total_test_count, total_chars):
    """验证配置一致性，返回 (is_valid, errors, warnings) 元组"""
    errors = []
    warnings = []

    # ===== 检查1: 层级编号连续 =====
    levels = [c["level"] for c in level_configs]
    expected_levels = list(range(1, len(level_configs) + 1))
    if levels != expected_levels:
        errors.append(f"层级编号不连续: 期望 {expected_levels}，实际 {levels}")

    # ===== 检查2: 排名区间连续无重叠 =====
    sorted_configs = sorted(level_configs, key=lambda x: x["rankStart"])
    for i, config in enumerate(sorted_configs):
        if i == 0:
            if config["rankStart"] != 1:
                errors.append(f"L{config['level']}: 排名起始应为 1，实际为 {config['rankStart']}")
        else:
            prev = sorted_configs[i - 1]
            expected_start = prev["rankEnd"] + 1
            if config["rankStart"] != expected_start:
                errors.append(
                    f"L{config['level']}: 排名起始应为 {expected_start}（L{prev['level']} 结束于 {prev['rankEnd']}），"
                    f"实际为 {config['rankStart']}"
                )

    last_config = sorted_configs[-1]
    if last_config["rankEnd"] != total_chars:
        errors.append(f"最后一层排名终止应为 {total_chars}，实际为 {last_config['rankEnd']}")

    # ===== 检查3: testCount 总和 =====
    actual_total = sum(c["testCount"] for c in level_configs)
    if actual_total != total_test_count:
        errors.append(f"testCount 总和应为 {total_test_count}，实际为 {actual_total}")

    # ===== 检查4: 权重与抽样间隔一致性 =====
    for config in level_configs:
        level_total = config["rankEnd"] - config["rankStart"] + 1
        expected_weight = level_total // config["testCount"] if config["testCount"] > 0 else 0

        # 权重应等于（层级总字数 / 抽样数），允许1的容差（因为整除）
        if abs(config["weight"] - config["sampleInterval"]) > 0:
            warnings.append(
                f"L{config['level']}: weight({config['weight']}) != sampleInterval({config['sampleInterval']})"
            )

        if config["sampleInterval"] != 1:  # 非全量测试
            if config["testCount"] > level_total:
                errors.append(
                    f"L{config['level']}: testCount({config['testCount']}) > "
                    f"层级总字数({level_total})"
                )

    # ===== 检查5: 熔断配置合理性 =====
    if fuse_config["consecutiveUnknownLimit"] < 3:
        warnings.append(f"连续不认识上限 {fuse_config['consecutiveUnknownLimit']} 过小，可能频繁触发熔断")
    if fuse_config["consecutiveUnknownLimit"] > 10:
        warnings.append(f"连续不认识上限 {fuse_config['consecutiveUnknownLimit']} 过大，可能延迟熔断")

    if not (0.5 <= fuse_config["errorRateLimit"] <= 0.95):
        warnings.append(f"错误率上限 {fuse_config['errorRateLimit']} 不在推荐范围 [0.5, 0.95] 内")

    if fuse_config["minTestCountForErrorRate"] < 3:
        warnings.append(f"错误率计算最小样本数 {fuse_config['minTestCountForErrorRate']} 过小")

    # ===== 检查6: 每层级信息展示 =====
    print("\n📊 层级配置概览:")
    print(f"{'层级':>4} {'名称':>6} {'排名区间':>12} {'总字数':>6} {'抽样数':>6} {'间隔':>4} {'权重':>4}")
    print("─" * 54)
    for config in level_configs:
        level_total = config["rankEnd"] - config["rankStart"] + 1
        print(
            f"  L{config['level']}  {config['name']:>4}  "
            f"{config['rankStart']:>4}-{config['rankEnd']:<4}  "
            f"{level_total:>5}  {config['testCount']:>5}  "
            f"×{config['sampleInterval']:<3}  ×{config['weight']:<3}"
        )
    print("─" * 54)
    print(f"  总计                     {total_chars:>5}  {actual_total:>5}")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def main():
    parser = argparse.ArgumentParser(description="验证层级配置一致性")
    parser.add_argument("--json", help="从 JSON 文件加载配置", default=None)
    args = parser.parse_args()

    if args.json:
        with open(args.json, "r", encoding="utf-8") as f:
            data = json.load(f)
        level_configs = data.get("levelConfigs", DEFAULT_LEVEL_CONFIGS)
        fuse_config = data.get("fuseConfig", DEFAULT_FUSE_CONFIG)
        total_test_count = data.get("totalTestCount", EXPECTED_TOTAL_TEST_COUNT)
        total_chars = data.get("totalChars", EXPECTED_TOTAL_CHARS)
    else:
        level_configs = DEFAULT_LEVEL_CONFIGS
        fuse_config = DEFAULT_FUSE_CONFIG
        total_test_count = EXPECTED_TOTAL_TEST_COUNT
        total_chars = EXPECTED_TOTAL_CHARS

    print("🔍 验证层级配置一致性...\n")

    is_valid, errors, warnings = validate_configs(
        level_configs, fuse_config, total_test_count, total_chars
    )

    if warnings:
        print(f"\n⚠️  警告 ({len(warnings)}):")
        for w in warnings:
            print(f"   - {w}")

    if errors:
        print(f"\n❌ 错误 ({len(errors)}):")
        for e in errors:
            print(f"   - {e}")
        print("\n❌ 验证失败！请修复以上错误。")
        sys.exit(1)
    else:
        print("\n✅ 所有验证通过！配置一致性良好。")
        sys.exit(0)


if __name__ == "__main__":
    main()
