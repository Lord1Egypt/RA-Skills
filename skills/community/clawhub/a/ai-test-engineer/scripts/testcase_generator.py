#!/usr/bin/env python3
"""
AI测试工程师 - 测试用例模板生成器
根据用户指定的测试类型和需求，自动生成符合8要素标准的测试用例模板。
"""

import json
import sys
from datetime import datetime

TEST_CASE_TEMPLATE = """| {id} | {title} | {precondition} | {steps} | {expected} | {data} | {priority} |"""

PRIORITY_GUIDE = {
    "P0": "阻塞发布 - 核心流程/资金/安全/数据丢失",
    "P1": "高优先级 - 重要功能异常/核心流程备选路径",
    "P2": "中优先级 - 非核心功能/边界场景",
    "P3": "低优先级 - UI细节/低频场景/优化建议",
}

METHOD_GUIDE = {
    "功能测试": "等价类划分 + 边界值分析 + 场景法",
    "接口测试": "参数组合 + 边界值 + 鉴权 + 响应校验",
    "性能测试": "负载模型 + 基准/负载/压力/稳定性场景",
    "安全测试": "OWASP Top 10 + STRIDE威胁模型",
    "兼容性测试": "兼容性矩阵（平台 × 浏览器 × 分辨率）",
    "探索性测试": "SBTM Charter + 测程",
}


def generate_markdown_header(module_name, test_type, requirement_desc):
    """生成测试用例文档头部"""
    return f"""# {module_name} - 测试用例

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> 测试类型：{test_type}
> 设计方法：{METHOD_GUIDE.get(test_type, '通用方法')}

## 需求概述
{requirement_desc}

## 测试设计方法说明
{METHOD_GUIDE.get(test_type, '请根据测试类型选择适当的设计方法')}

## 优先级说明
| 优先级 | 含义 | 判定标准 |
|--------|------|---------|
| P0 | 阻塞 | {PRIORITY_GUIDE['P0']} |
| P1 | 高 | {PRIORITY_GUIDE['P1']} |
| P2 | 中 | {PRIORITY_GUIDE['P2']} |
| P3 | 低 | {PRIORITY_GUIDE['P3']} |

## 测试用例

| 编号 | 标题 | 前置条件 | 测试步骤 | 预期结果 | 测试数据 | 优先级 |
|------|------|---------|---------|---------|---------|--------|
"""


def generate_test_case(case_id, title, precondition, steps, expected, data, priority):
    """生成单条测试用例的Markdown格式"""
    return f"| {case_id} | {title} | {precondition} | {steps} | {expected} | {data} | {priority} |"


def main():
    print("=== AI测试工程师 - 测试用例模板生成器 ===\n")

    module_name = input("模块名称（如：用户登录）：").strip()
    test_type = input("测试类型（功能测试/接口测试/性能测试/安全测试/兼容性测试/探索性测试）：").strip()
    requirement_desc = input("需求简述（一句话描述）：").strip()

    if test_type not in METHOD_GUIDE:
        test_type = "功能测试"

    markdown = generate_markdown_header(module_name, test_type, requirement_desc)

    print(f"\n设计方法：{METHOD_GUIDE[test_type]}")
    print("\n现在开始逐条添加测试用例（输入空行结束）：\n")

    case_num = 1
    while True:
        print(f"--- 用例 #{case_num} ---")
        title = input("标题（动词+验证点）：").strip()
        if not title:
            break

        precondition = input("前置条件：").strip()
        steps = input("测试步骤（一步一验证，用→分隔）：").strip()
        expected = input("预期结果：").strip()
        data = input("测试数据：").strip()
        priority = input("优先级（P0/P1/P2/P3）：").strip().upper()
        if priority not in PRIORITY_GUIDE:
            priority = "P2"

        case_id = f"{module_name[:4].upper()}-{case_num:03d}"
        markdown += generate_test_case(case_id, title, precondition, steps, expected, data, priority) + "\n"
        case_num += 1

    # 添加测试用例质量检查清单
    markdown += f"""
## 用例质量自检

- [ ] 每个用例含完整的8要素（编号/标题/前置/步骤/预期/数据/优先级/需求）
- [ ] 预期结果可量化，不含"正确""正常"等模糊词
- [ ] 测试步骤一步一验证，中间状态明确
- [ ] 测试数据具体可用，无需额外理解
- [ ] 覆盖正向/边界/异常三种类型
- [ ] 优先级划分有明确理由
- [ ] 异常用例独立（不合并多个无效等价类）

---
*由 AI测试工程师 自动生成*
"""
    print("\n✅ 测试用例模板生成完成！可直接粘贴到测试管理平台。\n")
    return markdown


if __name__ == "__main__":
    result = main()
    # 输出完整Markdown
    print("\n" + "=" * 60)
    print(result)
