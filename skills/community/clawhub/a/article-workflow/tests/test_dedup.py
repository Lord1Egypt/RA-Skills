#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Article Workflow 单元测试

运行：
  python tests/test_dedup.py
  python -m pytest tests/  (如果安装了 pytest)
"""

import sys
from pathlib import Path

# 导入核心模块
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
from dedup import normalize_url, get_url_hash, get_content_fingerprint, check_duplicate


def test(name, condition, message=""):
    """简单测试断言"""
    if condition:
        print(f"✅ {name}")
        return True
    else:
        print(f"❌ {name}")
        if message:
            print(f"   {message}")
        return False


def run_tests():
    """运行所有测试"""
    print("="*60)
    print("  🧪 Article Workflow 单元测试")
    print("="*60)
    print()
    
    passed = 0
    failed = 0
    
    # Test 1: 微信 URL 标准化
    print("📝 测试 URL 标准化...")
    url = "https://mp.weixin.qq.com/s?__biz=xxx&mid=xxx&idx=1&sn=xxx&mpshare=1&srcid=xxx"
    normalized = normalize_url(url)
    if test("微信 URL 保留关键参数", 
            "__biz=xxx" in normalized and "mid=xxx" in normalized and "idx=1" in normalized):
        passed += 1
    else:
        failed += 1
    
    if test("微信 URL 去除追踪参数", 
            "mpshare" not in normalized and "srcid" not in normalized):
        passed += 1
    else:
        failed += 1
    
    # Test 2: 同一篇文章不同 URL
    url1 = "https://mp.weixin.qq.com/s?__biz=xxx&mid=xxx&idx=1&sn=xxx&mpshare=1"
    url2 = "https://mp.weixin.qq.com/s?__biz=xxx&mid=xxx&idx=1&sn=xxx&srcid=yyy"
    if test("同一篇文章标准化后相同", normalize_url(url1) == normalize_url(url2)):
        passed += 1
    else:
        failed += 1
    
    # Test 3: 非微信 URL
    if test("非微信 URL 保持不变", 
            normalize_url("https://github.com/owner/repo") == "https://github.com/owner/repo"):
        passed += 1
    else:
        failed += 1
    
    # Test 4: URL 哈希
    print("\n🔐 测试 URL 哈希...")
    if test("相同 URL 相同哈希", 
            get_url_hash("https://example.com") == get_url_hash("https://example.com")):
        passed += 1
    else:
        failed += 1
    
    if test("不同 URL 不同哈希", 
            get_url_hash("https://example.com/1") != get_url_hash("https://example.com/2")):
        passed += 1
    else:
        failed += 1
    
    # Test 5: 内容指纹
    print("\n👆 测试内容指纹...")
    if test("相同内容相同指纹", 
            get_content_fingerprint("Title", "Content") == get_content_fingerprint("Title", "Content")):
        passed += 1
    else:
        failed += 1
    
    if test("不同标题不同指纹", 
            get_content_fingerprint("Title1", "Content") != get_content_fingerprint("Title2", "Content")):
        passed += 1
    else:
        failed += 1
    
    if test("指纹长度为 32 字符（MD5）", 
            len(get_content_fingerprint("T", "C")) == 32):
        passed += 1
    else:
        failed += 1
    
    # Test 6: 内容截断
    long_content = "A" * 2000
    short_content = "A" * 1000
    if test("超过 1000 字被截断", 
            get_content_fingerprint("T", long_content) == get_content_fingerprint("T", short_content)):
        passed += 1
    else:
        failed += 1
    
    # 总结
    print("\n" + "="*60)
    print(f"  测试结果：{passed} 通过，{failed} 失败")
    print("="*60)
    
    if failed == 0:
        print("\n✅ 所有测试通过！")
        return 0
    else:
        print(f"\n⚠️  {failed} 个测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
