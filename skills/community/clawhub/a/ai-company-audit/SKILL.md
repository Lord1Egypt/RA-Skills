---
name: "AI Company Audit"
slug: "ai-company-audit"
version: "1.0.0"
homepage: "https://clawhub.com/skills/ai-company-audit"
description: "跨Agentaudit日志standard。7类日志（决策/操作/错误/security/性能/访问/data）+ compliance检查点 + audittrackstandard，适配fully AI companygovernframework。"
license: MIT-0
tags: [ai-company, audit, compliance, logging, governance, audit-trail]
triggers:
  - audit log
  - compliance
  - audit trail
  - logging standard
  - audit日志
  - compliance检查
  - audittrack
  - 日志standard
interface:
  inputs:
    type: object
    schema:
      type: object
      properties:
        log_type:
          type: string
          enum: [decision, action, error, security, performance, access, data]
          description: audit日志类型
        agent_id:
          type: string
          description: Agent编号（可选）
        date_range:
          type: object
          properties:
            from: string
            to: string
  outputs:
    type: object
    schema:
      type: object
      properties:
        logs:
          type: array
          description: 日志条目数组
        compliance_status:
          type: object
          description: compliance状态
        anomalies:
          type: array
          description: 异常列表
  errors:
    - code: AUDIT_001
      message: "Log entry missing required fields"
      action: "Enforce schema: timestamp/agent/action/result"
permissions:
  files: []
  network: []
  commands: []
  mcp: []
dependencies:
  skills: [ai-company-hq, ai-company-registry, ai-company-conflict]
  cli: []
quality:
  saST: Pass
  vetter: Approved
  idempotent: true
metadata:
  category: governance
  layer: AGENT
  cluster: ai-company
  maturity: STABLE
  license: MIT-0
  standardized: true
---

# Audit Logging Standard — audit日志standard

## 7类audit日志

| Log Type | Description | Retention |
|----------|-------------|----------|
| Decision | strategy/战术决策record | 2 years |
| Action | Agent execute的操作 | 90 days |
| Error | 系统异常和错误 | 90 days |
| Security | authenticate/authorize/security incident | 2 years |
| Performance | latency/吞吐量/KPI | 30 days |
| Access | data访问record | 2 years |
| Data | data变更历史 | 7 years |

## Log Entry Schema

```yaml
log_entry:
  timestamp: "ISO 8601 format (YYYY-MM-DDTHH:MM:SS.SSSZ)"
  agent_id: "e.g., CFO-001, CEO-001"
  log_type: "decision|action|error|security|performance|access|data"
  action: "string (what happened)"
  target: "string (affected resource/endpoint)"
  result: "success|failure|partial"
  duration_ms: 0
  metadata:
    task_id: "TASK-001"
    confidence: 0.95
    [敏感]: "redacted"
  trace_id: "uuid (for cross-agent correlation)"
```

## Compliance Checkpoints

| Checkpoint | Standard | Enforcement |
|-----------|---------|-------------|
| P0 SLA 达成 | 95% P0 event在 SLA 内完成 | CQO monitor |
| 敏感data标注 | 所有 PII 字段含 `[敏感]` 标注 | CISO audit |
| 跨 Agent audittrack | trace_id 贯穿完整调用链 | CTO 技术实现 |
| audit日志不可篡改 | append-only + hash chain | CTO 技术实现 |
| audit日志保留期 | 详见上表（7类）| CTO storestrategy |

## P0 Incident Compliance

| P0 standard | respond要求 | audit要求 |
|---------|---------|---------|
| respond时间 | 15 分钟内初始respond | 时间戳record |
| CEO 通报 | 立即通报 | 决策日志 |
| 根因analyze | 48 小时内完成 | analyzereport存档 |
| improve项 | 7 天内入 backlog | trackrecord |

## Audit Log Storage Policy

```yaml
storage_policy:
  format: "structured JSON (CloudWatch/Elasticsearch/Splunk compatible)"
  encryption: "AES-256-GCM at rest"
  replication: "3 copies across regions"
  access_control: "CQO + CISO read-only; CTO write-only"
  retention:
    decision: "2 years"
    security: "2 years"
    access: "2 years"
    performance: "30 days"
    action: "90 days"
    error: "90 days"
    data: "7 years"
```

## Natural Language Commands

```
"Audit all decisions this week" → Decision logs filtered by date range
"Check compliance for P0 SLAs" → P0 compliance report
"Review access logs for sensitive data" → Access log audit
"Export audit trail for INC-001" → Trace by trace_id
```
