# M-A3 30-Agent集群 分阶段实施计划
> 版本：v1.0 | 日期：2026-04-14 | 作者：M-A3 幕僚长

---

## 一、实施策略

### 1.1 核心原则

| 原则 | 说明 |
|------|------|
| **先基础设施后业务** | Tier 0/1 Agent（调度/安全/记忆/数据）必须优先完成 |
| **先核心后扩展** | P0 Agent优先，P1次之，P2最后 |
| **并行开发** | 各域可同时开发，互不阻塞 |
| **可测试交付** | 每个Agent交付前必须通过质量基准测试 |
| **平滑灰度** | 新Agent逐步引入，不影响现有业务流程 |

### 1.2 阶段总览

```
Week 1-2   Phase 0: 基础设施层（10个Agent）
Week 3-4   Phase 1: GEO域 + 亚马逊域核心（10个Agent）
Week 5-6   Phase 2: GEO域 + 亚马逊域扩展（10个Agent）
Week 7-8   Phase 3: 全链路集成 + 压力测试
Week 9+    Phase 4: 持续优化 + 自进化增强
```

---

## 二、详细实施计划

### 📦 Phase 0：基础设施层（第1-2周）

**目标**：建立集群底座，确保后续Agent可靠运行

| # | Agent ID | Agent名称 | 优先级 | 预估工时 | 交付物 | 验收标准 |
|---|---------|---------|--------|---------|--------|---------|
| 1 | sup-09-scheduler | 调度协调Agent | P0 | 3天 | task_scheduler.py + DAG引擎 | 10个任务并行调度测试通过 |
| 2 | sup-10-security | 安全审计Agent | P0 | 3天 | security_audit.py + RBAC矩阵 | PII检测测试10/10通过 |
| 3 | sup-01-data-collect | 数据采集Agent | P0 | 3天 | data_collector.py + 适配器 | 3个数据源接入测试通过 |
| 4 | sup-08-memory | 记忆管理Agent | P1 | 2天 | memory_manager.py + RAG | 记忆检索准确率>85% |
| 5 | sup-02-content-gen | 内容生成Agent | P0 | 3天 | content_generator.py + 模板 | 批量生成质量评分>75分 |
| 6 | sup-04-compliance | 合规检查Agent | P0 | 2天 | compliance_checker.py | 10条合规规则测试通过 |
| 7 | sup-03-translation | 翻译Agent | P1 | 2天 | translator.py + 术语库 | 中英翻译质量评分>80 |
| 8 | sup-07-quality | 质量评分Agent | P1 | 2天 | quality_scorer.py | 与人工评分相关性>0.85 |
| 9 | geo-07-knowledge-graph | 知识图谱Agent | P0 | 3天 | knowledge_graph.py + JSON-LD | 实体识别准确率>90% |
| 10 | amz-09-keywords | 关键词Agent | P1 | 2天 | keyword_agent.py + 词库 | 关键词覆盖率>竞品1.5倍 |

**Phase 0 关键技术决策**：
```
✅ 调度引擎：基于Weighted Least Connections算法
✅ 安全架构：RBAC × Agent × 操作类型
✅ 数据管道：适配器模式，支持API/爬虫/文件
✅ 记忆系统：SQLite FTS5 + RAG语义检索
```

**Phase 0 风险评估**：
| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| 调度引擎并发死锁 | 中 | 高 | Phase 0第1个交付，深度测试 |
| 安全Agent误报阻塞正常请求 | 低 | 高 | 灰度10%流量，逐步放量 |
| 数据采集被反爬 | 中 | 中 | 多IP池 + 请求间隔 |

---

### 📊 Phase 1：核心业务Agent（第3-4周）

**目标**：交付GEO域和亚马逊域的核心P0 Agent，形成业务闭环

#### GEO域核心（5个）

| # | Agent ID | Agent名称 | 优先级 | 预估工时 | 交付物 | 验收标准 |
|---|---------|---------|--------|---------|--------|---------|
| 1 | geo-01-market-research | 市场研究Agent | P0 | 3天 | market_researcher.py + 报告模板 | TAM/SAM/SOM三层模型输出正确 |
| 2 | geo-03-content-strategy | 内容策略Agent | P0 | 3天 | content_strategist.py + 日历生成器 | 季度内容日历覆盖>200个话题 |
| 3 | geo-08-intent-prediction | 意图预测Agent | P1 | 2天 | intent_predictor.py | 意图分类准确率>85%（对标94.3%目标） |
| 4 | geo-02-competitor | 竞品分析Agent | P1 | 2天 | competitor_analyzer.py | GEO三维度评分可输出 |
| 5 | geo-06-monitoring | 效果监测Agent | P1 | 2天 | geo_monitor.py + 告警引擎 | AI搜索引用率追踪可用 |

#### 亚马逊域核心（5个）

| # | Agent ID | Agent名称 | 优先级 | 预估工时 | 交付物 | 验收标准 |
|---|---------|---------|--------|---------|--------|---------|
| 1 | amz-01-product-select | 选品分析Agent | P0 | 3天 | product_selector.py + 利润模型 | 选品报告覆盖Top10候选 |
| 2 | amz-02-listing | Listing优化Agent | P0 | 3天 | listing_optimizer.py | Listing评分>85分 |
| 3 | amz-03-profit | 利润优化Agent | P0 | 3天 | profit_optimizer.py + 决策树 | 预测准确率>80% |
| 4 | amz-04-ads | 广告投放Agent | P0 | 3天 | ads_manager.py + 竞价引擎 | ACOS优化建议可执行 |
| 5 | amz-05-inventory | 库存管理Agent | P1 | 2天 | inventory_manager.py | 补货计划表生成正确 |

**Phase 1 关键技术决策**：
```
✅ GEO意图预测：引入参考PureblueAI的意图分类模型
✅ 利润优化：使用ProfitOptimizer决策树算法
✅ 广告投放：基于TACOS导向的Bid调节算法
```

**Phase 1 业务闭环验证**：
```
用户输入：某消费电子新品 → 
GEO域：市场研究 → 竞品分析 → 内容策略 → 效果监测
亚马逊域：选品分析 → Listing优化 → 利润优化 → 广告投放
覆盖：产品上市前全链路
```

---

### 🚀 Phase 2：扩展Agent（第5-6周）

**目标**：交付所有剩余Agent，达到30个Agent完整覆盖

#### GEO域扩展（5个）

| # | Agent ID | Agent名称 | 优先级 | 预估工时 | 交付物 | 验收标准 |
|---|---------|---------|--------|---------|--------|---------|
| 1 | geo-04-multilingual | 多语言优化Agent | P1 | 2天 | multilingual_optimizer.py | 5个语种本地化完成 |
| 2 | geo-05-platform-adapt | 平台适配Agent | P1 | 2天 | platform_adapter.py | 知乎/CSDN/LinkedIn适配 |
| 3 | geo-09-schema | Schema优化Agent | P2 | 2天 | schema_optimizer.py | 全站Schema覆盖率>95% |
| 4 | geo-10-regional | 地域策略Agent | P2 | 2天 | regional_strategist.py | 4个区域差异化策略 |
| 5 | (整合Phase1) | - | - | - | GEO域工具链完善 | 全链路集成测试通过 |

#### 亚马逊域扩展（5个）

| # | Agent ID | Agent名称 | 优先级 | 预估工时 | 交付物 | 验收标准 |
|---|---------|---------|--------|---------|--------|---------|
| 1 | amz-06-review | 评价分析Agent | P1 | 2天 | review_analyzer.py + 情感分析 | 情感分析准确率>80% |
| 2 | amz-07-competitor-monitor | 竞品监控Agent | P1 | 2天 | competitor_monitor.py | 5个ASIN监控可用 |
| 3 | amz-08-pricing | 定价策略Agent | P1 | 2天 | pricing_strategist.py | 动态定价规则可配置 |
| 4 | amz-10-reporting | 报表分析Agent | P2 | 2天 | reporting_agent.py | 日/周/月报自动生成 |
| 5 | (整合Phase1) | - | - | - | 亚马逊域工具链完善 | 全链路集成测试通过 |

#### 支撑域扩展（2个）

| # | Agent ID | Agent名称 | 优先级 | 预估工时 | 交付物 | 验收标准 |
|---|---------|---------|--------|---------|--------|---------|
| 1 | sup-05-report-gen | 报告生成Agent | P1 | 2天 | report_generator.py + PPT模板 | Markdown/PDF/HTML/PPT四格式 |
| 2 | sup-06-customer-service | 客户服务Agent | P2 | 2天 | customer_service.py + 对话引擎 | FAQ自动回复准确率>85% |

**Phase 2 关键技术决策**：
```
✅ 多语言优化：文化适配引擎（非纯翻译）
✅ 竞品监控：实时爬虫 + 价格告警阈值
✅ 报告生成：ECharts可视化集成
```

---

### 🔧 Phase 3：全链路集成 + 压力测试（第7-8周）

**目标**：验证30个Agent的协同工作能力，确保生产级稳定性

#### 3.1 集成测试

| 测试场景 | 描述 | 预期结果 | 优先级 |
|---------|------|---------|--------|
| **GEO全链路** | 市场研究→竞品分析→内容策略→多语言→平台适配→效果监测 | 完整报告生成 | P0 |
| **亚马逊全链路** | 选品→Listing→利润→广告→库存→定价→报表 | 完整运营方案 | P0 |
| **跨域协作** | GEO市场研究 → 亚马逊选品（数据互通） | 选品报告包含GEO数据 | P0 |
| **P2P通信** | 10组跨Agent消息传递 | 消息可靠到达 | P0 |
| **降级测试** | Claude MA不可用 → Local → DeepSeek | 降级不影响核心功能 | P1 |
| **并发压测** | 50个并发请求，30个Agent | 无死锁，响应时间P95<5s | P0 |

#### 3.2 压力测试指标

```python
stress_test_scenarios = {
    "normal_load": {
        "concurrent_users": 50,
        "avg_tasks_per_user": 3,
        "expected_p95_latency_ms": 5000,
        "expected_error_rate": 0.01
    },
    "peak_load": {
        "concurrent_users": 200,
        "avg_tasks_per_user": 5,
        "expected_p95_latency_ms": 15000,
        "expected_error_rate": 0.05
    },
    "spike_load": {
        "concurrent_users": 500,
        "avg_tasks_per_user": 3,
        "expected_p95_latency_ms": 30000,
        "expected_error_rate": 0.10,
        "expected_queue_time_s": 120
    }
}
```

#### 3.3 安全压力测试

```
MCP协议漏洞扫描（43%风险覆盖）：
- 命令注入测试：防止恶意prompt注入
- 路径遍历测试：防止文件访问越界
- 凭证泄露测试：防止API Key暴露
- SSRF测试：防止内部服务探测
覆盖率目标：100%工具函数通过扫描
```

---

### 🌱 Phase 4：持续优化 + 自进化（第9周+）

**目标**：让集群具备自我优化能力

#### 4.1 自进化机制

```
learnings/
├── 2026-04-agent-failures/      # 失败经验
├── 2026-04-agent-successes/      # 成功规则
├── 2026-04-30-expansion/         # 扩展经验（本案）
└── agent_capability_matrix.md   # Agent能力矩阵

进化流程：
1. SUP-07质量评分持续监测
2. 低于基准触发learnings记录
3. SUP-08记忆管理归类整理
4. 定期（周）知识编译→Wiki
5. 月度Agent能力画像更新
```

#### 4.2 性能优化计划

| 优化项 | 目标 | 负责人 | 优先级 |
|--------|------|-------|--------|
| 调度算法优化 | P95延迟从5s→3s | SUP-09 | P1 |
| 缓存命中率提升 | 从30%→60% | SUP-08 | P1 |
| 意图预测模型升级 | 准确率85%→90% | GEO-08 | P1 |
| 成本优化 | Token消耗降低20% | 全部 | P2 |

#### 4.3 下一步扩展方向（2026 Q2-Q3）

| 方向 | Agent数量 | 说明 |
|------|----------|------|
| 供应链域 | 5个 | 采购/物流/生产/质检/溯源 |
| 客服域 | 5个 | 多语言客服/投诉处理/退款/工单/回访 |
| 财务域 | 5个 | 成本分析/税务/汇率/预算/审计 |
| **潜在新增** | **15个** | 45个Agent集群 |

---

## 三、交付物清单

### 3.1 文档交付物

| 文件路径 | 说明 | 阶段 | 状态 |
|---------|------|------|------|
| `30-expansion/30-agents-design.md` | 30个Agent完整设计方案 | Phase 0 | ✅ 已完成 |
| `30-expansion/agent_registry.yaml` | Agent注册表配置 | Phase 0 | ✅ 已完成 |
| `30-expansion/IMPLEMENTATION_PLAN.md` | 分阶段实施计划 | Phase 0 | ✅ 已完成 |
| `30-expansion/agent_protocol.md` | Agent通信协议规范 | Phase 0 | 📋 待交付 |
| `30-expansion/test_benchmark.md` | Agent质量基准测试集 | Phase 1 | 📋 待交付 |

### 3.2 代码交付物

```
agent-cluster/
├── agents/
│   ├── geo/
│   │   ├── geo-01-market-research/
│   │   ├── geo-02-competitor/
│   │   ├── geo-03-content-strategy/
│   │   ├── geo-04-multilingual/
│   │   ├── geo-05-platform-adapt/
│   │   ├── geo-06-monitoring/
│   │   ├── geo-07-knowledge-graph/
│   │   ├── geo-08-intent-prediction/
│   │   ├── geo-09-schema/
│   │   └── geo-10-regional/
│   ├── amazon/
│   │   ├── amz-01-product-select/
│   │   ├── amz-02-listing/
│   │   ├── amz-03-profit/
│   │   ├── amz-04-ads/
│   │   ├── amz-05-inventory/
│   │   ├── amz-06-review/
│   │   ├── amz-07-competitor-monitor/
│   │   ├── amz-08-pricing/
│   │   ├── amz-09-keywords/
│   │   └── amz-10-reporting/
│   └── support/
│       ├── sup-01-data-collect/
│       ├── sup-02-content-gen/
│       ├── sup-03-translation/
│       ├── sup-04-compliance/
│       ├── sup-05-report-gen/
│       ├── sup-06-customer-service/
│       ├── sup-07-quality/
│       ├── sup-08-memory/
│       ├── sup-09-scheduler/
│       └── sup-10-security/
```

---

## 四、里程碑

| 里程碑 | 日期 | 交付内容 | 成功标准 |
|--------|------|---------|---------|
| M1 | Week 2末 | Phase 0完成 | 10个基础设施Agent可用 |
| M2 | Week 4末 | Phase 1完成 | 20个Agent，覆盖核心业务 |
| M3 | Week 6末 | Phase 2完成 | 30个Agent全部就绪 |
| M4 | Week 8末 | Phase 3完成 | 全链路测试通过，压力测试达标 |
| M5 | Week 10末 | Phase 4上线 | 自进化机制运行，知识库积累 |

---

## 五、资源预算

### 5.1 开发工作量

| 阶段 | Agent数量 | 开发天数 | 人力投入 |
|------|----------|---------|---------|
| Phase 0 | 10 | 14天 | 2人并行 |
| Phase 1 | 10 | 14天 | 2人并行 |
| Phase 2 | 10 | 14天 | 2人并行 |
| Phase 3 | 集成 | 14天 | 2人并行 |
| **总计** | **30** | **56天** | **约4人月** |

### 5.2 成本估算

| 成本项 | 月度成本 | 说明 |
|--------|---------|------|
| Claude MA API | ¥2,000-5,000 | 按量付费，Phase 0-1高消耗 |
| DeepSeek API | ¥500-1,000 | Phase 0-2消耗 |
| 云服务器 | ¥1,000-2,000 | 4核8G起步 |
| 数据存储 | ¥200-500 | SQLite + OSS |
| **月度合计** | **¥3,700-8,500** | |

---

*本计划由 M-A3 幕僚长 制定*
*版本 v1.0 | 2026-04-14*
*下一步行动：启动 Phase 0 开发*
