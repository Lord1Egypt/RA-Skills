---
name: creator-outreach
description: |
  邮件建联全流程能力，覆盖发送、任务查询、沟通历史、待办跟进、效果指标、渠道配置、附件上传。平台代发机制，无需用户提供 SMTP 配置。
  Use when: 建联, 发邮件, 批量发送, email outreach, send email, outreach
compatibility: Node.js 20.6+
metadata:
  layer: outreach
  parent: creator-scraper-cv
---

# Creator Outreach — 邮件建联

## 概述

邮件建联全流程能力：搜索达人后一键发送邮件，支持单发/批量发送、任务轮询、沟通历史查询、待办跟进、效果指标分析，平台统一代发无需用户配置。

## 脚本引用

| 脚本路径 | 状态 | 说明 |
|----------|------|------|
| `../../scripts/outreach_send.mjs` | ✅ 已实现 | 发送邮件（单发/批量） |
| `../../scripts/outreach_task.mjs` | ✅ 已实现 | 查询发送任务状态与结果 |
| `../../scripts/outreach_contact.mjs` | ✅ 已实现 | 查询联系人沟通历史 |
| `../../scripts/outreach_todo.mjs` | ✅ 已实现 | 待办跟进（超时/未读） |
| `../../scripts/outreach_metrics.mjs` | 🔮 待实现 | 效果指标（发送量/打开率/回复率） |
| `../../scripts/outreach_config.mjs` | 🔮 待实现 | 渠道与模板配置查询 |
| `../../scripts/outreach_upload.mjs` | 🔮 待实现 | 附件上传（max 10MB） |

> 🔮 标注的脚本尚未部署，调用将返回错误。待后端实现后可直接启用。

## 架构原则

**Skill = 纯 HTTP 客户端，不做任何本地业务逻辑处理。**

- 脚本只负责组装 JSON 参数并调用 OpenAPI 接口
- 所有业务逻辑（创建提报、查找会话、判断新建/回复）由 OpenAPI 内部完成
- Skill 不需要知道 `submission_id`、`influencer_id` 等内部概念
- 搜索后发送时，将搜索结果中的 `uid` + `platform` 传给 outreach_send，OpenAPI 内部自动从 Holo 查完整达人数据

## 发送机制

**邮件由 Creativault 平台后端统一代发（AWS SES），用户无需提供任何发信配置。**

- **[禁止]** 向用户索要 SMTP 配置、邮箱密码、授权码、发信服务器地址
- **[禁止]** 建议用户"用自己的邮箱手动发送"——平台已具备发送能力
- `channel` 参数当前仅 `ses` 生效（默认值）；`gmail`/`outlook` 为预留字段，后端未实现
- 若用户问"邮件怎么发出去的" → 回答："由 Creativault 平台统一代发，无需配置任何邮箱或 SMTP。"

## 参数说明

### outreach_send.mjs

`to` 和 `recipients` 互斥，传其一。

| 参数 | 类型 | 说明 |
|------|------|------|
| `to` | string | 收件人邮箱（单发） |
| `uid` | string | 达人平台 UID（单发必填，来自搜索结果的 uid 字段） |
| `nickname` | string | 达人昵称（可选，用于会话展示） |
| `platform` | string | 达人平台：tiktok/youtube/instagram |
| `recipients` | object[] | 批量发送：`{email, uid, nickname, platform}` 数组 |
| `subject` | string | 邮件主题 |
| `body_html` | string | HTML 正文（支持 `{{creator_name}}` 变量） |
| `body_text` | string | 纯文本正文 |
| `channel` | string | `ses`（默认，唯一生效渠道） |
| `template_id` | integer | 模板 ID（覆盖 subject/body） |
| `send_mode` | string | `immediate`（默认）/ `smart`（时区优化） |
| `force_new` | boolean | 强制新建会话（默认 false） |
| `attachment_ids` | string[] | 附件 ID 列表 |

### outreach_task.mjs

| 参数 | 类型 | 说明 |
|------|------|------|
| `task_id` | string | **必填**。发送返回的任务 ID |
| `include_result` | boolean | 附带逐收件人结果（默认 false） |
| `result_filter` | string | 结果过滤：`all`/`sent`/`failed` |
| `poll` | boolean | 自动轮询至终态（默认 false） |
| `poll_interval` | integer | 轮询间隔秒数（默认 5） |
| `poll_max_attempts` | integer | 最大轮询次数（默认 60） |

### outreach_contact.mjs

| 参数 | 类型 | 说明 |
|------|------|------|
| `email` | string | **必填**。达人邮箱 |
| `include_history` | boolean | 包含消息历史（默认 true） |
| `include_summary` | boolean | 包含 AI 摘要（默认 true） |

### outreach_todo.mjs

| 参数 | 类型 | 说明 |
|------|------|------|
| `overdue_hours` | integer | 超时阈值小时数（默认 24） |
| `include_unread` | boolean | 包含未读会话（默认 true） |
| `include_overdue` | boolean | 包含超时会话（默认 true） |

## 安全规则

**邮件发送是高风险操作，每次发送前必须获得用户明确确认。**

**[禁止]** 用户说"帮我发邮件"后直接执行发送脚本。

**[必须]** 在执行 `outreach_send.mjs` 之前，展示收件人列表并等待用户确认：

1. **单笔发送**：展示收件人邮箱、主题、正文预览
2. **批量发送**：展示收件人数量（≤5 全部展示，>5 展示前 5 个 + "...及其他 N 个"）、主题、正文预览
3. 用户说"确认"/"发送"/"是"/"Y" → 执行发送
4. 用户说"取消"/"不发"/"修改" → 不执行，询问修改意见
5. 回复已有会话也需要确认
6. 唯一例外：用户明确说"直接发送不用确认"时可跳过

## 输出格式

### 发送确认格式

```
📧 发送确认

• 收件人：{email 或 N 个收件人列表}
• 主题：{subject}
• 渠道：{channel}
• 模式：{send_mode}
• 正文预览：{前 100 字符...}

确认发送吗？(Y/N)
```

### 任务状态格式

```
📬 发送结果

• 任务ID：{task_id}
• 状态：{completed/partial/failed}
• 成功：{sent_count} 封
• 失败：{failed_count} 封
• 耗时：{duration}
• 消耗积分：{credits_consumed}
```

### 积分说明

| 操作 | 积分消耗 |
|------|----------|
| 发送邮件（每封） | 1 |
| 所有查询接口 | 0（免费） |

### 决策规则

- "发邮件"/"建联"/"reach out" → `outreach_send.mjs`
- 搜索结果列表 → `outreach_send.mjs` + `recipients`
- 发送后 → `outreach_task.mjs` + `poll:true` 确认投递
- "待办"/"follow-up" → `outreach_todo.mjs`
- "沟通历史"/"what did I discuss" → `outreach_contact.mjs`
- "效果"/"metrics" → `outreach_metrics.mjs`（🔮 待实现）
- "渠道"/"模板" → `outreach_config.mjs`（🔮 待实现）
- 模板变量：`{{creator_name}}`、`{{creator_email}}`、`{{platform}}`
- 搜索后发送时，**必须**传 `uid` + `platform`（OpenAPI 自动从 Holo 查完整达人数据）
