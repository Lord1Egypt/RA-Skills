# 批量建联工作流

## 概述

从达人搜索到邮件发送到跟进的 6 步闭环流程，适用于"找一批达人并发建联邮件"的复合需求。

## 前置条件

- 环境变量已配置（CV_API_KEY、CV_USER_IDENTITY）
- 用户已明确目标达人画像（平台、关键词、国家等筛选条件）

## 步骤

### Step 1: 搜索候选达人 [discovery/creator-search]

- **动作**：根据用户指定的筛选条件搜索达人，建议添加 `has_email: true` 确保结果有邮箱
- **输入**：用户提供的筛选条件（platform、keyword、country_code、followers 范围等）
- **产出**：达人列表（含 username、email、uid、platform、followers_count、engagement_rate）

### Step 2: 筛选确认 [AI 辅助] [需用户确认]

- **动作**：AI 对搜索结果进行初步筛选和排序，展示候选列表供用户确认
- **输入**：Step 1 产出的达人列表
- **产出**：用户确认的最终收件人列表（含 email、uid、nickname、platform）

### Step 3: 发送确认 [outreach/creator-outreach] [需用户确认]

- **动作**：展示完整收件人列表、邮件主题、正文预览，等待用户确认发送
- **输入**：Step 2 确认的收件人列表 + 邮件内容（subject、body_html 或 template_id）
- **产出**：用户确认发送指令

### Step 4: 批量发送 [outreach/creator-outreach]

- **动作**：调用 outreach_send.mjs 执行批量发送
- **输入**：确认后的 recipients 数组 + 邮件内容参数
- **产出**：task_id（发送任务 ID）

### Step 5: 轮询结果 [outreach/creator-outreach]

- **动作**：调用 outreach_task.mjs 轮询发送任务状态直到完成
- **输入**：Step 4 返回的 task_id
- **产出**：发送结果摘要（成功数、失败数、失败原因）

### Step 6: 跟进待办 [outreach/creator-outreach]

- **动作**：发送完成后，提示用户可在 24~48 小时后查看待办跟进
- **输入**：发送完成状态
- **产出**：待办跟进建议（调用 outreach_todo.mjs 查看未回复/超时会话）

## 异常处理

- Step 1 无结果：建议放宽筛选条件或换关键词
- Step 4 发送失败：展示失败原因，询问是否重试
- Step 5 部分失败：展示失败收件人列表，询问是否重发
