#!/usr/bin/env python3
"""测试 API 服务"""

import requests
import json

# 测试数据
test_problem = {
    "title": "38 岁财务 BP，长沙 10K vs 惠州 25K",
    "type": "职业选择",
    "status": "在长沙工作，10K/月，管理层动荡",
    "options": "A. 留长沙 B. 去惠州",
    "concerns": "3 年变动频繁，年龄大，家庭因素"
}

# 发送请求
print("发送测试请求...")
response = requests.post(
    'http://localhost:5001/api/v1/analyze',
    json=test_problem,
    headers={'Content-Type': 'application/json'}
)

print(f"状态码：{response.status_code}\n")

if response.ok:
    result = response.json()
    print("✅ API 响应成功！")
    print(f"\n问题 ID: {result['problem_id']}")
    print(f"推荐：{result['analysis']['recommendation']}")
    print(f"\n理由:")
    for reason in result['analysis']['reasoning']:
        print(f"  ✓ {reason}")
else:
    print(f"❌ 请求失败：{response.text}")
