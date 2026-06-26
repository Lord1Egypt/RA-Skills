#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地址分类器测试脚本
验证所有分类规则是否正常工作
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from address_classifier import AddressClassifier


def test_classifier():
    """测试各种场景的分类"""
    classifier = AddressClassifier({'log_level': 'DEBUG'})

    test_cases = [
        # (ID, 地址, 期望分类结果, 期望大类)
        ("1", "贵州省贵阳市南明区沙冲南路226号", "贵州贵阳南明", "本省本市"),
        ("2", "贵州省开阳县禾丰乡典寨村", "贵州贵阳开阳", "本省本市"),
        ("3", "贵州省清镇市红枫湖镇", "贵州贵阳清镇", "本省本市"),
        ("4", "贵州省毕节市七星关区", "贵州毕节市", "本省外市"),
        ("5", "贵州省纳雍县张家湾镇", "贵州毕节市", "本省外市"),
        ("6", "贵州省仁怀市长岗镇", "贵州遵义市", "本省外市"),
        ("7", "山东省莱阳市姜疃镇", "外省山东省", "外省"),
        ("8", "西河镇新四村11组", "外省重庆市", "外省"),
        ("9", "河南省焦作市", "地址不全", "地址不全"),
    ]

    print("开始测试地址分类器...")
    print("=" * 80)

    passed = 0
    failed = 0

    for address_id, address, expected_result, expected_category in test_cases:
        result = classifier.classify(address_id, address)

        # 验证结果
        result_ok = result.classified_result == expected_result
        category_ok = result.category == expected_category

        status = "✓ PASS" if (result_ok and category_ok) else "✗ FAIL"

        if result_ok and category_ok:
            passed += 1
        else:
            failed += 1

        print(f"\n测试 {address_id}: {status}")
        print(f"  输入: {address}")
        print(f"  期望: {expected_result} ({expected_category})")
        print(f"  实际: {result.classified_result} ({result.category})")

        if not result_ok:
            print(f"  分类结果不匹配!")
        if not category_ok:
            print(f"  大类标识不匹配!")

    print("\n" + "=" * 80)
    print(f"测试结果: 通过 {passed}/{len(test_cases)}, 失败 {failed}/{len(test_cases)}")

    if failed == 0:
        print("✓ 所有测试通过！")
        return True
    else:
        print("✗ 存在测试失败项")
        return False


if __name__ == "__main__":
    success = test_classifier()
    sys.exit(0 if success else 1)
