# 高级功能配置指南

本文档详细说明 ChatMerge 的所有高级功能配置方法。

---

## 📋 目录

1. [智能频道发现](#智能频道发现)
2. [定时纪要](#定时纪要)
3. [实时监控](#实时监控)
4. [行动项跟踪](#行动项跟踪)
5. [多维度分析](#多维度分析)
6. [智能摘要分级](#智能摘要分级)
7. [语音/视频会议集成](#语音视频会议集成)
8. [跨平台去重](#跨平台去重)
9. [AI 智能建议](#ai-智能建议)

---

## 智能频道发现

### 功能说明

当用户没有指定具体频道时，自动列出可用频道并智能推荐。

### 使用方式

```
使用 $chatmerge，总结我昨天的讨论
```

ChatMerge 会自动：
1. 列出昨天有活动的所有频道
2. 按消息数量排序
3. 让用户选择要总结的频道

### 配置选项

```yaml
channel_discovery:
  enabled: true
  sort_by: "activity"  # activity, name, platform
  show_message_count: true
  show_last_activity: true
  max_channels: 10  # 最多显示多少个频道
```

### 高级用法

**按关键词过滤：**
```
使用 $chatmerge，总结我在"项目"相关频道的讨论
```

**按平台过滤：**
```
使用 $chatmerge，总结我在 Discord 的所有讨论
```

---

## 定时纪要

### 功能说明

设置定时任务，自动生成纪要并推送到指定目标。

### 基础配置

```yaml
schedule:
  - name: "每日站会纪要"
    cron: "0 9 * * 1-5"  # 工作日早上 9 点
    channels:
      - "discord:#project-alpha"
      - "slack:#team-chat"
    time_range: "last_24h"
    summary_level: "brief"
    output_to: "slack:#standup-notes"
```

### Cron 表达式说明

```
格式：分 时 日 月 周
示例：
- "0 9 * * 1-5"  # 工作日早上 9 点
- "0 18 * * 5"   # 每周五下午 6 点
- "0 */2 * * *"  # 每 2 小时
- "0 9,18 * * *" # 每天早上 9 点和下午 6 点
```

### 完整配置示例

```yaml
schedule:
  # 每日站会纪要
  - name: "每日站会纪要"
    cron: "0 9 * * 1-5"
    channels:
      - "discord:#project-alpha"
      - "slack:#team-chat"
    time_range: "last_24h"
    summary_level: "brief"
    output_to: "slack:#standup-notes"
    notify_on_error: true

  # 每周周报
  - name: "周报"
    cron: "0 18 * * 5"
    channels:
      - "discord:#project-alpha"
      - "telegram:产品讨论群"
    time_range: "last_7d"
    summary_level: "comprehensive"
    perspective: "exec"  # CEO 视角
    output_to: "email:boss@company.com"
    include_analysis: true

  # 客户反馈日报
  - name: "客户反馈日报"
    cron: "0 20 * * *"
    channels:
      - "slack:#customer-support"
    time_range: "last_24h"
    summary_level: "detailed"
    focus: "customer_feedback"
    output_to: "notion:page_id_xxx"
```

### 使用命令设置

```
使用 $chatmerge，设置每天早上 9 点自动生成站会纪要，包含 Discord #project-alpha 和 Slack #team-chat，发送到 Slack #standup-notes
```

### 管理定时任务

**查看所有定时任务：**
```
使用 $chatmerge，显示所有定时纪要
```

**暂停定时任务：**
```
使用 $chatmerge，暂停"每日站会纪要"
```

**删除定时任务：**
```
使用 $chatmerge，删除"每日站会纪要"
```

---

## 实时监控

### 功能说明

持续监听指定频道，当出现关键事件时立即通知。

### 基础用法

```
使用 $chatmerge，监控 Discord #project-alpha，有紧急情况通知我
```

### 完整配置

```yaml
monitoring:
  - name: "项目频道监控"
    channels:
      - "discord:#project-alpha"
      - "slack:#team-chat"
    triggers:
      keywords:
        - "P0"
        - "critical"
        - "urgent"
        - "紧急"
        - "线上故障"
      mentions:
        - "@boss"
        - "@all"
      decisions: true  # 监控决策
      risks: true      # 监控风险信号
    notify_to: "telegram:me"
    summary_interval: "1h"  # 每小时生成一次摘要
```

### 触发条件

**紧急关键词：**
- P0, P1, critical, urgent, 紧急, 线上故障

**重要决策：**
- 决定, 批准, 确定, approved, confirmed

**风险信号：**
- 延期, 阻塞, 无法完成, blocked, delayed

**特殊提及：**
- @老板, @all, @here

### 通知示例

```
⚠️ 紧急提醒
时间：2026-03-23 14:35
频道：Discord #project-alpha
发言人：李四

内容：
"发现 P0 级 bug，iOS 支付崩溃，影响所有用户"

建议：立即处理！

[查看完整讨论] [停止监控]
```

### 管理监控任务

**查看所有监控：**
```
使用 $chatmerge，显示所有监控任务
```

**停止监控：**
```
使用 $chatmerge，停止监控 Discord #project-alpha
```

---

## 行动项跟踪

### 功能说明

自动创建任务到外部工具（Jira/Notion/GitHub），并持续跟踪进度。

### 支持的集成

1. **Jira**
2. **Notion**
3. **GitHub Issues**
4. **日历（Google Calendar, Outlook）**
5. **Todoist**
6. **Trello**

### 配置集成

```yaml
integrations:
  jira:
    enabled: true
    url: "https://your-company.atlassian.net"
    project_key: "PROJ"
    default_issue_type: "Task"
    credentials: "env:JIRA_API_TOKEN"

  notion:
    enabled: true
    database_id: "xxx-xxx-xxx"
    credentials: "env:NOTION_API_KEY"

  github:
    enabled: true
    repo: "your-org/your-repo"
    credentials: "env:GITHUB_TOKEN"

  calendar:
    enabled: true
    provider: "google"  # google, outlook
    credentials: "env:GOOGLE_CALENDAR_TOKEN"
```

### 使用方式

**自动创建任务：**
```
使用 $chatmerge，总结 Discord #project-alpha 最近 100 条消息，并创建行动项到 Jira
```

**手动确认：**
```
"我发现 3 个行动项，要帮你创建任务吗？

1. 修复 iOS 支付 bug (李四, 今天 18:00)
   → 创建 Jira ticket
   → 添加日历提醒

2. 准备 v2.3 上线方案 (张三, 周四 17:00)
   → 创建 Notion 任务
   → 添加日历提醒

要创建吗？（可以说'全部'、'1,2'或'取消'）"
```

### 进度跟踪

**自动跟踪：**
- ChatMerge 会定期检查行动项状态
- 从后续聊天中识别任务完成
- 自动更新任务状态

**进度报告：**
```
"行动项进度更新（2026-03-23）：

✅ 已完成（2 个）
- 修复 iOS 支付 bug (李四)
- 优化数据库索引 (王五)

⏳ 进行中（1 个）
- 准备 v2.3 上线方案 (张三, 预计周四完成)

❌ 已延期（1 个）
- 排查客户 A 性能问题 (老张, 原定今天，已延期 1 天)

要我在群里提醒老张吗？"
```

### 配置选项

```yaml
action_tracking:
  enabled: true
  auto_create: false  # 是否自动创建，false 则需要用户确认
  auto_update: true   # 是否自动更新状态
  check_interval: "6h"  # 检查间隔
  remind_before_due: "2h"  # 截止前多久提醒
  notify_on_overdue: true  # 延期时是否通知
```

---

## 多维度分析

### 功能说明

从人员、情绪、效率等多个维度分析聊天内容。

### 启用方式

```
使用 $chatmerge，总结 Discord #project-alpha 最近 100 条消息，包含多维度分析
```

### 分析维度

#### 1. 人员分析

```markdown
## 人员分析

### 发言统计
- 发言最多：张三 (45 条, 占 28%)
- 发言最少：王五 (3 条, 占 2%)
- 平均发言：16 条/人

### 活跃时段
- 最活跃：下午 2-4 点 (67 条消息)
- 最安静：上午 10-12 点 (12 条消息)

### 沉默成员
- ⚠️ 王五：3 天未发言
- ⚠️ 赵六：5 天未发言

建议：私下沟通了解情况
```

#### 2. 情绪分析

```markdown
## 情绪分析

### 整体情绪
- 正面：35% 😊
- 中性：45% 😐
- 负面：20% 😟

### 焦虑话题
- iOS bug 修复 (负面情绪 80%)
- 进度延期 (负面情绪 65%)

### 积极话题
- v2.3 上线成功 (正面情绪 90%)
- 用户好评 (正面情绪 85%)

建议：关注 iOS bug 修复进展，及时沟通缓解焦虑
```

#### 3. 效率分析

```markdown
## 效率分析

### 决策效率
- 平均决策时间：2.5 小时
- 最快决策：iOS bug 修复方案 (30 分钟)
- 最慢决策：v3.0 技术选型 (6 小时)

### 行动项完成率
- 本周完成：3/5 (60%)
- 按时完成：2/3 (67%)
- 延期任务：2 个

### 待跟进问题
- 总数：5 个
- 超过 3 天未解决：2 个

建议：提升决策效率，减少讨论时间
```

### 配置选项

```yaml
analysis:
  enabled: true
  dimensions:
    people: true
    sentiment: true
    efficiency: true
    risks: true
  sentiment_threshold: 0.6  # 情绪判断阈值
  silence_threshold_days: 3  # 多少天未发言算沉默
```

---

## 智能摘要分级

### 功能说明

根据用户角色生成不同粒度的摘要。

### 使用方式

**指定视角：**
```
使用 $chatmerge，总结 Discord #project-alpha 最近 100 条消息，CEO 视角
```

**自动识别：**
ChatMerge 会根据用户身份自动选择合适的视角。

### 三种视角

#### 1. CEO 视角（极简）

**特点：**
- 只包含关键结论
- 突出数字和结果
- 3-5 条核心信息

**示例：**
```markdown
# 本周关键信息

✅ v2.3 已上线，用户反馈积极
⚠️ iOS bug 已修复，影响 2 小时
💰 Q2 预算 50 万已批准
📈 下周重点：v3.0 需求评审
```

#### 2. 项目经理视角（详细）

**特点：**
- 包含进展、风险、资源需求
- 完整的行动项列表
- 详细的风险分析

**示例：**
```markdown
# 本周项目进展

## 产品发布
- v2.3 上线：周五 18:00 顺利上线，无回滚
- 用户反馈：整体积极，搜索性能提升明显

## Bug 修复
- 3 个 P0 bug 已全部修复

## 进度风险
- v3.0 排期较紧，需加人

## 下周计划
- 需求评审、技术方案确定
```

#### 3. 开发者视角（技术细节）

**特点：**
- 包含技术实现细节
- 具体的 bug 和修复方案
- 技术决策和架构讨论

**示例：**
```markdown
# 本周技术工作

## Bug 修复
- iOS 支付崩溃 (根因：nil pointer in payment handler)
- 修复方案：添加 null check + 单元测试

## 性能优化
- 优化数据库索引 (性能提升 40%)
- 搜索算法优化 (响应时间 800ms → 300ms)

## 技术债务
- 升级依赖库 (修复 CVE-2024-1234)
- 重构支付模块 (减少代码重复 30%)
```

### 配置选项

```yaml
summary_levels:
  exec:  # CEO 视角
    max_items: 5
    include_details: false
    focus: ["results", "risks", "decisions"]

  pm:  # 项目经理视角
    max_items: 20
    include_details: true
    focus: ["progress", "risks", "resources", "actions"]

  dev:  # 开发者视角
    max_items: 50
    include_details: true
    focus: ["technical", "bugs", "architecture", "code_review"]
```

---

## 语音/视频会议集成

### 功能说明

自动转录语音/视频会议内容，生成会议纪要。

### 支持平台

- Zoom
- Google Meet
- Microsoft Teams
- 腾讯会议
- 飞书会议

### 使用方式

**自动检测：**
```
"检测到你刚结束了一个 Zoom 会议（1 小时 23 分钟）
要我生成会议纪要吗？"
```

**手动触发：**
```
使用 $chatmerge，总结我刚才的 Zoom 会议
```

### 配置集成

```yaml
meeting_integration:
  zoom:
    enabled: true
    auto_record: true
    auto_transcribe: true
    credentials: "env:ZOOM_API_KEY"

  google_meet:
    enabled: true
    auto_record: true
    auto_transcribe: true
    credentials: "env:GOOGLE_MEET_TOKEN"
```

### 会议纪要示例

```markdown
# 会议纪要：v3.0 需求评审

## 会议信息
- 时间：2026-03-23 14:00-15:23 (1 小时 23 分钟)
- 平台：Zoom
- 参与者：5 人（张三、李四、王五、赵六、孙七）
- 主持人：张三

## 发言统计
- 张三：23 分钟 (28%)
- 李四：18 分钟 (22%)
- 王五：15 分钟 (18%)
- 赵六：12 分钟 (15%)
- 孙七：8 分钟 (10%)
- 沉默时间：7 分钟 (8%)

## 主要议题
1. v3.0 核心功能确定
2. 技术架构选型
3. 排期和资源分配

## 关键讨论

### v3.0 核心功能
- 决定：优先实现用户画像和智能推荐
- 理由：市场需求最强烈，ROI 最高
- 反对意见：王五认为应该先做性能优化
- 最终结论：先做核心功能，性能优化并行进行

### 技术架构
- 方案 A：微服务架构（张三推荐）
- 方案 B：单体架构（李四推荐）
- 决定：采用方案 A，但分阶段实施
- 理由：长期可扩展性更好

## 决策记录
1. v3.0 优先实现用户画像和智能推荐
2. 采用微服务架构，分阶段实施
3. 招聘 2 名后端工程师
4. 下周一前完成详细技术方案

## 行动项
| 任务 | 负责人 | 截止时间 | 状态 |
| --- | --- | --- | --- |
| 完成详细技术方案 | 张三 | 下周一 | 待开始 |
| 启动招聘流程 | HR | 本周五 | 待开始 |
| 评估性能优化工作量 | 王五 | 下周三 | 待开始 |

## 待跟进问题
1. 微服务架构的具体拆分方案？
2. 性能优化和新功能如何并行？
3. 招聘预算是否充足？

## 下次会议
- 时间：下周一 14:00
- 议题：技术方案评审
```

---

## 跨平台去重

### 功能说明

识别跨平台的同一讨论，避免重复统计。

### 工作原理

1. **内容相似度匹配**
   - 使用语义相似度算法
   - 阈值：85% 以上认为是同一讨论

2. **时间邻近度**
   - 时间差在 5 分钟内
   - 考虑跨平台转发延迟

3. **关键词匹配**
   - 提取关键实体（人名、项目名、Bug ID）
   - 关键词一致则认为相关

### 示例

**原始消息：**
```
Discord #project-alpha (10:23)
张三："发现 iOS 支付 bug，需要紧急修复"

Slack #team-chat (10:25)
李四："Discord 上说 iOS 支付有 bug，谁负责修？"

Telegram 产品群 (10:30)
王五："刚看到 iOS 支付的问题，影响大吗？"
```

**去重后：**
```markdown
## 跨平台讨论追踪

### iOS 支付 bug
- 首次提及：Discord #project-alpha (张三, 10:23)
- 后续讨论：
  - Slack #team-chat (李四, 10:25)
  - Telegram 产品群 (王五, 10:30)
- 参与人数：5 人
- 讨论热度：🔥🔥🔥 高
- 跨平台数：3 个

**关键内容：**
"发现 iOS 支付 bug，需要紧急修复"
```

### 配置选项

```yaml
deduplication:
  enabled: true
  similarity_threshold: 0.85  # 相似度阈值
  time_window: 300  # 时间窗口（秒）
  track_cross_platform: true  # 是否追踪跨平台讨论
```

---

## AI 智能建议

### 功能说明

基于分析结果，主动提供改进建议。

### 建议类型

#### 1. 效率建议

**触发条件：**
- 讨论时间过长（> 2 小时）
- 决策效率低
- 重复讨论同一问题

**示例：**
```markdown
## 📊 效率建议

### 问题：讨论时间过长
- 发现 3 个讨论超过 2 小时才有结论
- 平均决策时间：2.5 小时（行业平均：1 小时）

### 建议：
1. 提前准备议题和方案
2. 设置讨论时间上限（如 1 小时）
3. 指定决策人避免拖延
4. 使用投票快速达成共识

### 预期效果：
- 决策时间缩短 50%
- 团队效率提升 30%
```

#### 2. 风险建议

**触发条件：**
- 成员长时间沉默
- 多次提到延期/阻塞
- 负面情绪高

**示例：**
```markdown
## ⚠️ 风险建议

### 问题：成员沉默
- 王五已经 3 天未发言
- 赵六已经 5 天未发言

### 可能原因：
1. 工作遇到阻塞
2. 对项目失去兴趣
3. 个人原因

### 建议：
1. 私下沟通了解情况
2. 提供必要的帮助和支持
3. 调整任务分配

### 预期效果：
- 及时发现和解决问题
- 提升团队凝聚力
```

#### 3. 流程建议

**触发条件：**
- 行动项缺少负责人
- 截止时间不明确
- 决策流程混乱

**示例：**
```markdown
## 🎯 流程建议

### 问题：行动项不明确
- 发现 5 个行动项没有明确负责人
- 3 个行动项没有截止时间

### 建议：
1. 每次讨论结束前明确 owner
2. 使用 @mention 指定负责人
3. 设置明确的截止时间
4. 使用任务管理工具（Jira/Notion）

### 实施方案：
- 在群里发送行动项模板
- 要求每个行动项必须有 owner 和 deadline
- 定期检查行动项进度

### 预期效果：
- 行动项完成率提升 40%
- 延期率降低 50%
```

### 配置选项

```yaml
ai_suggestions:
  enabled: true
  types:
    efficiency: true
    risks: true
    process: true
  threshold:
    discussion_time: 7200  # 讨论超过 2 小时触发建议
    silence_days: 3  # 沉默超过 3 天触发建议
    missing_owner_count: 3  # 缺少负责人的行动项超过 3 个触发建议
```

---

## 总结

ChatMerge 的高级功能让聊天纪要从"被动记录"升级为"主动管理"：

1. **智能发现** - 自动找到需要总结的频道
2. **自动执行** - 定时生成纪要，无需手动触发
3. **实时监控** - 关键事件立即通知
4. **闭环管理** - 从讨论到任务到跟踪，全流程自动化
5. **深度洞察** - 多维度分析，发现隐藏问题
6. **智能建议** - AI 主动提供改进方案

这些功能让 ChatMerge 不仅是一个纪要工具，更是一个**团队协作智能助手**。

---

**需要帮助？** 查看 [README.md](README.md) | [QUICKSTART.md](QUICKSTART.md) | [SKILL.md](SKILL.md)
