---
name: daily-standup
description: 每日早报聚合器。当用户询问每日汇总、standup、晨报、或工作状态总览时激活。
metadata:
  openclaw:
    emoji: "📋"
    requires:
      env: [MORPHIXAI_API_KEY]
---

# 每日早报

聚合多个数据源，生成精简的晨报。

## 前置条件

1. **安装插件**: `openclaw plugins install openclaw-morphixai`
2. **获取 API Key**: 访问 [morphix.app/api-keys](https://morphix.app/api-keys) 生成 `mk_xxxxxx` 密钥
3. **配置环境变量**: `export MORPHIXAI_API_KEY="mk_your_key_here"`
4. **链接账号**: 访问 [morphix.app/connections](https://morphix.app/connections) 链接需要聚合的服务账号（GitLab、Jira、Outlook 等），或通过 `mx_link` 工具逐个链接

## 触发词

- "早报" / "日报" / "standup" / "今日工作"
- "帮我看看今天有什么"

## 执行策略

使用 `mx_*` 工具**并行**查询以下数据源，然后汇总输出。

### GitLab

使用 `mx_gitlab` 工具：

```
1. mx_gitlab: action: get_user → 获取当前用户
2. mx_gitlab: action: list_projects → 获取项目列表
3. mx_gitlab: action: list_merge_requests, state: "opened"
     → 查询我的待合并 MR
4. mx_gitlab: action: list_pipelines, per_page: 5
     → 查看最近 pipeline 状态
```

### GitHub（可选）

使用 `mx_github` 工具：

```
1. mx_github: action: list_pulls, state: "open" → 我的待合并 PR
2. mx_github: action: list_issues, state: "open" → 待处理 Issue
3. mx_github: action: list_workflow_runs → CI 状态
```

### Jira

使用 `mx_jira` 工具：

```
1. mx_jira: action: get_myself → 获取当前用户 accountId
2. mx_jira: action: search_issues
   jql: "assignee = <accountId> AND status != Done ORDER BY priority DESC, updated DESC"
     → 我的未完成 Issue
3. mx_jira: action: search_issues
   jql: "assignee = <accountId> AND due >= startOfWeek() AND due <= endOfWeek() ORDER BY due ASC"
     → 本周到期 Issue
4. mx_jira: action: search_issues
   jql: "sprint in openSprints() AND assignee = <accountId>"
     → 当前 Sprint 进度
```

### 邮件（可选）

使用 `mx_outlook` 或 `mx_gmail` 工具：

**Outlook：**
```
mx_outlook: action: list_messages, top: 10
  → 筛选 isRead: false 的邮件
```

**Gmail：**
```
mx_gmail: action: search_messages, query: "is:unread", max_results: 10
  → 然后逐条 get_message 获取摘要
```

### 待办任务（可选）

使用 `mx_ms_todo` 或 `mx_google_tasks` 工具：

```
mx_ms_todo: action: list_tasks, list_id: "<默认列表ID>"
  → 筛选今日到期的任务
```

### 日历（可选）

使用 `mx_outlook_calendar` 工具：

```
mx_outlook_calendar: action: get_calendar_view
  start_date_time: "<今日 00:00>"
  end_date_time: "<今日 23:59>"
  → 今日会议安排
```

## 降级规则

如果某个工具的账号未链接或查询失败，跳过该部分并标注"未连接"或"查询失败"——绝不阻塞整个早报。

使用 `mx_link: action: list_accounts` 预先检测哪些账号可用，只查询已连接的服务。

## 回复格式

严格按以下结构回复（中文，精简）：

```
**代码**
- GitLab: N 个待合并 MR（列出标题）/ GitHub: N 个待合并 PR
- CI 状态：全绿 / X 个失败

**Jira**
- N 个本周到期 Issue（列出 key + 标题）
- 当前 Sprint 进度：X/Y 完成

**邮件**
- N 封未读（列出发件人 + 主题，最多 5 封）

**待办**
- N 个今日到期任务（列出标题）

**日历**
- N 个今日会议（列出时间 + 主题）

**今日建议**
- 基于以上信息给出 1-2 条优先级建议
```

> 未连接的数据源不展示对应板块。

## 规则

- 总输出不超过 500 字
- 无客套话，无寒暄
- 紧急事项优先标记
- 仅用列表，不用段落
