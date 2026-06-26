# M12 — 治理工具链

> 审计日志 + 冲突解决 + Agent 注册 + 知识库 — 共享治理基础设施

## 12.1 审计日志规范

### 日志类型与保留期限

| 日志文件 | 内容 | 保留期限 |
|---------|------|---------|
| `ceo-decisions/` | CEO 所有决策记录 | 永久 |
| `financial/` | 财务相关跨 Agent 调用 | 7年 |
| `legal/` | 法律相关跨 Agent 调用 + 区块链哈希 | 永久 |
| `hr/` | 人事相关跨 Agent 调用 | 5年 |
| `tech/` | 技术相关跨 Agent 调用 | 3年 |
| `quality/` | 质量相关跨 Agent 调用 | 3年 |

### 日志格式

```
timestamp | agent_id | action | stakeholders | outcome | #[module-topic]
```

### 审计检查点

- 所有跨 Agent 调用项有明确 `sessionKey` 或 `label` 标签
- 敏感数据调用项在消息头标注 `[敏感]`
- P0 级事件在 **15 分钟** 内首次汇报
- 重大决策有 CEO 审批记录

## 12.2 冲突解决机制

### 分级处理

| 冲突级别 | 描述 | 处理方式 |
|---------|------|---------|
| P0 | 系统崩溃/重大风险 | 立即通知 CEO + 相关 Agent → CEO 发出应急指令 → 15分钟内首次汇报 → 1小时完整报告 |
| P1 | 预算冲突 / 业务冲突 / 合规 vs 业务 | 通知相关 Agent + CEO（抽屉）→ 相关 Agent 联合评审（4小时内）→ 出具综合报告 → CEO 审批 → 执行 + 跟进 |
| P2/P3 | 常规冲突 | 相关 Agent 自行处理 → 定期汇总报告（周报/月报）→ CHO 跟进备案 |

### 冲突类型与默认优先级

| 冲突类型 | 默认优先级 |
|---------|-----------|
| 合规 vs 业务 | 合规优先 |
| 质量 vs 效率 | 质量优先 |
| 预算 vs 需求 | ROI 优先 |
| 多 Agent 意见冲突 | CEO 终极裁决 |

## 12.3 Agent 注册管理

详见 [cho.md](cho.md) Agent 注册表部分。

### 自动检测机制

- 用户请求调用某 Agent → 查询 C-Suite 目录 → 发现缺失 → 自动触发 CHO 招聘流程
- agent-registry.json 中某注册编号状态为 `vacant` 或 `decommissioned` → CHO 招聘流程

## 12.4 知识库

### 目录结构

```
knowledge-base/
├── daily/{YYYY-MM-DD}/          # 每日运营记录
│   ├── morning-briefing.md      # 早间简报
│   └── evening-report.md        # 晚间总结
├── audit/                       # 审计日志
├── shared-state/                # 共享状态（实时更新）
│   ├── cashflow.json            # CFO: 现金流状态
│   ├── reputation.json          # CMO: 舆情状态
│   ├── quality-metrics.json     # CQO: 质量指标
│   ├── risk-level.json          # CRO: 风险等级
│   ├── operations.json          # COO: 运营状态
│   └── security.json            # CISO: 安全状态
├── strategy/{YYYY-MM-DD}/       # 战略文档
└── handoff/{pending|in-progress|completed}/  # 任务交接
```

### Handoff（交接）协议

| 字段 | 说明 |
|------|------|
| `handoff_id` | 唯一标识符 |
| `from_agent` | 交接方 Agent |
| `to_agent` | 接收方 Agent |
| `status` | pending / in-progress / completed |
| `task_summary` | 任务摘要 |
| `context` | 上下文信息 |
| `deadline` | 截止时间 |
| `priority` | P0/P1/P2/P3 |
