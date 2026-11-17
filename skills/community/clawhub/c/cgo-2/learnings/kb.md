# AI CGO Knowledge Base

> 版本：1.0 | 最后更新：2026-06-14
> 本文件由 Optimization Protocol 自动维护

## 成功模式

### PLG + AI Feature Gate
- **适用场景**：SaaS 产品，用户量 > 1w MAU，有免费版
- **关键决策点**：将 AI 功能作为免费版的限制功能（如每月 10 次 AI 分析），付费解锁更高配额
- **产出效果**：免费→付费转化率提升 2-3x，同时 AI 调用成本可控
- **来源**：通用 SaaS 增长模式

### AI SDR 自动跟进
- **适用场景**：B2B，销售线索量 > 500/月，CRM 系统完善
- **关键决策点**：AI 自动发送个性化 follow-up 邮件，基于用户行为（打开/点击/访问页面）触发不同话术
- **产出效果**：线索→SQL 转化率提升 30-50%，SDR 人力成本降低 60%
- **来源**：通用 B2B 增长模式

### 增长实验自动化
- **适用场景**：growth team > 3 人，每月实验 > 10 个
- **关键决策点**：AI 自动分析 A/B 测试结果，当置信度 > 95% 时自动推送胜出变体
- **产出效果**：实验周期从 2 周缩短到 3 天，实验吞吐量提升 4x
- **来源**：通用增长工程模式

## 失败模式

### 跳过 PMF 直接做增长
- **失败环节**：框架不匹配
- **用户反馈**：用户要求增长策略，但产品尚未验证 PMF
- **归因分析**：增长策略假设产品有稳定留存基础，PMF 未验证前做增长只会加速流失
- **改进建议**：在 Pre-flight Check 中强化 PMF 验证步骤，未通过 PMF 时自动输出验证框架而非增长计划
- **来源**：Skill 设计时已预判

### 假设 CAC 数据缺失
- **失败环节**：假设偏差
- **用户反馈**：推荐策略基于错误的 CAC 假设
- **归因分析**：用户未提供 CAC/LTV 数据时，默认使用了行业均值，但实际偏差 > 3x
- **改进建议**：缺少 CAC 时强制要求用户提供，不假设行业均值
- **来源**：Skill 设计时已预判

## 行业基准

### B2B SaaS
- **CAC 范围**：$500 - $5,000（依客单价而异）
- **LTV/CAC 比率**：> 3x（健康），> 5x（优秀）
- **Payback Period**：< 12 个月
- **Gross Margin**：70-85%
- **数据来源**：OpenView SaaS Benchmarks, KeyBanc SaaS Survey
- **更新日期**：2025-Q4

### B2C SaaS (订阅制)
- **CAC 范围**：$20 - $200
- **LTV/CAC 比率**：> 3x
- **Payback Period**：< 6 个月
- **Gross Margin**：60-80%
- **数据来源**：Recurly Research, ProfitWell
- **更新日期**：2025-Q4

### E-commerce
- **CAC 范围**：$10 - $100（受客单价、渠道影响大）
- **LTV/CAC 比率**：> 2x（DTC 品牌健康线）
- **Payback Period**：< 3 个月（电商回本周期短）
- **Gross Margin**：40-60%
- **数据来源**：Shopify Benchmarks, SimulStats
- **更新日期**：2025-Q4

## 增长策略模式库

### SEO Content Cluster 策略
- **适用阶段**：growth
- **适用行业**：B2B SaaS, Content-heavy 产品
- **AARRR 阶段**：Acquisition
- **AI 改造点**：AI 批量生成 Cluster 内容初稿 + AI 自动内链优化 + AI 分析搜索排名 Gap
- **预期效果**：6 个月内 Organic Traffic 增长 3-5x
- **来源**：通用 SEO 增长策略

### 用户激活 Onboarding 序列
- **适用阶段**：early / growth
- **适用行业**：SaaS（特别是工具型产品）
- **AARRR 阶段**：Activation
- **AI 改造点**：AI 分析用户行为 → 动态调整 Onboarding 步骤 → 个性化功能推荐
- **预期效果**：Activation Rate 提升 20-40%
- **来源**：通用 SaaS 增长策略

## 变更日志

| 日期 | 版本 | 变更内容 |
|------|------|---------|
| 2026-06-14 | 1.0 | 初始化：种子数据填充 |
| 2026-06-12 | 0.1 | 创建知识库结构（空模板） |
