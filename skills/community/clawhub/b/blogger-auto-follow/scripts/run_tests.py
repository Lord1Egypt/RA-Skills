#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化测试一键运行器 (Automated Test Suite Runner)
运行所有单元测试与健康检查并输出报告
"""

import os
import sys
import unittest
import time

def run_all_tests():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_dir = os.path.join(project_root, "tests")

    print("=" * 68)
    print("🧪 开始运行 Blogger Auto-Follow 自动化测试套件...")
    print(f"📁 测试目录: {test_dir}")
    print("=" * 68)

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir, pattern="test_*.py")

    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    elapsed = time.time() - start_time

    print("\n" + "=" * 68)
    print(f"📊 测试运行完成 (耗时: {elapsed:.2f} 秒)")
    print(f"   ✅ 测试用例总数: {result.testsRun}")
    print(f"   ❌ 失败 (Failures): {len(result.failures)}")
    print(f"   ⚠️ 错误 (Errors):   {len(result.errors)}")
    print("=" * 68)

    if result.wasSuccessful():
        print("🎉 全部自动化测试通过！核心功能与数据契约稳定。")
        return 0
    else:
        print("❌ 存在未通过的测试，请根据上方堆栈信息进行修复。")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
