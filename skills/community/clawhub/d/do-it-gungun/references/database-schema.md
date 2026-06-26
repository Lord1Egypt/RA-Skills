# do-it 决策数据库结构

**版本：** 1.0.0  
**创建日期：** 2026-03-15  
**用途：** 为 do-it 技能提供客观数据支撑

---

## 📊 数据库 Schema

### 1. 职业选择库 (career_choices)

```json
{
  "industry_salary": {
    "industry": "行业名称",
    "role": "职位",
    "city": "城市",
    "experience_years": "工作年限",
    "salary_min": "最低薪资",
    "salary_median": "中位数薪资",
    "salary_max": "最高薪资",
    "sample_size": "样本数量",
    "data_source": "数据来源",
    "updated_at": "更新时间"
  },
  "city_development": {
    "city": "城市",
    "gdp_growth": "GDP 增长率",
    "population_inflow": "人口净流入",
    "industry_clusters": "产业集群",
    "policy_support": "政策支持",
    "living_cost_index": "生活成本指数",
    "development_score": "发展评分 (1-10)",
    "data_source": "数据来源",
    "updated_at": "更新时间"
  },
  "career_age_curve": {
    "role": "职位",
    "age_range": "年龄段",
    "avg_salary": "平均薪资",
    "promotion_rate": "晋升率",
    "turnover_rate": "跳槽率",
    "peak_age": "黄金年龄",
    "decline_age": "下滑年龄",
    "data_source": "数据来源"
  },
  "job_hopping_success": {
    "from_industry": "原行业",
    "to_industry": "目标行业",
    "experience_years": "工作年限",
    "success_rate": "成功率",
    "avg_salary_change": "薪资变化%",
    "common_barriers": "常见障碍",
    "data_source": "数据来源"
  }
}
```

---

### 2. 感情问题库 (relationships)

```json
{
  "relationship_psychology": {
    "issue_type": "问题类型",
    "research_summary": "研究摘要",
    "success_factors": "成功因素",
    "risk_factors": "风险因素",
    "recommended_actions": "建议行动",
    "success_rate": "成功率",
    "data_source": "数据来源"
  },
  "marriage_statistics": {
    "region": "地区",
    "divorce_rate": "离婚率",
    "avg_marriage_age": "平均结婚年龄",
    "remarriage_rate": "再婚率",
    "common_causes": "常见原因",
    "data_source": "数据来源"
  }
}
```

---

### 3. 投资决策库 (investments)

```json
{
  "investment_returns": {
    "asset_type": "资产类型",
    "time_period": "时间周期",
    "avg_return": "平均回报",
    "max_drawdown": "最大回撤",
    "volatility": "波动率",
    "sharpe_ratio": "夏普比率",
    "data_source": "数据来源"
  },
  "industry_cycle": {
    "industry": "行业",
    "cycle_stage": "周期阶段",
    "growth_rate": "增长率",
    "risk_level": "风险等级",
    "recommended_action": "建议行动",
    "data_source": "数据来源"
  }
}
```

---

### 4. 生活选择库 (life_choices)

```json
{
  "city_comparison": {
    "city": "城市",
    "housing_price": "房价 (元/㎡)",
    "avg_rent": "平均租金",
    "education_score": "教育评分",
    "healthcare_score": "医疗评分",
    "transportation_score": "交通评分",
    "environment_score": "环境评分",
    "overall_score": "综合评分",
    "data_source": "数据来源"
  },
  "cost_of_living": {
    "city": "城市",
    "food_cost": "饮食成本",
    "transport_cost": "交通成本",
    "education_cost": "教育成本",
    "healthcare_cost": "医疗成本",
    "total_monthly": "月总成本",
    "data_source": "数据来源"
  }
}
```

---

### 5. 案例复盘库 (case_reviews)

```json
{
  "case_record": {
    "case_id": "案例 ID",
    "user_profile": "用户画像",
    "problem_type": "问题类型",
    "options": "可选方案",
    "recommendation": "推荐选择",
    "reasoning": "判断理由",
    "decision_date": "决策日期",
    "follow_up_date": "跟进日期",
    "outcome": "实际结果",
    "user_satisfaction": "用户满意度",
    "accuracy_score": "准确率评分",
    "lessons_learned": "经验教训"
  }
}
```

---

## 🔄 数据更新机制

### 自动更新

```yaml
daily:
  - 股票/基金回报率
  - 汇率数据
  
weekly:
  - 招聘网站薪资数据
  - 行业新闻/趋势
  
monthly:
  - 城市生活成本
  - 行业报告
  
quarterly:
  - 统计局数据
  - 智库报告
  
yearly:
  - 人口普查数据
  - 学术研究更新
```

### 数据来源优先级

```
1. 官方数据 (统计局/教育部/卫健委) - 最高优先级
2. 权威机构 (智库/研究院) - 高优先级
3. 商业平台 (招聘网站/金融机构) - 中优先级
4. 用户反馈 (案例复盘) - 持续积累
```

---

## 📈 数据使用方式

### 判断流程

```
用户输入问题
    ↓
识别问题类型 (职业/感情/投资/生活)
    ↓
调用对应数据库
    ↓
数据对比分析
    ↓
结合用户具体情况
    ↓
输出判断建议
    ↓
记录案例到复盘库
    ↓
后续跟进结果
    ↓
优化判断模型
```

### 权重设计

| 因素 | 权重 | 说明 |
|------|------|------|
| 客观数据 | 50% | 薪资/成本/成功率等硬数据 |
| 用户情况 | 30% | 个人条件/偏好/约束 |
| 案例经验 | 15% | 历史类似案例结果 |
| 滚滚直觉 | 5% | 无法量化的因素 |

---

## 🎯 数据质量要求

### 准确性
- 官方数据优先
- 多源交叉验证
- 标注数据来源

### 时效性
- 标注数据时间
- 过期数据提醒
- 定期更新机制

### 完整性
- 样本数量要求
- 覆盖主要城市/行业
- 持续补充缺口

---

## 📋 实施计划

### 阶段 1：MVP (1 个月)
- [ ] 职业选择库基础数据
- [ ] 主要城市薪资数据
- [ ] 10 个案例积累

### 阶段 2：完善 (3 个月)
- [ ] 全部 5 个数据库
- [ ] 自动更新机制
- [ ] 50 个案例积累

### 阶段 3：产品化 (6 个月)
- [ ] Web/H5 界面
- [ ] 用户反馈系统
- [ ] 100+ 案例积累
- [ ] 准确率统计

---

## 💡 核心原则

1. **数据驱动，不是数据唯一** - 数据是基础，但要结合用户具体情况
2. **透明可追溯** - 每个判断都有数据来源
3. **持续优化** - 案例复盘反哺数据库
4. **用户隐私** - 脱敏处理，保护用户信息

---

**创建人：** 滚滚 & 地球人  
**创建时间：** 2026-03-15  
**状态：** 🚀 设计完成，等待实施
