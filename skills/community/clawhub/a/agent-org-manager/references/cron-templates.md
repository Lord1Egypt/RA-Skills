# Cron Templates — 可部署配置

Ready-to-deploy cron configurations. Copy, replace placeholders, deploy. Every template here has run in production.

## Template: Daily Learning

Replace: `{Department}`, `{dept_name}`, `{domain}`, `{expr}`

```json
{
  "name": "{Department}·每日学习",
  "schedule": { "kind": "cron", "expr": "{expr}", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "你今天是{Department}。执行每日学习：搜索{domain}的最新进展，关注过去24小时的行业动态。输出学习笔记到 company/departments/{dept_name}/learning/学习笔记_YYYYMMDD.md。格式：(1)核心发现-一条最关键的行业动态 (2)与我司关系-这条发现和我们的业务有什么关联 (3)建议行动-基于这个发现我们应该做什么。控制在300字。使用zai/glm-4-flash。禁止回复HEARTBEAT_OK。禁止使用message工具。输出文件后退出。",
    "model": "zai/glm-4-flash",
    "lightContext": true,
    "timeoutSeconds": 300
  },
  "failureAlert": {
    "after": 2,
    "channel": "feishu",
    "to": "CEO",
    "cooldownMs": 3600000
  }
}
```

### Stagger Table

```
Department      expr         Time
DataCenter      30 7 * * *   07:30
Brand           40 7 * * *   07:40
Sales           50 7 * * *   07:50
Finance         0  8 * * *   08:00
Legal           10 8 * * *   08:10
Inspector       20 8 * * *   08:20
Admin           30 8 * * *   08:30
```

---

## Template: Daily Report

Replace: `{Department}`, `{dept_name}`, `{offset_min}`

```json
{
  "name": "{Department}·每日汇报",
  "schedule": { "kind": "cron", "expr": "{expr}", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "你今天是{Department}。向main session发送每日汇报。汇报包含：(1)今日完成的具体工作 (2)一个你今天学到的东西 (3)一个你担心的风险或问题 (4)需要CEO做的决策（或'无需决策'）(5)明天要交付的东西。用sessions_send发送给main session，不要用message工具。使用zai/glm-4-flash，lightContext。",
    "model": "zai/glm-4-flash",
    "lightContext": true,
    "timeoutSeconds": 300
  },
  "failureAlert": {
    "after": 1,
    "channel": "feishu",
    "to": "CEO",
    "cooldownMs": 7200000
  }
}
```

### Stagger Table

```
Department      expr                Time
DataCenter      0 22 * * *          22:00
Brand           2 22 * * *          22:02
Sales           4 22 * * *          22:04
Finance         6 22 * * *          22:06
Legal           8 22 * * *          22:08
Inspector       10 22 * * *         22:10
Admin           12 22 * * *         22:12
```

---

## Template: Weekly Inspection

```json
{
  "name": "监察部·每周巡检",
  "schedule": { "kind": "cron", "expr": "0 22 * * 5", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行每周cron巡检：(1)cron(action='list')列出所有cron (2)标记consecutiveErrors≥2的job (3)对每个异常job诊断原因 (4)输出巡检报告到company/departments/inspector/巡检报告_YYYYMMDD.md。报告格式：检查总数/正常数/异常数/异常详情。使用zai/glm-4-flash。如果全部正常，输出文件只写'✅ 全数正常'。",
    "model": "zai/glm-4-flash",
    "lightContext": true,
    "timeoutSeconds": 600
  },
  "failureAlert": {
    "after": 2,
    "channel": "feishu",
    "to": "CEO",
    "cooldownMs": 86400000
  }
}
```

---

## Template: Monthly Maintenance

```json
{
  "name": "SkillHub月度维护",
  "schedule": { "kind": "cron", "expr": "0 10 1 * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行月度Skill维护：(1)cd到workspace的skills/目录 (2)检查5个skill（opc-os-core/intelligence-brain/digital-persona/cron-health-monitor/agent-org-manager）的本地SKILL.md是否有更新 (3)如有更新，重新publish到SkillHub (4)同步到GitHub（commit+tag+push+release） (5)输出维护日志到company/departments/datacenter/maintenance/skillhub_YYYYMM.md。使用zai/glm-4-flash。",
    "model": "zai/glm-4-flash",
    "lightContext": true,
    "timeoutSeconds": 1800
  },
  "failureAlert": {
    "after": 1,
    "channel": "feishu",
    "to": "CEO",
    "cooldownMs": 86400000
  }
}
```

---

## Template: One-Shot Repair Task

Replace: `{jobId}`, `{error_description}`, `{department}`

```json
{
  "name": "{Department}·修复 [{jobId}]",
  "schedule": { "kind": "at", "at": "ISO_TIMESTAMP" },
  "sessionTarget": "isolated",
  "deleteAfterRun": true,
  "payload": {
    "kind": "agentTurn",
    "message": "你是{Department}。修复以下cron失败：jobId={jobId}，错误={error_description}。诊断→修复→验证。输出必须以'✅ 已修复'或'❌ 需要CEO'开头。用sessions_send通知main session结果。",
    "model": "zai/glm-4-flash",
    "lightContext": true,
    "timeoutSeconds": 600
  }
}
```

---

## Template Variables Checklist

Before deploying any template, verify:
- [ ] `{Department}` replaced with actual department name (e.g., "品牌部")
- [ ] `{dept_name}` replaced with file-safe name (e.g., "brand")
- [ ] `{domain}` replaced with department's specific learning domain
- [ ] `{expr}` matches the stagger table for that department
- [ ] `failureAlert.channel` and `failureAlert.to` are correct
- [ ] `model` field uses an available provider (verify with current model list)
- [ ] Output paths exist (pre-create directories if needed)
