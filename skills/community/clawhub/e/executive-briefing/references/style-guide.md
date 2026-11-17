# 高管语态手册

## 核心理念

**"交付判断，不交付活动。"**

高管不关心你做了什么过程，只关心结果意味着什么、需要做什么决策。

---

## 中文写作规范

### 结论前置（BLUF）

| ❌ 错误 | ✅ 正确 |
|--------|--------|
| 根据过去三个月的调研，我们分析了47个采购品类，发现其中12个品类存在成本优化空间。 | 采购成本可在12个月内降低1200万元。 |

### 技术术语 → 业务影响

| ❌ 技术语言 | ✅ 业务语言 |
|-----------|-----------|
| 完成微服务架构拆分，将单体应用解耦为23个微服务 | 系统稳定性提升40%，故障恢复时间从2小时缩短至5分钟 |
| 接入Kubernetes集群，实现容器化部署 | 资源利用率从35%提升至72%，每年节省服务器成本约80万 |
| 完成数据中台建设，打通ERP/CRM/WMS三套系统 | 跨部门数据获取时间从3天缩短至实时，决策效率显著提升 |

### 过程描述 → 结果呈现

| ❌ 过程描述 | ✅ 结果呈现 |
|-----------|-----------|
| 我们组织了5次跨部门协调会，访谈了12位业务负责人，收集了87条需求 | 确认了3个关键痛点：交付延期率18%、库存周转天数超行业均值2.3倍、客户投诉中43%与配送时效相关 |
| 经过反复论证和多轮方案评审 | 最终方案（方案C）预期ROI为310%，12个月内回本 |

### 建议格式

| ❌ 模糊建议 | ✅ 明确建议 |
|-----------|-----------|
| 建议考虑优化采购流程 | 建议在Q3完成电子采购平台上线，预计年省1200万。由采购部张总负责，9月30日前上线 |
| 可以考虑增加客服人力 | 建议Q4新增6名客服（成本约36万/年），目标将首次响应时间从15分钟降至3分钟以内 |

---

## 英文写作规范

### Avoid passive voice

| ❌ Passive | ✅ Active |
|-----------|---------|
| It is recommended that the platform be migrated | We recommend migrating the platform |
| Issues were identified during the audit | The audit identified three issues |
| The budget has been approved | The CFO approved the budget |

### Kill adverbs

Remove unless they carry specific meaning:
- ~~significantly~~ → show the number
- ~~potentially~~ → state the probability
- ~~approximately~~ → give the range
- ~~basically~~ → delete
- ~~essentially~~ → delete

---

## 通用铁律

1. **第一句就是结论** — 不铺垫、不介绍背景、不说"我们分析了…"
2. **数字说话** — 能量化绝不用形容词
3. **短句原则** — 每句不超过30字（中文）/ 20词（英文）
4. **一页一主题** — 每段只讲一个点，讲完就结束
5. **附录分离** — 详细数据/方法论/技术细节放附录
6. **先确认受众** — CFO读法和Board读法不同，CEO有上下文和steering committee第一次见面也不同
7. **不发明数字** — 源材料没有的数据绝对不编，宁可标注"待确认"

---

## 受众分层指南

| 受众 | 关注重点 | 篇幅建议 | 语言风格 |
|------|---------|---------|---------|
| CEO | 战略方向、竞争格局、增长机会 | ≤3分钟 | 宏观、趋势、决策导向 |
| CFO | 投资回报、成本影响、财务风险 | ≤3分钟 | 数字、ROI、风险量化 |
| Board of Directors | 治理合规、重大风险、长期价值 | ≤5分钟 | 正式、全面、可追溯 |
| Steering Committee | 项目进度、里程碑、资源需求 | ≤5分钟 | 结构化、对比、里程碑 |

---

*参考来源：Anthropic Executive Briefing / zhasty007 Executive Summary / Recipe-060*
