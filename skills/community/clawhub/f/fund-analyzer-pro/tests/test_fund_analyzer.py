#!/usr/bin/env python3
"""
Fund-Analyzer-Pro 单元测试

**运行方式**：
```bash
cd ~/.openclaw/workspace/skills/fund-analyzer-pro
python tests/test_fund_analyzer.py
```

**测试覆盖**：
- 基金代码校验
- 缓存机制
- 加密存储
- API 降级
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# 导入被测模块（使用 exec 方式，因为文件名含连字符）
scripts_path = Path("/home/admin/.openclaw/workspace/skills/fund-analyzer-pro/scripts")

# 执行脚本获取命名空间
qieman_ns = {}
with open(scripts_path / "qieman-mcp-query.py", 'r', encoding='utf-8') as f:
    exec(f.read(), qieman_ns)

encrypt_ns = {}
with open(scripts_path / "encrypt-holdings.py", 'r', encoding='utf-8') as f:
    exec(f.read(), encrypt_ns)

validate_fund_code = qieman_ns['validate_fund_code']
get_cache_key = qieman_ns['get_cache_key']
get_from_cache = qieman_ns['get_from_cache']
save_to_cache = qieman_ns['save_to_cache']

encrypt_data = encrypt_ns['encrypt_data']
decrypt_data = encrypt_ns['decrypt_data']
save_holdings = encrypt_ns['save_holdings']
load_holdings = encrypt_ns['load_holdings']
delete_holdings = encrypt_ns['delete_holdings']

# 测试数据
# 测试数据
TEST_FUND_CODES = [
    ("000001", True),    # 有效
    ("110022", True),    # 有效
    ("12345", False),    # 5 位，无效
    ("1234567", False),  # 7 位，无效
    ("abc123", False),   # 含字母，无效
    ("", False),         # 空字符串，无效
    (None, False),       # None，无效
]

def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Fund-Analyzer-Pro 单元测试")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    # 测试 1：基金代码校验
    print("\n📝 测试 1：基金代码校验")
    for code, expected in TEST_FUND_CODES:
        result = validate_fund_code(code)
        if result == expected:
            passed += 1
            print(f"  ✅ {code} → {result}")
        else:
            failed += 1
            print(f"  ❌ {code} → {result} (期望 {expected})")
    
    # 测试 2：缓存 key 生成
    print("\n📝 测试 2：缓存 key 生成")
    key1 = get_cache_key("test_method", {"param": "value"})
    key2 = get_cache_key("test_method", {"param": "value"})
    key3 = get_cache_key("test_method", {"param": "other"})
    if key1 == key2:
        passed += 1
        print(f"  ✅ 相同参数生成相同 key")
    else:
        failed += 1
        print(f"  ❌ 相同参数应生成相同 key")
    if key1 != key3:
        passed += 1
        print(f"  ✅ 不同参数生成不同 key")
    else:
        failed += 1
        print(f"  ❌ 不同参数应生成不同 key")
    
    # 测试 3：缓存保存加载
    print("\n📝 测试 3：缓存保存加载")
    test_data = {"nav": 1.5, "change": "+2.5%"}
    cache_key = "test_cache_key"
    save_to_cache(cache_key, test_data)
    loaded = get_from_cache(cache_key, ttl=3600)
    if loaded == test_data:
        passed += 1
        print(f"  ✅ 缓存数据一致")
    else:
        failed += 1
        print(f"  ❌ 缓存数据不一致")
    
    # 测试 4：加密解密
    print("\n📝 测试 4：加密解密")
    test_data = {"fund": "000001", "amount": 100000}
    encrypted = encrypt_data(test_data)
    decrypted = decrypt_data(encrypted)
    if decrypted == test_data:
        passed += 1
        print(f"  ✅ 加密解密一致")
    else:
        failed += 1
        print(f"  ❌ 加密解密不一致")
    
    # 测试 5：持仓保存加载
    print("\n📝 测试 5：持仓保存加载")
    test_user = "test_user_final"
    test_holdings = {"user_id": test_user, "funds": [{"code": "000001"}]}
    save_holdings(test_user, test_holdings)
    loaded = load_holdings(test_user)
    if loaded and loaded['user_id'] == test_user:
        passed += 1
        print(f"  ✅ 持仓保存加载成功")
        delete_holdings(test_user)
    else:
        failed += 1
        print(f"  ❌ 持仓保存加载失败")
    
    # 总结
    print("\n" + "=" * 60)
    print(f"测试完成：通过 {passed} 个，失败 {failed} 个")
    print("=" * 60)
    
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
