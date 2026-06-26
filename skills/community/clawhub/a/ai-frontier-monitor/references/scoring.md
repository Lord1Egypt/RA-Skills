# 评分体系参考

## 自动评分关键词

### 企业落地 (0-2.5 分，权重 40%)
enterprise, customer, business, production, deployment, case study,
company, organization, roi, revenue, savings, scale, regulated, industry, copilot,
automate, automates, streamline, boost, productivity,
available on, built with, powered by, how we used,
企业, 客户, 落地, 部署, 案例, 行业, 转型, 自动化, 提效

额外加分: 标题含 "used"/"deployed"/"built with" → +0.5

### 数据支撑 (0-1.5 分，权重 20%)
%, percent, x faster, x cheaper, reduced, increased, improved,
saved, cost, efficiency, accuracy, latency, benchmark,
million, billion, thousand,
量化, 效率, 成本

### 可学习性 (0-1 分，权重 20%)
how we, architecture, methodology, best practice, lesson,
framework, pattern, approach, strategy, pipeline, workflow,
方法论, 架构, 最佳实践, 经验, 教训

### 前沿性 (0-1 分，权重 20%)
first, new, launch, announce, breakthrough, novel,
open source, open-source, release, preview, beta,
now available, come to, general availability,
首次, 发布, 开源, 突破, 新品

### 来源加分
- OpenAI/AWS: +1.0 (官方博客，落地案例多)
- Techmeme: +0.5 (聚合新闻)
- Product Hunt / HN Show: +0.3

## 动态分层逻辑

分数并非硬编码阈值，而是基于当日实际分数分布动态调整：

- 核心情报阈值 = max(3.5, 最高分 × 0.8)
- 值得关注阈值 = max(2.5, 最高分 × 0.5)
- 快速浏览 = 1.0 ~ 值得关注阈值

## 信号检测关键词

### 资本信号
series, funding, raised, invest, 投资, 融资, million, billion,
估值, 融资轮, 收购, acquire, merger, 并购, IPO, 上市,
seed, round, valuation, capital

### 产品信号
launch, release, announce, general availability, GA,
preview, beta, open source, open-source,
产品, 发布, 上线, 开源, 首发, 推出, 大模型, model

### 技术信号
model, architecture, training, inference, benchmark,
framework, sota, state-of-the-art, breakthrough,
fine-tun, rag, agent, mcp, tool use, reasoning,
multimodal, diffusion, transformer, rlhf, dpo,
spec, protocol, standard,
技术, 架构, 推理, 微调, 多模态
