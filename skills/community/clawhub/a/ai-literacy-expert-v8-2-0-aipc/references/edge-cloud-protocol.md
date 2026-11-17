# 端云协同协议 v1.0（Edge-Cloud Protocol v1.0）

> V7 定义的端云交互标准化协议：所有 Skill 必须遵守的 JSON Schema。

## 1. 协议概述

### 1.1 设计目标
1. **标准化**：所有 AI PC Skill 端云交互统一格式
2. **可审计**：每次交互都有 ZUP（零上传证明）记录
3. **可降级**：本地故障 / 云端故障自动降级
4. **可计量**：每次交互成本可计算

### 1.2 协议版本
- **当前版本**：1.0
- **向后兼容**：是
- **协议路径**：`/api/v1/edge-cloud/exchange`

## 2. 请求结构（6 段）

```json
{
  "protocol_version": "1.0",
  "request_id": "uuid",
  "timestamp": "2026-08-15T10:00:00Z",
  "source": "edge-ai-pc",
  "intent": "教学策略推荐",
  "abstract": {
    "task_type": "pedagogy_recommendation",
    "context": "高一信息技术 · 期中复习",
    "abstract_data": "<10KB",
    "pii_detected": false,
    "data_classification": "anonymous"
  },
  "request": {
    "decision_type": "creative",
    "max_tokens": 500,
    "max_cost_usd": 0.001
  },
  "callback": {
    "edge_execution": true,
    "save_to_local": true
  }
}
```

### 2.1 字段详解

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `protocol_version` | string | ✅ | 协议版本号 |
| `request_id` | string | ✅ | 请求唯一 ID（UUID v4）|
| `timestamp` | string | ✅ | ISO 8601 时间戳 |
| `source` | string | ✅ | 发起方（如 `edge-ai-pc`）|
| `intent` | string | ✅ | 意图描述（人类可读）|
| `abstract.task_type` | string | ✅ | 任务类型（见 3.1）|
| `abstract.context` | string | ✅ | 上下文描述 |
| `abstract.abstract_data` | object | ✅ | 抽象元数据（< 10KB）|
| `abstract.pii_detected` | boolean | ✅ | PII 检测结果 |
| `abstract.data_classification` | string | ✅ | 数据分类 |
| `request.decision_type` | string | ✅ | 决策类型（见 3.2）|
| `request.max_tokens` | number | ✅ | 最大生成 token 数 |
| `request.max_cost_usd` | number | ✅ | 最大成本（美元）|
| `callback.edge_execution` | boolean | ✅ | 是否在端侧执行 |
| `callback.save_to_local` | boolean | ✅ | 是否保存到本地 |

## 3. 4 大决策类型

### 3.1 按任务类型分类
| task_type | 描述 | 示例 |
|-----------|------|------|
| `pedagogy_recommendation` | 教学策略推荐 | 选择 5E/探究式/PBL |
| `courseware_design` | 课件设计 | 跨学科课件生成 |
| `learning_path_planning` | 学习路径规划 | 3 个月 AI 学习计划 |
| `assessment_analysis` | 评估分析 | 学情诊断 + 改进建议 |
| `content_creation` | 内容创作 | 故事脚本 / 教学反思 |

### 3.2 按决策类型分类
| decision_type | 描述 | 端云分工 |
|---------------|------|----------|
| `creative` | 创意型（需要 LLM 创造力）| 云端重 + 端侧轻 |
| `analytical` | 分析型（需要数据洞察）| 云端中 + 端侧重 |
| `educational` | 教育型（需要教学专业性）| 云端中 + 端侧重 |
| `strategic` | 策略型（需要全局视野）| 云端重 + 端侧轻 |

## 4. 7 大核心约束

### 4.1 数据大小约束
- `abstract.abstract_data` 必须 < 10KB
- 超出 → 端侧自动截断 + 警告

### 4.2 隐私约束
- `abstract.pii_detected` 必须为 `false`
- 检测到 PII → 端侧自动脱敏 + 重试

### 4.3 数据保留约束
- 端侧原始数据保留 7 天（合规审计）
- 云端元数据保留 30 天
- 教学决策永久保留（端侧归档）

### 4.4 决策执行约束
- 云端只能返回"决策 / 建议 / 文本"
- 实际操作必须在端侧执行
- `callback.edge_execution` 必须为 `true`

### 4.5 成本监控约束
- 每次请求通过 `request.max_cost_usd` 设置成本上限，响应返回 `usage.cost_usd` 记录实际消耗
- 响应中新增 `cumulative_cost_usd` 字段，端侧维护当月累计计数器（IndexedDB）
- 预算告警三级阈值：50%（黄色警告）→ 80%（红色警告 + 限制非必要请求）→ 100%（自动熔断，切换 Level 5 降级）
- 单次请求建议成本：< $0.01；推荐月预算：< $10/月（约 10,000 次请求）
- 详见 §11 成本监控与预算管控

### 4.6 PII 漏检应急约束
- PII 检测召回率 > 95%，仍有最多 5% 漏检风险；定义 5 层安全网：传输后随机抽样 5% 审计 → 漏检确认 → 自动隔离（暂停云端 5 分钟）→ 通知管理员 → 取证日志
- 响应中新增 `pii_audit` 字段，记录审计触发、PII 类型、处置动作
- 72 小时内按 GDPR 要求完成数据泄露通知
- 详见 §12 PII 漏检应急处理

### 4.7 JSON Schema 校验约束
- 端云协议提供正式 JSON Schema 文件（Draft 2020-12）：`references/edge-cloud-protocol-schema.json`
- 所有请求/响应必须通过 Schema 校验，不合规请求直接拒绝（错误码 `E005`）
- 实现方以 Schema 文件为最终校验依据，本文档示例仅作说明用途
- 详见 §13 形式化 JSON Schema 参考

## 5. 响应结构

```json
{
  "protocol_version": "1.0",
  "request_id": "uuid",
  "timestamp": "2026-08-15T10:00:01Z",
  "status": "success",
  "decision": {
    "type": "creative",
    "content": "推荐使用 5E 教学法（Engage/Explore/Explain/Elaborate/Evaluate）...",
    "structured": {
      "teaching_method": "5E",
      "stages": [...],
      "duration": "45min"
    }
  },
  "usage": {
    "prompt_tokens": 120,
    "completion_tokens": 350,
    "total_tokens": 470,
    "cost_usd": 0.0008
  },
  "audit": {
    "zup_id": "zup-uuid-xxx",
    "abstract_data_size_bytes": 5120,
    "pii_detected": false
  }
}
```

## 6. 错误码

| 错误码 | 描述 | 处理建议 |
|--------|------|----------|
| `E001` | 协议版本不匹配 | 升级端侧到最新版本 |
| `E002` | abstract_data > 10KB | 端侧压缩 |
| `E003` | PII detected | 端侧脱敏重试 |
| `E004` | 数据分类错误 | 改为 `anonymous` |
| `E101` | 云端超时（> 30s） | 重试或降级到本地 |
| `E102` | 云端拒绝（敏感请求） | 改为端侧决策 |
| `E103` | 云端配额超限 | 等待配额刷新 |
| `E201` | 端侧 NPU 不可用 | 降级到 CPU |
| `E202` | 端侧存储已满 | 清理临时数据 |

## 7. 降级策略

### 7.1 5 级降级
```
Level 1: 端云协同（标准）
Level 2: 端云协同（降级，max_tokens 减半）
Level 3: 仅端侧（云端不可用）
Level 4: 仅端侧（最小功能）
Level 5: 完全本地（无 AI 能力）
```

### 7.2 降级触发条件
- 云端连续 3 次超时 → Level 2
- 云端连续 5 次超时 → Level 3
- 端侧 NPU 不可用 → Level 4
- 端侧全部不可用 → Level 5

## 8. 协议示例

### 8.1 教学策略推荐
```json
{
  "protocol_version": "1.0",
  "request_id": "req-uuid-001",
  "timestamp": "2026-08-15T10:00:00Z",
  "source": "edge-ai-pc",
  "intent": "为高一信息技术期中复习推荐教学策略",
  "abstract": {
    "task_type": "pedagogy_recommendation",
    "context": "高一(3)班 · 信息技术 · 期中复习 · 40 人",
    "abstract_data": {
      "avg_score": 78.5,
      "weak_knowledge_points": ["机器学习基础", "神经网络"],
      "class_attention_span": "25min"
    },
    "pii_detected": false,
    "data_classification": "anonymous"
  },
  "request": {
    "decision_type": "educational",
    "max_tokens": 500,
    "max_cost_usd": 0.001
  },
  "callback": {
    "edge_execution": true,
    "save_to_local": true
  }
}
```

### 8.2 跨学科课件生成
```json
{
  "protocol_version": "1.0",
  "request_id": "req-uuid-002",
  "timestamp": "2026-08-15T10:05:00Z",
  "source": "edge-ai-pc",
  "intent": "为《岳阳楼记》生成跨学科课件",
  "abstract": {
    "task_type": "courseware_design",
    "context": "初二语文 · 第 5 课",
    "abstract_data": {
      "text_topic": "岳阳楼记",
      "key_themes": ["忧国忧民", "山水描写", "古文修辞"],
      "duration": "45min",
      "grade": "初二"
    },
    "pii_detected": false,
    "data_classification": "anonymous"
  },
  "request": {
    "decision_type": "creative",
    "max_tokens": 2000,
    "max_cost_usd": 0.008
  },
  "callback": {
    "edge_execution": true,
    "save_to_local": true
  }
}
```

## 9. SDK 示例

### 9.1 Python SDK
```python
from edge_cloud_protocol import EdgeCloudClient

client = EdgeCloudClient(api_key="...", endpoint="...")

# 教学策略推荐
response = client.exchange(
    intent="为高一信息技术期中复习推荐教学策略",
    task_type="pedagogy_recommendation",
    context="高一(3)班 · 信息技术 · 期中复习",
    abstract_data={
        "avg_score": 78.5,
        "weak_knowledge_points": ["机器学习基础"],
    },
    decision_type="educational",
    max_tokens=500,
    max_cost_usd=0.001
)
print(response.decision.content)
```

### 9.2 JavaScript SDK
```javascript
import { EdgeCloudClient } from '@ai-literacy/edge-cloud-protocol';

const client = new EdgeCloudClient({ apiKey: '...', endpoint: '...' });

const response = await client.exchange({
  intent: '为高一信息技术期中复习推荐教学策略',
  taskType: 'pedagogy_recommendation',
  context: '高一(3)班 · 信息技术 · 期中复习',
  abstractData: { avgScore: 78.5, weakKPs: ['机器学习基础'] },
  decisionType: 'educational',
  maxTokens: 500,
  maxCostUsd: 0.001
});
console.log(response.decision.content);
```

## 10. 7 项检查清单

部署 V7 端云协同协议前必查：

- [ ] 协议版本升级到 1.0
- [ ] 实现请求结构 6 段
- [ ] 配置 PII 自动检测
- [ ] 配置 abstract_data < 10KB 限制
- [ ] 实现 5 级降级策略
- [ ] 配置 7 大核心约束
- [ ] 集成 ZUP 零上传证明

## 11. 成本监控与预算管控

### 11.1 单次请求成本追踪
- 每次请求通过 `request.max_cost_usd` 设置成本上限
- 响应中返回 `usage.cost_usd` 记录实际消耗
- 单次请求建议成本：< $0.01

### 11.2 累计成本追踪
- 响应中新增 `cumulative_cost_usd` 字段，记录当月累计消耗
- 端侧维护本地累计计数器（IndexedDB）
- 每次请求前检查累计值是否超出预算

```json
{
  "protocol_version": "1.0",
  "request_id": "uuid",
  "status": "success",
  "usage": {
    "prompt_tokens": 120,
    "completion_tokens": 350,
    "total_tokens": 470,
    "cost_usd": 0.0008
  },
  "cumulative_cost_usd": 3.75
}
```

### 11.3 预算告警阈值
| 阈值 | 触发条件 | 动作 |
|------|----------|------|
| 50% | 累计成本达到月预算 50% | 端侧显示黄色警告，提醒教师控制用量 |
| 80% | 累计成本达到月预算 80% | 端侧显示红色警告，限制非必要请求 |
| 100% | 累计成本达到月预算 100% | 触发自动熔断（见 11.4） |

### 11.4 自动熔断机制
- 当累计成本达到月预算 100% 时，自动切换到 **仅端侧模式**（Level 5 降级）
- 熔断后所有请求仅在端侧处理，不再调用云端 API
- 熔断状态在端侧 UI 显示明确提示
- 管理员可手动解除熔断或调整月预算

### 11.5 成本审计日志
每次请求记录成本审计日志（JSON 格式）：

```json
{
  "cost_audit_id": "cost-audit-uuid-xxx",
  "timestamp": "2026-08-15T10:00:01Z",
  "request_id": "req-uuid-001",
  "cost_usd": 0.0008,
  "cumulative_cost_usd": 3.75,
  "monthly_budget_usd": 10.00,
  "budget_remaining_pct": 62.5,
  "alert_level": "none",
  "circuit_breaker_triggered": false
}
```

### 11.6 月预算建议
- **推荐月预算**：< $10/月（适用于单教师日常教学）
- 按每请求平均 $0.001 计算，$10 预算约支持 10,000 次请求/月
- 学校/机构可按教师数量线性扩展

## 12. PII 漏检应急处理

> **重要前提**：PII 检测召回率 > 95%，意味着仍有最多 5% 的 PII 可能漏检并随 abstract_data 上传到云端。本节定义漏检后的应急处理协议。

### 12.1 漏检响应协议（5 步）

1. **传输后内容审计**：随机抽样 5% 的 `abstract_data` 进行深度 PII 复查
2. **漏检确认**：若审计中发现 PII → 立即撤回云端响应，标记为 ZUP 违规
3. **自动隔离**：暂停云端调用 5 分钟，防止更多数据泄露
4. **通知管理员**：发送告警通知，包含漏检详情
5. **取证日志**：记录泄露的 PII 类型、泄露对象、时间戳

### 12.2 响应 JSON 结构

响应中新增 `pii_audit` 字段：

```json
{
  "protocol_version": "1.0",
  "request_id": "uuid",
  "status": "success",
  "pii_audit": {
    "audit_triggered": true,
    "audit_method": "random_sampling_5pct",
    "pii_found": false,
    "pii_types_found": [],
    "action_taken": "none",
    "circuit_breaker_activated": false,
    "admin_notified": false,
    "forensic_log_id": null
  }
}
```

当检测到 PII 漏检时：

```json
{
  "pii_audit": {
    "audit_triggered": true,
    "audit_method": "random_sampling_5pct",
    "pii_found": true,
    "pii_types_found": ["name", "phone"],
    "action_taken": "revoke_and_quarantine",
    "circuit_breaker_activated": true,
    "quarantine_duration_minutes": 5,
    "admin_notified": true,
    "forensic_log_id": "forensic-uuid-xxx"
  }
}
```

### 12.3 取证日志格式

```json
{
  "forensic_log_id": "forensic-uuid-xxx",
  "timestamp": "2026-08-15T10:05:00Z",
  "request_id": "req-uuid-002",
  "pii_leaked": [
    { "type": "name", "value_masked": "张**", "occurrence": "abstract_data.context" },
    { "type": "phone", "value_masked": "138****5678", "occurrence": "abstract_data.abstract_data" }
  ],
  "leaked_to": "openai-api",
  "cloud_response_revoked": true,
  "quarantine_start": "2026-08-15T10:05:00Z",
  "quarantine_end": "2026-08-15T10:10:00Z",
  "admin_notified_at": "2026-08-15T10:05:01Z"
}
```

## 13. 形式化 JSON Schema 参考

端云协同协议的完整形式化 JSON Schema 定义在独立文件中：

- **文件路径**：`references/edge-cloud-protocol-schema.json`
- **Schema 标准**：JSON Schema Draft 2020-12
- **内容覆盖**：请求结构（6 段）、响应结构（含 `usage` / `audit` / `cumulative_cost_usd` / `pii_audit`）、错误响应结构

> 实现方应以 JSON Schema 文件为最终校验依据，本文档中的示例仅作说明用途。

---

> **核心价值**：Edge-Cloud Protocol v1.0 让所有 AI PC Skill 的端云交互有了统一标准 —— 这是 V7「端云协同」从"概念"到"工程"的关键一步。
