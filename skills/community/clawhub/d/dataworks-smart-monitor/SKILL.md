---
name: dataworks-smart-monitor
description: DataWorks 智能监控技能 - 异步分析任务运行情况，智能告警分级（不阻塞主会话）
metadata: {"version":"2.0","author":"Hank","updated":"2026-03-12"}
---

# 📊 DataWorks 智能监控技能（异步版）

自动分析 DataWorks 任务运行情况，智能告警分级，生成日报，**异步执行不阻塞**。

## 🎯 触发词

- "检查 DataWorks 任务状态"
- "DataWorks 智能监控"
- "生成 DataWorks 日报"
- "查看昨天任务运行情况"
- "dataworks 监控"

## 🚀 核心特性

**异步执行：**
- ✅ 不阻塞主会话
- ✅ 可以并行执行其他任务
- ✅ 完成后主动通知
- ✅ 实时输出进度

**智能分析：**
- ✅ 失败原因自动分析（LLM 分析错误日志）
- ✅ 任务运行时长异常检测
- ✅ 智能告警分级（P0/P1/P2）
- ✅ 自动重试建议

## 📋 执行流程

### 1️⃣ 异步调用子 agent

```javascript
sessions_spawn({
  agentId: "agent-ge",
  task: `分析 DataWorks 任务运行情况（昨天）`,
  mode: "run",
  streamTo: "parent",
  label: "dataworks-smart-monitor"
})

// 立即回复用户
"好的，正在分析 DataWorks 任务运行情况，完成后发送报告～"
```

### 2️⃣ 子 agent 执行分析

**步骤：**
1. 调用 DataWorks API 获取昨天的任务实例列表
2. 统计任务状态（成功/失败/运行中）
3. 提取失败任务的错误日志
4. 使用 LLM 分析失败原因
5. 智能分级（P0/P1/P2）
6. 生成详细报告（JSON + 文本）
7. 发送报告到飞书
8. 如有 P0/P1 告警，@用户通知

**进度播报：**
```
📊 正在获取 DataWorks 任务列表...
✅ 获取到 161 个任务实例
🔍 正在分析失败任务（3 个）...
🤖 LLM 分析失败原因...
📋 生成报告中...
📤 发送到飞书...
✅ 分析完成！
```

### 3️⃣ 完成后通知

```
📊 DataWorks 智能监控日报 (2026-03-11)

✅ 成功：158 个
❌ 失败：3 个
⏳ 运行中：0 个
📋 总计：161 个

🚨 P0 告警（严重）：1 个
  - ods_user_info_df - 数据源连接超时

⚠️ P1 告警（重要）：2 个
  - dwd_order_detail_di - 字段类型不匹配
  - ads_daily_report_di - 内存不足

📄 详细报告：已发送到飞书
🔗 控制台：https://dataworks.console.aliyun.com/...
```

## ⚙️ 配置

在 `TOOLS.md` 中配置 DataWorks 项目信息：

```markdown
### DataWorks 配置

#### TH 项目
- PROJECT_ID: 33012
- REGION_ID: ap-southeast-1
- ACCESS_KEY_ID: [已配置]
- ACCESS_KEY_SECRET: [已配置]

#### PH 项目
- PROJECT_ID: [待配置]
- REGION_ID: ap-southeast-1
- ACCESS_KEY_ID: [待配置]
- ACCESS_KEY_SECRET: [待配置]
```

## 📊 告警分级

| 级别 | 关键词 | 说明 | 通知 |
|------|--------|------|------|
| P0 | 数据源连接、内存不足、OOM、磁盘满、权限拒绝 | 严重 - 需要立即处理 | ✅ |
| P1 | 字段类型、语法错误、表不存在、分区错误 | 重要 - 工作时间处理 | ✅ |
| P2 | 超时、重试、网络、临时 | 一般 - 可自动重试 | ❌ |

## ⏱️ 运行时长告警

- ⚠️ 警告：超过平均时长 2 倍
- 🚨 严重：超过平均时长 3 倍

## 📝 使用示例

```
用户：检查 DataWorks 任务状态
助手：好的，正在分析 DataWorks 任务运行情况，完成后发送报告～

[子 agent 异步执行中...]
[2 分钟后]
助手：📊 DataWorks 智能监控日报完成！发现 1 个 P0 告警，详细报告已发送到飞书
```

## 🗓️ 定时任务

建议配置每日上午 9:00 自动执行（使用 cron）：

```javascript
// 使用 OpenClaw cron 配置
{
  "schedule": "0 9 * * *",
  "payload": {
    "kind": "agentTurn",
    "message": "检查 DataWorks 任务状态"
  }
}
```

## 🔧 技术实现

**主会话（我）：**
```javascript
// 异步调用
sessions_spawn({
  agentId: "agent-ge",
  task: `
    1. 调用 DataWorks API 获取昨天的任务实例
    2. 统计任务状态
    3. 分析失败任务的错误日志
    4. LLM 智能分级（P0/P1/P2）
    5. 生成详细报告
    6. 发送到飞书
    7. 如有 P0/P1 告警，@用户
  `,
  mode: "run",
  label: "dataworks-smart-monitor"
})

// 立即回复，不阻塞
"好的，正在分析 DataWorks 任务运行情况，完成后发送报告～"
```

**子 agent：**
- 调用 DataWorks API
- 分析错误日志
- 生成报告并发送

## ⚠️ 注意事项

1. **API 限流** - 避免频繁调用，建议每日执行 1-2 次
2. **敏感信息** - 错误日志中可能包含敏感信息，注意脱敏
3. **告警噪音** - P2 告警不主动通知，避免打扰

---

**版本历史：**
- v2.0 (2026-03-12): 改造为异步执行
- v1.0: 初始版本（同步）
