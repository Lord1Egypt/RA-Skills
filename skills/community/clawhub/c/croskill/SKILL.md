# 首席风险官Agent技能

## 技能概述

这是一个专为AI Agent设计的首席风险官技能，帮助企业识别、评估和管理各类风险。

## 功能特性

### 核心功能

1. **风险评估**
   - 支持多种风险类型：市场风险、信用风险、操作风险等
   - 基于企业信息和风险因素进行综合评估
   - 生成风险等级和风险评分

2. **影响分析**
   - 评估风险对财务、声誉和运营的影响
   - 提供量化的风险影响范围

3. **建议生成**
   - 根据风险等级生成针对性的应对建议
   - 支持高、中、低不同风险级别的处理方案

## 使用方法

### 输入参数

```python
{
    "risk_type": "市场风险",  # 风险类型
    "company_info": {
        "name": "测试企业",
        "industry": "金融",
        "size": "大型"
    },
    "risk_factors": ["利率波动", "汇率风险", "竞争对手行动"]
}
```

### 输出结果

```python
{
    "status": "success",
    "risk_type": "市场风险",
    "assessment": {
        "risk_level": "高",
        "risk_score": 85,
        "identified_risks": ["利率波动", "汇率风险", "竞争对手行动"],
        "impact_analysis": {
            "financial": "可能导致10-20%的收入损失",
            "reputational": "可能影响企业品牌形象",
            "operational": "可能导致业务中断"
        }
    },
    "recommendations": [
        "立即启动应急预案",
        "建立风险监控指标",
        "定期进行压力测试",
        "寻求专业咨询服务"
    ]
}
```

## 技术规格

- **语言**: Python 3.8+
- **依赖**: 无外部依赖
- **版本**: 1.0.0
- **作者**: AI Agent

## 部署方式

### 本地使用

```python
from cro_skill import ChiefRiskOfficerSkill

# 创建技能实例
cro_skill = ChiefRiskOfficerSkill()

# 执行风险评估
result = cro_skill.execute({
    "risk_type": "市场风险",
    "company_info": {
        "name": "测试企业",
        "industry": "金融",
        "size": "大型"
    },
    "risk_factors": ["利率波动", "汇率风险", "竞争对手行动"]
})

print(result)
```

### ClawHub发布

```bash
# 登录ClawHub
npx clawhub login

# 发布技能
npx clawhub publish . --name "首席风险官" --version "1.0.0" --tags "风险,管理,合规,监控"
```

## 应用场景

- 企业风险管理部门日常风险评估
- 投资决策前的风险分析
- 合规审计中的风险识别
- 业务连续性规划

## 版本历史

- **1.0.0** (2026-03-13): 初始版本，实现核心风险评估功能