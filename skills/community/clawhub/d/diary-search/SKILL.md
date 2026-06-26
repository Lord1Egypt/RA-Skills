---
name: diary-search
description: "检索日记与会话内容，支持中文分词、BM25搜索、时间衰减排序。可搜索日记、查找历史对话（含归档）、导出会话记录（自动过滤噪音，3天后自动清理）、查询定时任务运行记录。"
metadata:
  openclaw:
    emoji: "📔"
    requires:
      bins: []
      config:
        - path: "~/.openclaw/openclaw.json"
          access: "read"
          purpose: "读取插件配置路径"
      filesystem:
        - path: "~/.openclaw/memory"
          access: "read"
          purpose: "读取日记文件"
        - path: "~/.openclaw/memory/exports"
          access: "write"
          purpose: "保存会话导出文件（自动过期清理）"
        - path: "~/.openclaw/agents/*/sessions"
          access: "read-write"
          purpose: "读取会话记录（含归档文件）；清理 checkpoint 备份文件"
        - path: "~/.openclaw/cron"
          access: "read"
          purpose: "读取定时任务运行记录"
    install:
      - id: npm
        kind: node
        package: "diary-search"
        label: "Install via npm"
      - id: clawhub
        kind: clawhub
        slug: diary-search
        label: "Install via ClawHub"
---

# Diary Search

日记与会话检索插件，搜索 OpenClaw 记录的日记内容和历史对话。

**源代码**: [GitHub](https://github.com/sebrinass/diary-search) | **npm**: [diary-search](https://www.npmjs.com/package/diary-search)

## 安装步骤

**第一步：安装插件**

```bash
npm install -g diary-search
```

**第二步：更新配置**

在 `~/.openclaw/openclaw.json` 的 `plugins.load.paths` 中添加：

```json
"~/.npm-global/lib/node_modules/diary-search"
```

完整示例：

```json
{
  "plugins": {
    "enabled": true,
    "load": {
      "paths": [
        "~/.npm-global/lib/node_modules/diary-search"
      ]
    }
  }
}
```

**第三步：重启 Gateway**

```bash
openclaw gateway restart
```

## 使用方法

安装完成后，直接对我说：

### 日记搜索
```
搜索我上周关于"项目架构"的日记
搜索 2026-02 月关于"数据库优化"的讨论
查找昨天提到的"bug"
查看我的日记统计
```

### 会话检索
```
列出昨天的会话
列出 2026-03-03 的会话
搜索我之前说的"webchat"
导出会话 77762d1f 的对话内容
```

### 定时任务查询
```
查看最近 7 天的定时任务运行记录
查看 xiaobu 的定时任务
```

## 工具说明

### 日记工具

#### diary_search

搜索日记内容。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | ✅ | 搜索关键词 |
| limit | number | ❌ | 返回条数，默认 5 |
| time_filter | string | ❌ | 时间过滤器 |

**time_filter 可选值：**
- `today` / `yesterday` / `last_week` / `last_month` / `this_month`
- `YYYY-MM`（如 2026-02）
- `YYYY-MM-DD`（如 2026-02-28）

#### diary_stats

获取日记统计信息。

### 会话工具

#### session_list_by_date

按日期列出会话文件。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | ✅ | 日期（today/yesterday/YYYY-MM-DD/YYYY-MM） |
| agent | string | ❌ | Agent 名称，默认 xiaobu |

**注意**：自动过滤定时任务会话，只显示正常对话。

#### session_search

搜索会话消息内容。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | ✅ | 搜索关键词 |
| date | string | ❌ | 日期过滤，默认最近 30 天 |
| limit | number | ❌ | 返回条数，默认 5 |
| agent | string | ❌ | Agent 名称，默认 xiaobu |

**特性**：
- 默认搜索最近 30 天的会话（包括已归档的会话）
- 如需搜索更早内容，请指定 `date` 参数
- 自动过滤心跳检查消息

#### session_export

导出会话的纯对话文本（自动过滤噪音，只保留时间+正文）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| session_id | string | ✅ | 会话ID（可以是前缀） |
| agent | string | ❌ | Agent 名称，默认 xiaobu |
| include_thinking | boolean | ❌ | 是否包含 AI 思考过程，默认 false |

**特性**：
- 自动过滤心跳检查消息
- 自动剥离记忆注入块（`<relevant-memories>`）、系统元数据、工具输出等噪音
- 导出文件保存至 `{工作区}/memory/exports/` 目录
- 文件名格式：`YYYY-MM-DD-HHmmss-会话导出-标题.md`
- 文件头部含 YAML 元数据（含过期时间，默认 3 天后自动清理）
- 兼容 memory-lancedb-pro 和 OpenClaw 原版记忆插件

### 定时任务工具

#### cron_list_runs

列出定时任务的运行记录。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| days | number | ❌ | 查询最近多少天，默认 7 |
| agent | string | ❌ | 过滤指定 agent 的定时任务 |

**返回内容**：
- 运行时间
- 任务名称
- 状态（ok/error）
- 耗时
- Agent 名称
- 会话 ID（可直接跳转查看详情）
- 执行摘要

## 日记格式

支持 `.md`、`.txt`、`.markdown` 文件，文件名建议使用 `YYYY-MM-DD.md` 格式。

### 清理工具

#### diary_cleanup

扫描并清理会话目录中的 checkpoint 备份文件。checkpoint 是 OpenClaw 在会话出错/中断时自动创建的快照，内容与原会话完全重复，删除不影响正常对话记录。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| agent | string | ❌ | Agent 名称，默认 xiaobu |
| dry_run | boolean | ❌ | 仅扫描不删除（默认 true） |

**使用流程**：

1. 先调用 `diary_cleanup(dry_run=true)` 扫描，查看将删除的文件列表和大小
2. **向用户确认后**，再调用 `diary_cleanup(dry_run=false)` 执行删除
3. ⚠️ **删除前必须向用户确认！**

**自动行为**：会话检索时已自动跳过 checkpoint 文件，无需手动排除。
