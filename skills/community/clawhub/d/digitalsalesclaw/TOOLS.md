# DigitalSalesClaw 工具手册

## 架构

MySQL 统一数据源，所有工具通过 `db.get_conn()` 访问。

工具目录：`~/.openclaw/workspace/skills/digitalsalesclaw/tools/`

---

## 对话与推理

### ask

理解用户问题，路由到对应数据模块，返回结构化结果。

支持自然语言筛选：`"douyin 上 pending 的选题"` → 自动解析为 `platform=douyin status=pending`

---

## 内容

### content

脚本生成、钩子生成、批量流水线、内容优化。

钩子库：5种风格 × 22条模板，支持语义相似度过滤避免重复。

### topic_recommend

选题推荐：热点追踪 + 季节性 + 竞品空白点。

### hook_generator

5种风格独立生成：提问式 / 故事式 / 数据式 / 对比式 / 情绪式。

### content_predict

内容效果预测，标题评分。

### trend_aware_content

热点监控、季节性规划、竞品内容分析。

### ad_optimization

广告出价建议、预算分配、关键词扩展。

---

## 合规

### compliance

语义优先审核架构：

1. **语义实体提取**：识别疾病域、药品类别、疗效声明类型
2. **Guardrail 兜底**：8条绝对禁区规则，拦截明显违规
3. **AI 推理证据链**：为 Agent 生成 Chain-of-Thought 判断引导

输出结构：`semantic_entities` + `guardrail_results` + `evidence_for_ai` + `ai_reasoning_prompt`

规则编码：`{类型}-{大类}-{序号}`，如 `GA-A-001`（广告法-绝对化用语-第1条）

### compliance_audit

审核状态机：draft → pending → approved → published，每步记录审计日志。

### compliance_hierarchy

合规规则管理：查询三层编码详情，按法规类型分组。

---

## 患者

### patient

会话管理、随访 SOP、工单升级流程。

### patient_segmentation

智能分群 + 风险评估 + 干预计划。

### patient_journey

统一患者旅程事件模型，整合触点数据和转化事件。

### attribution

6种归因模型（first_touch / last_touch / linear / time_decay / position_based / data_driven），支持 CAC/LTV 分析。

---

## 药房与供应链

### pharmacy

库存状态监控、低库存告警。

### supply_chain

采购订单创建、审批、物流跟踪。

### supply_chain_state

供应链状态机：pending → approved → ordered → shipped → received → stocked。

### drug_ontology

药品统一本体，药品-疾病关联，品类分析。

---

## 竞品与 KOL

### competitor

竞品数据、价格监控、评分追踪。

### kol_matching

KOL 智能匹配，支持内容类型 × 平台 × 预算筛选。

### doctor

医生档案、拜访记录、影响力评分。

### persona_identity

医生-KOL 统一身份管理，跨平台去重。

---

## 分析与监控

### analytics

运营看板：内容/患者/合规多维分析，支持 7d / 14d / 30d / 90d 周期。

### smart_analytics

Z-score 异常检测，覆盖内容效果、患者活跃度、库存三个维度。

### goal_decomposer

战略目标 → 战术分解 → 可执行任务三层分解。

### self_reflection

历史决策回顾，失败模式分析，持续改进机制。

---

## 流程与协作

### engine

条件执行引擎，支持 if / for / while / retry，预定义7个工作流模板。

### triggers

数据阈值触发器，集成 smart_analytics 异常结果，支持钉钉告警。

### orchestrate

多 Agent 协作编排，任务分解与并行执行。

---

## 知识

### knowledge_qa

医药知识库检索（jieba 分词 + TF-IDF），支持法规条款、药品信息、临床指南。
