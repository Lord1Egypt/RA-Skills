# Fund Advisor Agent 使用示例

本文档提供 Fund Advisor Agent 的常见使用场景和示例代码。

## 快速开始

### 示例1：基础基金查询

```python
from src.agents.agent import build_agent

# 构建 Agent
agent = build_agent()

# 查询基金净值
response = agent.invoke({
    "messages": [
        ("user", "帮我查询易方达蓝筹精选（005827）的最新净值和业绩")
    ]
})

print(response["messages"][-1].content)
```

### 示例2：完整配置方案咨询

```python
# 用户咨询配置方案
response = agent.invoke({
    "messages": [
        ("user", """我想配置一个基金组合，具体信息如下：
        - 风险承受能力：中等
        - 投资期限：3年
        - 可用资金：20万元
        - 预期收益：6-8%
        
        请给我一个详细的配置方案""")
    ]
})

print(response["messages"][-1].content)
```

## 典型场景

### 场景1：定投计划制定

```
用户：我想开始定投沪深300指数基金，每月投2000元，帮我计算一下3年后的预期收益

Agent：
1. 使用 calculate_sip_returns 工具计算收益
2. 生成定投计划建议
3. 提供止盈策略建议
```

**示例代码：**
```python
# 计算定投收益
response = agent.invoke({
    "messages": [
        ("user", "计算每月定投2000元，3年，年化8%的定投收益")
    ]
})
```

### 场景2：基金对比分析

```
用户：帮我对比一下易方达蓝筹精选、招商中证白酒、景顺长城新兴成长这三只基金

Agent：
1. 使用 query_fund_data 查询三只基金数据
2. 使用 compare_funds_performance 对比业绩
3. 使用 compare_funds_risk_metrics 对比风险指标
4. 生成对比报告
```

**示例代码：**
```python
# 对比基金业绩
response = agent.invoke({
    "messages": [
        ("user", "对比易方达蓝筹精选、招商中证白酒、景顺长城新兴成长的近一年业绩")
    ]
})
```

### 场景3：投资报告生成

```
用户：请把刚才的配置方案生成PDF报告

Agent：
1. 使用 generate_portfolio_pdf_report 生成报告
2. 返回下载链接
```

**示例代码：**
```python
# 生成 PDF 报告
response = agent.invoke({
    "messages": [
        ("user", "生成我的配置方案PDF报告")
    ]
})
```

### 场景4：投资日记

```
用户：记录一下今天的投资心得，今天学习了定投策略，觉得很适合工薪族

Agent：
1. 使用 create_investment_diary 创建日记
2. 分析情绪和市场观点
3. 返回日记ID和确认信息
```

**示例代码：**
```python
# 创建投资日记
response = agent.invoke({
    "messages": [
        ("user", "创建投资日记：今天学习了定投策略，认为很适合工薪族")
    ]
})
```

### 场景5：市场监控

```
用户：帮我设置沪深300指数的估值预警，当PE超过15倍时提醒我

Agent：
1. 使用 setup_market_alert 配置预警
2. 设置估值阈值
3. 关联飞书通知
```

**示例代码：**
```python
# 设置市场预警
response = agent.invoke({
    "messages": [
        ("user", "设置沪深300指数PE>15时发送飞书预警")
    ]
})
```

## 工具直接调用

### 直接使用工具函数

```python
from tools.fund_data_tool import query_fund_data
from tools.sip_calculator_tool import calculate_sip_returns
from tools.report_generator_tool import generate_portfolio_pdf_report

# 查询基金数据
fund_info = query_fund_data("005827")
print(fund_info)

# 计算定投收益
sip_result = calculate_sip_returns(
    monthly_amount=2000,
    years=3,
    expected_return=8.0
)
print(sip_result)

# 生成报告
report_url = generate_portfolio_pdf_report(
    risk_level="中低风险",
    investment_period="3年",
    available_funds="20万",
    expected_return="6-8%",
    allocation_data='[{"fund_type": "债券基金", "allocation": "70%", "recommendation": "纯债基金", "reason": "稳健"}]'
)
print(report_url)
```

## 多轮对话示例

### 对话流程

```python
# 第一轮：收集用户信息
response1 = agent.invoke({
    "messages": [
        ("user", "我想配置基金组合")
    ]
})

# 第二轮：提供详细信息
response2 = agent.invoke({
    "messages": [
        ("user", "我是中低风险投资者，3年投资期，有20万资金")
    ]
})

# 第三轮：生成方案
response3 = agent.invoke({
    "messages": [
        ("user", "请给我详细的配置方案")
    ]
})

# 第四轮：生成报告
response4 = agent.invoke({
    "messages": [
        ("user", "生成PDF报告")
    ]
})

# 第五轮：设置提醒
response5 = agent.invoke({
    "messages": [
        ("user", "设置定投提醒和估值预警")
    ]
})
```

## 错误处理

```python
try:
    # 尝试查询基金
    result = query_fund_data("000000")  # 错误的基金代码
    
    if "Error" in result or "失败" in result:
        print("查询失败，请检查输入")
        
except Exception as e:
    print(f"系统错误: {str(e)}")
```

## 性能优化

### 批量查询

```python
from concurrent.futures import ThreadPoolExecutor

def batch_query_funds(fund_codes):
    """批量查询基金"""
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(query_fund_data, fund_codes))
    return results

# 使用
codes = ["005827", "110011", "000251", "161725", "001717"]
results = batch_query_funds(codes)
```

### 缓存结果

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query_fund_data(fund_code):
    """缓存基金查询结果"""
    return query_fund_data(fund_code)
```

## 最佳实践

1. **清晰表达需求**
   - 提供完整的信息（风险、期限、资金）
   - 明确具体的问题或任务

2. **逐步深入**
   - 先了解基本概念
   - 再深入具体方案
   - 最后生成报告或设置提醒

3. **及时确认**
   - 对配置方案进行确认
   - 调整不合适的部分
   - 再生成正式报告

4. **善用工具**
   - 工具会自动调用
   - 可以直接指定使用某个工具
   - 如："使用 web-search 查询易方达蓝筹精选"

5. **定期复盘**
   - 使用投资日记记录
   - 查询历史对话
   - 总结投资心得
