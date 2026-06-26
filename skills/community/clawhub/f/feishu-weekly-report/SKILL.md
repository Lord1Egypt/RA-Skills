---
name: feishu-weekly-report
description: |
  生成飞书周报。通过两种方式收集工作内容：(1) 调用飞书API拉取指定时间范围的聊天记录，(2) 读取本地daily memory日志。
  合并两个数据源后，按用户指定的周报模板自动整理输出。
  触发词：周报、工作总结、上周总结、本周总结、写周报、weekly report。
  Use when: 用户需要生成周报、工作总结，或要求回顾某段时间的工作内容。
---

# 飞书周报 Skill

生成周报分两步：收集素材 → 整理输出。

## Step 1: 收集素材

从两个数据源并行收集，合并去重。

### 数据源 A: 飞书聊天记录（API 拉取）

1. 确定时间范围（默认上周一 00:00 到上周日 23:59，用户本地时区）
2. 从 OpenClaw 配置获取飞书 app_id 和 app_secret：
   ```bash
   grep -E "appId|appSecret" ~/.openclaw/openclaw.json
   ```
3. 获取当前 chat_id（从 inbound context 的 `chat_id` 字段取）
4. 计算时间戳（秒级）并执行拉取脚本：
   ```bash
   START_TS=$(python3 -c "import datetime; d=datetime.datetime(2026,2,24,0,0,tzinfo=datetime.timezone(datetime.timedelta(hours=8))); print(int(d.timestamp()))")
   END_TS=$(python3 -c "import datetime; d=datetime.datetime(2026,2,28,23,59,59,tzinfo=datetime.timezone(datetime.timedelta(hours=8))); print(int(d.timestamp()))")
   bash <skill_dir>/scripts/fetch_feishu_messages.sh <app_id> <app_secret> <chat_id> $START_TS $END_TS
   ```
5. 输出为 JSON lines，每行一条消息。过滤掉 `msg_type` 不是 `text` 或 `post` 的消息（图片、卡片等无法提取有效文本）。过滤掉机器人的"正在思考中..."等状态消息。

**注意事项：**
- 时间戳单位是**秒**（不是毫秒）
- 如果用户有多个群聊，可能需要拉取多个 chat_id 的消息
- 消息量可能很大，优先提取用户发的消息（sender_type=user），机器人回复作为补充上下文

### 数据源 B: 本地 Daily Memory 日志

读取 workspace 下的 memory 目录：
```bash
ls <workspace>/memory/YYYY-MM-DD.md  # 对应日期范围内的文件
```

如果日志存在，内容通常已经是整理过的工作要点，优先使用。

### 合并策略

- daily memory 有的内容优先使用（已整理过，质量高）
- 飞书聊天记录补充 memory 中没有的内容
- 去掉闲聊、调试、重复内容，只保留工作相关的实质内容

## Step 2: 整理输出

### 默认周报模板

```markdown
## 本周工作总结

[按工作模块分条列出，每条简洁描述做了什么、产出是什么]

## 关键成果与进展

[本周最重要的2-3个产出/里程碑]

## 下周工作计划

[基于本周工作的延续和未完成事项，按优先级排列]

## 遇到的问题与需要的支持

[阻塞项、跨团队协作需求、资源需求等]

## 其他备注

[可选：学习心得、工具探索、流程优化建议等]
```

### 输出原则

- **简洁**：每条工作描述控制在1-2行
- **结果导向**：强调产出而非过程（"输出了XX文档" 而非 "研究了很久XX"）
- **量化**：有数据的加数据（"完成了3个模块的测试，通过率95%"）
- **分类清晰**：按工作模块分组，不要流水账

### 用户自定义模板

如果用户提供了自定义模板格式，使用用户的格式。将收集到的素材按用户模板的结构重新组织。

## Daily Memory 写入（可选）

如果用户同意，在每次有实质工作内容的对话结束后，主动将当天要点写入：
```
<workspace>/memory/YYYY-MM-DD.md
```

格式：
```markdown
# YYYY-MM-DD 工作记录

## 工作内容
- [具体做了什么]

## 关键产出
- [文档/代码/配置等具体产出]

## 待跟进
- [未完成的事项]
```

这样下次生成周报时，日志已经准备好了。
