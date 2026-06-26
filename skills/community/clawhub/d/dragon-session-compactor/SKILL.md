---
name: session-compactor
description: >
  上下文压缩技能。当对话越来越长、token快爆的时候，自动压缩旧消息为摘要，保留最近上下文。
  触发条件：
  - "压缩会话"、"compact"、"上下文满了"
  - 检测到消息超过阈值（默认100条或token估计超过80000）
  - 手动调用 $compact
  无外部依赖，纯Node.js实现。
---

# Session Compactor - 上下文压缩系统

## 核心概念

```
原始会话: [msg1, msg2, ..., msgN]
    ↓ 检测到需要压缩
    ↓ 提取关键信息
    ↓ 生成摘要
压缩后会话: [System(摘要), msg(N-3), msg(N-2), msg(N-1), msgN]
```

## 配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `preserveRecent` | 4 | 保留最近N条消息 |
| `maxTokens` | 80000 | 超过此token数触发压缩 |
| `summaryMaxTokens` | 2000 | 摘要最大token数 |
| `storePath` | ./.clawsession.json | 会话存储路径 |

## 数据结构

### Session 文件格式 (.clawsession.json)

```json
{
  "version": 1,
  "createdAt": "2026-04-06T...",
  "updatedAt": "2026-04-06T...",
  "messages": [...],
  "compactionCount": 0,
  "totalTokens": 12345
}
```

### 消息格式

```json
{
  "role": "user|assistant|system|tool",
  "content": "...",
  "timestamp": "ISO8601",
  "toolUse": {
    "name": "read_file",
    "input": "..."
  }
}
```

## 快速使用

```bash
# 手动压缩
node scripts/compact.mjs run

# 检查当前会话状态
node scripts/compact.mjs status

# 强制压缩（忽略阈值）
node scripts/compact.mjs compact --force

# 查看压缩历史
node scripts/compact.mjs history
```

## API 接口

```javascript
const { SessionCompactor } = require('./scripts/compact.mjs');

const compactor = new SessionCompactor({
  preserveRecent: 4,
  maxTokens: 80000,
  storePath: './.clawsession.json'
});

// 检查是否需要压缩
const needsCompaction = compactor.shouldCompact();

// 执行压缩
const result = compactor.compact();
console.log(`压缩了${result.removedCount}条消息`);

// 估算当前token
const tokens = compactor.estimateTokens();
console.log(`当前约${tokens} tokens`);
```

## 压缩算法

### 1. 提取关键信息

从旧消息中提取：
- **关键文件路径**（.rs, .py, .ts, .json, .md）
- **工具调用记录**（bash, read_file, write_file等）
- **待办事项**（todo, next, pending, follow up）
- **用户请求**（最近的3条用户消息）
- **AI响应摘要**（每条AI响应的核心内容）

### 2. 生成摘要格式

```markdown
<summary>
## 会话摘要

**压缩次数**: 2
**时间范围**: 2026-04-06 10:00 - 16:00
**总消息数**: 48条（已压缩2次）

### 关键操作
- 工具调用: bash(x3), read_file(x5), write_file(x2)
- 主要文件: src/main.py, SKILL.md, evolution-log.md

### 用户主要请求
1. 创建 efficiency-hub 技能
2. 发布 efficiency-hub 到 Clawhub
3. 学习 Claw Code 架构

### 待完成事项
- 继续改进 chat-memory-v2
- 完善工具注册表

### 最近消息（未压缩）
- [保留最近4条消息原文]
</summary>
```

### 3. 增量压缩

如果之前已经压缩过，摘要会累积：

```markdown
<summary>
## 会话摘要

**压缩次数**: 3

### 早期上下文（压缩于 10:00）
[第一次压缩的摘要内容]

### 近期上下文（压缩于 14:00）
[第二次压缩的摘要内容]

### 最新摘要（压缩于 16:00）
[第三次压缩的摘要内容]

### 最近消息
[保留的4条消息]
</summary>
```

## Token 估算

简单估算（无需外部库）：
```
tokens ≈ 总字符数 / 4 + 工具调用次数 * 10
```

## 文件清单

```
session-compactor/
├── SKILL.md              # 本文件
├── scripts/
│   └── compact.mjs       # 核心压缩逻辑
└── references/
    └── compaction-log.md # 压缩操作日志
```

## 使用场景

1. **自动触发** — 在 heartbeat 或 cron 任务中检查是否需要压缩
2. **手动调用** — 用户说"压缩一下"
3. **定时压缩** — 每小时自动检查

## 集成到 OpenClaw

在 HEARTBEAT.md 中加入：

```markdown
## 自动压缩检查
每30分钟检查一次会话长度，超过阈值自动压缩
```

---

_龙虾王子自我进化的成果 🦞_
