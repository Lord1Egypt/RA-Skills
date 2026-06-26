#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

# 测试导入
try:
    from main import check_content, run
    print("✓ 模块导入成功")
except Exception as e:
    print(f"✗ 模块导入失败：{e}")
    sys.exit(1)

# 测试空文本
print("\n测试 1: 空文本检测")
result = check_content("")
print(json.dumps(result, ensure_ascii=False, indent=2))

# 测试超长文本
print("\n测试 2: 超长文本检测")
long_text = "a" * 5001
result = check_content(long_text)
print(json.dumps(result, ensure_ascii=False, indent=2))

# 测试正常文本（需要配置正确的 API 凭证）
print("\n测试 3: 正常文本检测（需要配置正确的 API 凭证）")
print("提示：请设置以下环境变量：")
print("  export CHENGJUN_API_KEY='your_http_api_token'")

test_text = "创建特色社会主义道路，为深入学习贯彻党的二十精神"
result = check_content(test_text)
print(json.dumps(result, ensure_ascii=False, indent=2))

print("\n测试完成")
