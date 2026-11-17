# 端云成本优化（V7 核心）

> V7 通过「元数据级交互 + 端侧重计算」实现云端成本降低 80% 的目标。

## 1. 设计目标

### 1.1 量化指标
- **单次请求成本**：< $0.001（对比 V6 平均 $0.05，降低 80%）
- **月度累计成本**：< $10（约 10,000 次请求）
- **预算告警阈值**：50% 黄色 / 80% 红色 / 100% 熔断
- **成本可追溯**：每次请求精确到 $0.0001

### 1.2 核心策略
1. **元数据级交互**：abstract_data < 10KB（V6 中等体积数据 → V7 元数据）
2. **端侧重计算**：OCR/ASR/TTS/RAG 全部本地，零云端成本
3. **缓存复用**：相同 abstract_data 命中缓存，命中率 > 40%
4. **降级机制**：5 级降级，预算紧张时自动切换到纯端侧模式

## 2. 5 级成本分级

| 级别 | 名称 | 月度成本 | 适用场景 | 决策位置 |
|------|------|----------|----------|----------|
| L0 | Free | $0 | 纯端侧（无云端调用） | 端侧 |
| L1 | Lite | < $1 | 个人教师备课（< 1000 请求/月） | 云端轻 |
| L2 | Standard | $1~$5 | 教研组协作（1000~5000 请求/月） | 云端中 |
| L3 | Pro | $5~$10 | 学校级部署（5000~10000 请求/月） | 云端重 |
| L4 | Enterprise | 定制 | 区/市级 SaaS（> 10000 请求/月） | 云端专属 |

## 3. 成本监控仪表盘

### 3.1 实时指标
```prometheus
# 单次请求成本
v7_request_cost_usd{request_id="uuid"} 0.0008

# 月度累计成本
v7_cumulative_cost_usd 3.2456

# 预算使用率
v7_budget_usage_ratio 0.32

# 缓存命中率
v7_cache_hit_ratio 0.45
```

### 3.2 成本趋势
- **按日/周/月粒度**查看成本曲线
- **按 task_type 分组**：pedagogy_recommendation / courseware_design / learning_path_planning / assessment_analysis / content_creation
- **按 decision_type 分组**：creative / analytical / educational / strategic

## 4. 4 种降本策略

### 4.1 缓存（Cache）
- **键**：abstract_data 的 SHA256 哈希
- **TTL**：7 天（与数据保留期一致）
- **存储**：端侧 IndexedDB（零云端存储成本）
- **命中率目标**：> 40%

### 4.2 压缩（Compress）
- abstract_data 从原始 JSON 压缩为 < 5KB
- 超出 10KB 自动截断 + 警告（V7 §4.1，E002）
- 详见 `references/edge-cloud-protocol.md` §4.1

### 4.3 降级（Degrade）
| 级别 | 触发条件 | 行为 | 成本 |
|------|----------|------|------|
| L1 | 正常 | 云端 LLM 完整决策 | $0.001 |
| L2 | 云端慢（> 5s） | max_tokens 250 | $0.0005 |
| L3 | 云端不可用 | 端侧 LLM（Qwen-1.5B） | $0 |
| L4 | 端侧 LLM 不可用 | 规则 + 模板 | $0 |
| L5 | 全部不可用 | 完全本地 + 提示用户 | $0 |

### 4.4 批量（Batch）
- 短任务自动批处理（如多个 OCR 请求合并）
- 端侧 NPU 批量推理，减少云端调用次数
- 详见 `references/npu-scheduling-guide.md` §5.3

## 5. 智能预算告警

### 5.1 三级告警
| 阈值 | 级别 | 行为 |
|------|------|------|
| 50% | 黄色警告 | 仪表盘标记 + 日志记录 |
| 80% | 红色警告 | 通知管理员 + 限制非必要请求（max_tokens 减半） |
| 100% | 自动熔断 | 切换到 L3~L5 降级模式 + 邮件/IM 通知 |

### 5.2 熔断恢复
- 管理员手动解除（不可自动恢复，防止成本失控）
- 解除后重置月度计数器
- 熔断事件记录到审计日志

## 6. 成本审计日志

### 6.1 日志格式
```json
{
  "timestamp": "2026-08-15T10:00:00Z",
  "request_id": "uuid",
  "provider": "openai",
  "model": "gpt-4o-mini",
  "task_type": "pedagogy_recommendation",
  "decision_type": "educational",
  "tokens_in": 350,
  "tokens_out": 200,
  "cost_usd": 0.0008,
  "cumulative_cost_usd": 3.2456,
  "cache_hit": false,
  "degradation_level": 1
}
```

### 6.2 审计要求
- 每次云端调用必须记录成本（精确到 $0.0001）
- 成本日志与 ZUP 审计日志关联（通过 request_id）
- 日志可导出 CSV/JSON
- 保留期 30 天（与云端元数据保留期一致）

## 7. 实现脚本

| 脚本 | 作用 |
|------|------|
| `scripts/cost_monitor.py` | 累计追踪 + 3 级告警 + 自动熔断 |
| `scripts/edge_cloud_dispatch.py` | 每次交换注入 cost_usd + cumulative_cost_usd |
| `references/edge-cloud-protocol.md` §4.5 | 协议层成本约束定义 |
| `references/edge-cloud-protocol-schema.json` | cost_usd 字段 schema |

## 8. 检查清单

部署 V7 成本优化前必查：

- [ ] `cost_monitor.py` 已实例化并注入 EdgeCloudClient
- [ ] 月度预算已配置（默认 $10）
- [ ] 50%/80%/100% 三级告警阈值已生效
- [ ] 100% 触发自动熔断切换 L3 降级
- [ ] 缓存机制已启用（IndexedDB）
- [ ] 成本审计日志可导出
- [ ] 单次请求成本 ≤ $0.001
- [ ] 月度累计成本 ≤ $10

---

> **总结**：V7 通过「元数据级交互 + 端侧重计算 + 5 级降级 + 智能预算告警」四重保障，在保持教学创新能力的同时将云端成本降低 80%，实现"跑得便宜"的核心价值。
