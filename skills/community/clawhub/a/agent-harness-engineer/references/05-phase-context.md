# Phase 5: 上下文管理

## 目标

设计四级压缩管道、会话WAL、记忆系统，在严格上下文约束下保障Agent持续执行能力。核心挑战：200K tokens看似充足，但一次复杂工具调用的结果可能轻易占用数万tokens，几轮对话后即触达上限。

---

# 设计原理

## 上下文即负债

每一次API调用的token消耗都是延迟和成本的直接映射。上下文不仅是"能记住多少"，更是"能跑多快"和"能跑多久"的组合约束。设计目标不是最大化上下文利用率，而是在保证任务正确性的前提下最小化冗余。

**核心洞察**：
- 一个120K token的结果中，80%的内容对后续决策无实际影响
- 工具输出越冗长，Agent越容易"迷失"，注意力被稀释
- 压缩的质量指标不是压缩率，而是压缩后的"任务可恢复性"

## 渐进式压缩的经济学

四级压缩的本质是成本阶梯：每一级仅在前一级不足时触发，避免"用大炮打蚊子"。

| 级别 | 成本 | 场景 |
|------|------|------|
| Snip | ~0ms, 0 API调用 | 90%的日常情况 |
| Microcompact | ~1ms, 0 API调用 | 工具输出过长 |
| Context-Collapse | ~5ms, 0 API调用 | 历史对话冗余 |
| Autocompact | ~2s, 1次API调用 | 前三者均不足 |

---

# 抽象接口层

系统设计为三层架构：

```
AgentCore
  └─ CompressionPipeline   ← 编排四级压缩，暴露 compact() 入口
       ├─ SnipStrategy
       ├─ MicrocompactStrategy
       ├─ CollapseStrategy
       └─ AutocompactStrategy
  └─ MemoryManager         ← 四分类记忆生命周期管理
       ├─ ShortTermStore    ← 内存中，本次会话
       └─ LongTermStore     ← 文件/向量DB，跨会话
  └─ SessionWAL            ← JSONL追加日志，可恢复
```

**CompressionPipeline** 不直接修改 `messages` 数组。它接收 `CompressionRequest {messages[], tokenBudget, reason}`，返回 `CompressionResult {compressedMessages[], tokensFreed, levelUsed, recoveryHints[]}`。这保证"压缩"与"消息管理"解耦。

**MemoryManager** 不嵌入AgentCore。它通过 `MemoryContextLoader` 以插件方式注入：Core在构造API请求时，调用Loader获取当前情景相关的记忆块，Loader内部查询MemoryManager并返回经过优先级排序的结果。

---

# 压缩算法描述

本章节描述**算法逻辑**而非可执行代码。所有描述使用伪代码格式表示控制流和数据结构操作。

## 通用前提

所有压缩策略统一从 `tokenCounter` 模块获取精确token数（通过模型原生tokenizer，不依赖 `len(content)/4` 估算）。`tokenCounter.count(text)` 返回精确值，`tokenCounter.estimate(structuredMessage)` 返回含元数据的估算。

压缩触发条件：`currentTokens > budget * 0.85`，且 `hasAttemptedReactiveCompact == false`（见陷阱章节）。

---

## Level 1: Snip（剪断）

**目标**：移除消息历史中最旧的连续片段。
**复杂度**：O(1) 数组操作。
**成本**：~0ms，无网络IO。

### 算法

```
FUNCTION snip(messages, targetTokensToFree):
    oldestBlock ← 取 messages 前 N 条消息，
                   使得这 N 条消息的 token 总和 ≥ targetTokensToFree
    remainder   ← messages[N:]

    ── 构建系统注入消息 ──
    injection ← {
        role: "system",
        content: "上下文已剪断。以下为已跳过的历史摘要：" +
                 生成 N 条消息的简要摘要（每条消息截取前80字符）
    }

    resultMessages ← [injection] + remainder
    tokensFreed   ← sum(tokenCount(oldestBlock))
    RETURN (resultMessages, tokensFreed)

    ── 边界条件 ──
    如果 N < 5: 不进行Snip（避免频繁微小剪断），返回原始消息
    如果 messages 总数 < 10: 不进行Snip，返回原始消息
```

**关键设计决策**：Snip 不静默删除——它注入一条 system 消息说明"已剪断"，让LLM感知到上下文的断裂点。否则Agent会困惑"之前聊的内容去哪了"。

**触发顺序**：Snip 是压缩管道的第一个入口。每次检查token预算时优先尝试。

---

## Level 2: Microcompact（微压缩）

**目标**：对超过阈值的工具调用结果进行头尾截断，保留关键信息。
**复杂度**：O(M) 遍历消息，M为消息总数。
**成本**：~1ms，纯字符串操作。

### 算法

```
FUNCTION microcompact(messages, resultThreshold=4000, headTokens=1500, tailTokens=500):
    freed ← 0
    FOR EACH msg IN messages WHERE msg.role == "tool":
        contentTokens ← tokenCount(msg.content)
        IF contentTokens ≤ resultThreshold:
            CONTINUE  ← 跳过短结果

        headContent ← 取前 headTokens 个token对应的文本
        tailContent ← 取后 tailTokens 个token对应的文本
        midTruncated ← contentTokens - headTokens - tailTokens

        separator ← "... [中间 {midTruncated} tokens 已截断] ..."

        msg.content ← headContent + separator + tailContent
        freed ← freed + midTruncated

    RETURN (messages, freed)
```

**关键设计决策**：

- **头尾保留**：工具输出的开头通常包含状态/概要，末尾通常包含结论/错误——两者都是决策关键信息。中段（例如大段日志或中间步骤）对后续推理价值低。
- **阈值差异化**：不同工具类型应有不同阈值。例如 `read_file` 输出阈值可设为 8000，`bash` 输出阈值可设为 2000。阈值由工具注册时的 `meta.outputProfile` 字段提供。
- **不可逆标注**：截断后的消息在元数据中标记 `microcompacted: true`，防止被重复截断。

---

## Level 3: Context-Collapse（上下文折叠）

**目标**：通过"读时投射"将N条连续历史消息折叠为一条摘要消息，但不修改原始消息数组——仅在读取上下文时动态注入折叠摘要。
**复杂度**：O(N) 遍历折叠窗口。
**成本**：~5ms，字符串模板拼接。

### 数据结构

```
collapseStore: Map<Int, CollapseEntry>
  key: 折叠起始消息的索引
  value: {
    originalSpan: [startIdx, endIdx],
    collapsedTokens: Int,
    summary: String,           ← 手工模板，非LLM生成
    collapsedAt: Timestamp,
    originalTotalTokens: Int
  }
```

### 算法（读时投射）

```
FUNCTION applyCollapseProjection(messages, collapseStore):
    projected ← []
    i ← 0
    WHILE i < len(messages):
        entry ← collapseStore.get(i)
        IF entry IS NOT NULL:
            projected.append({
                role: "system",
                content: "── 折叠上下文（{entry.originalSpan[1]-entry.originalSpan[0]}条消息）──\n" +
                         entry.summary
            })
            i ← entry.originalSpan[1]  ← 跳过折叠区间
            CONTINUE
        projected.append(messages[i])
        i ← i + 1
    RETURN projected

FUNCTION generateCollapseSummary(messagesInSpan):
    ── 构建模板化摘要，不调用LLM ──
    summary ← ""

    FOR EACH msg IN messagesInSpan:
        IF msg.role == "user":
            summary ← summary + "用户: " + truncate(msg.content, 200) + "\n"
        ELSE IF msg.role == "assistant" AND msg有tool_calls:
            summary ← summary + "调用了工具: "
            FOR EACH tc IN msg.tool_calls:
                summary ← summary + tc.name + " "
            summary ← summary + "\n"
        ELSE IF msg.role == "tool":
            summary ← summary + "工具结果(" + tokenCount(msg.content) + " tokens)\n"
        ELSE:
            summary ← summary + "消息(" + tokenCount(msg.content) + " tokens)\n"

    RETURN summary
```

**关键设计决策**：

- **不修改原数组**：与 Snip/Microcompact 不同，Collapse 不改变 `messages` 数组本身。它只在 `buildAPIRequest()` 阶段通过投射生成轻量版本。这意味着 Collapse 是可回退的——如果后续需要完整历史进行调试，原始消息仍然完整。
- **Collapse触发时机**：当消息数组包含连续20+条"非决策关键"的消息时。决策关键消息包括：tool_calls、plan变更、task status变更。非关键消息包括：纯文本对话、确认消息、无工具调用的assistant回复。
- **去重检查**：折叠前检查 bloom filter，避免已折叠区间被重复折叠。

---

## Level 4: Autocompact（自动压缩）

**目标**：调用LLM对整段对话历史进行语义摘要，是唯一涉及API调用的压缩级别。仅在前三级均不足以释放足够token空间时触发。
**成本**：1次完整的LLM API调用（~2s延迟）。

### 算法

```
FUNCTION autocompact(messages, targetFreeTokens, llmClient):
    ── 第一步：定位压缩区间 ──
    compressionStart ← 0
    accumulatedTokens ← 0
    FOR i FROM len(messages)-1 DOWN TO 0:   ← 从尾部向头部扫描
        accumulatedTokens ← accumulatedTokens + tokenCount(messages[i])
        IF accumulatedTokens ≥ targetFreeTokens:
            compressionStart ← i
            BREAK

    IF compressionStart == 0:
        RETURN FAILURE("无法压缩足够空间")

    historicalMsgs ← messages[0:compressionStart]
    recentMsgs    ← messages[compressionStart:]
    ── 保留最后10条消息不压缩（最近的上下文最重要）──
    IF len(recentMsgs) < 10:
        compressionStart ← max(0, len(messages) - 10)
        historicalMsgs ← messages[0:compressionStart]
        recentMsgs ← messages[compressionStart:]

    ── 第二步：调用LLM生成摘要 ──
    compactPrompt ← """
    请对以下对话历史进行结构化摘要，保留以下关键信息：
    1. 用户的核心目标（当前任务是什么）
    2. 已完成的步骤（按顺序列出）
    3. 关键决策点（触发了哪些工具，为什么要触发）
    4. 未解决的问题/待处理的任务
    5. 当前工作的文件清单
    6. 正在使用的Skill/工具上下文

    格式：简洁，使用要点列表。不要包含无关的闲聊内容。
    """
    summary ← llmClient.invoke(compactPrompt + 序列化(historicalMsgs))

    ── 第三步：构建恢复提示 ──
    recoveryMessage ← {
        role: "system",
        content: "── 上下文压缩点（Autocompact）──\n" +
                 "以下历史已被压缩为摘要，但关键状态已保留：\n\n" +
                 summary + "\n\n" +
                 "── 恢复指令 ──\n" +
                 "1. 继续执行未完成的任务\n" +
                 "2. 必要时重新读取当前工作文件\n" +
                 "3. 正在使用的工具上下文已在前置消息中恢复"
    }

    resultMessages ← [recoveryMessage] + recentMsgs
    RETURN (resultMessages, tokenCount(historicalMsgs) - tokenCount(summary))
```

**关键设计决策**：

- **从尾到头扫描**：Autocompact 从消息历史尾部向头部累加 token，确定最小压缩区间。这保证压缩的是"最旧且最不重要"的部分。
- **结构化摘要Prompt**：摘要不是自由文本，而是包含6个固定字段的结构化模板。这确保LLM压缩后的信息密度可预期，后续Agent能可靠地从摘要中恢复状态。
- **恢复消息**：压缩后不是简单替换，而是插入一条带恢复指令的system消息——明确告诉LLM"你需要从头恢复状态"。

---

# 记忆系统设计

## 四分类记忆模型

记忆不是模糊的"上下文"，而是有明确生命周期和存储策略的四类数据：

| 类别 | 作用域 | 存储介质 | 生命周期 | 示例 |
|------|--------|----------|----------|------|
| **User** | 用户级别 | 长期存储 | 永不过期 | 用户偏好（语言、代码风格）、常用项目路径 |
| **Feedback** | 项目/任务级 | 长期存储 | 按反馈时效 | "上次你建议用async，但这里用sync更合适" |
| **Project** | 项目级别 | 长期存储 | 随项目演进 | 项目结构、技术栈、依赖关系、约定 |
| **Reference** | 跨项目 | 长期存储 | 按有效期 | API文档摘要、最佳实践片段 |

### User记忆

存储用户偏好和习惯。结构：
```
UserMemory {
    preferences: { language: "zh-CN", codeStyle: "PEP8", verbosity: "concise" },
    history: [{ query_pattern, preferred_tool, timestamp }, ...]
}
```
User记忆不经过auto-dream——它是累积性的，只在用户显式更新时修改。

### Feedback记忆

存储LLM/Action纠正反馈。结构：
```
FeedbackMemory {
    entries: [{
        correction_type: "tool_choice" | "code_style" | "approach" | "other",
        original_action: String,
        corrected_action: String,
        context_snippet: String,     ← 触发事件前后3轮对话
        timestamp: Timestamp,
        ttl: Duration                 ← 超时自动清理
    }, ...]
}
```
每一行feedback有TTL。例如"代码风格"反馈可能TTL=30天，"tool_choice"反馈可能TTL=7天。

### Project记忆

存储当前项目结构和技术上下文。结构：
```
ProjectMemory {
    root_path: String,
    file_index: Map<Path, FileMeta>,     ← 文件结构快照
    tech_stack: { language, framework, package_manager, ... },
    conventions: [String],                ← 命名规范、目录结构约定
    last_scan: Timestamp
}
```
Project记忆在每次session开始时通过文件系统扫描刷新。刷新策略：比较 `last_scan` 和文件修改时间，仅增量更新。

### Reference记忆

存储外部知识的摘要。结构：
```
ReferenceMemory {
    entries: [{
        source: URL | file_path | "inline",
        topic: String,
        summary: String,              ← 由LLM生成的摘要（≤500 tokens）
        original_length: Int,
        embeddings: Vector,           ← 仅Enterprise
        timestamp: Timestamp
    }, ...]
}
```

---

## Auto-Dream 机制

"Auto-dream"（自动做梦）是将短期记忆整合为长期记忆的异步过程。它的设计灵感来自人类睡眠中的记忆巩固——在Agent空闲或session结束时触发。

### 触发条件（满足任一即触发）

```
条件A: short_term_buffer.length > THRESHOLD_COUNT (默认20)
条件B: session.isEnding == true 且 short_term_buffer.length > 0
条件C: 距离上次auto-dream > DREAM_INTERVAL (默认30分钟) 且 short_term_buffer.length > 5
```

### 做梦流程

```
FUNCTION auto_dream(shortTermBuffer, longTermStore):
    ── 第一步：分类 ──
    classified ← classifyEntries(shortTermBuffer)
    # 返回 {feedback: [...], reference: [...], project: [...], user: [...]}

    ── 第二步：对每类分别整合 ──
    FOR EACH (category, entries) IN classified:
        IF entries IS EMPTY: CONTINUE

        ── 对非Feedback类：调用LLM进行归纳 ──
        IF category ∈ {reference, project, user}:
            dreamPrompt ← 构建类别专属的归纳prompt
            consolidated ← llm.invoke(dreamPrompt + 序列化(entries))
            longTermStore.upsert(category, consolidated)

        ── 对Feedback类：逐条持久化（不归纳，保留精确内容）──
        ELSE IF category == "feedback":
            FOR EACH entry IN entries:
                longTermStore.appendFeedback(entry)

    ── 第三步：清空短期缓冲 ──
    shortTermBuffer.clear()

    ── 第四步：记录dream日志 ──
    SessionWAL.write({
        type: "AUTO_DREAM",
        entries_count: totalEntries,
        categories: classified.keys()
    })
```

### 归纳Prompt模板（按类别）

```
用于 Reference 记忆：
"请将以下多条相关reference条目归纳为一条不超过500 tokens的摘要。
 保留所有可复用的代码模式、API签名和关键数值。"

用于 Project 记忆：
"请将以下项目结构变化记录合并到现有Project记忆中。
 仅更新有变化的部分，不变的部分不重复。"

用于 User 记忆：
"请提取以下用户交互中的新偏好或习惯变更。
 仅输出变更项，已存在的偏好不重复。"
```

---

# Session WAL 设计集成

Session WAL（Write-Ahead Log）是会话的持久化事件日志，采用追加写入的JSONL格式，是恢复和审计的基础设施。

## 设计原理

- **追加仅写**：每行一个JSON事件，尾部追加，O(1)写入
- **幂等可回放**：每个事件有唯一 `seq_id`，重放时跳过已处理的序列号
- **崩溃安全**：每个事件写入后 fsync，保证磁盘持久化
- **定时checkpoint**：每N个事件后创建快照行，减少重放启动时间

## 5种事件类型

| 类型 | 字段 | 含义 |
|------|------|------|
| `USER_INPUT` | `{seq_id, content, timestamp}` | 用户发送消息 |
| `TOOL_CALL` | `{seq_id, tool_name, params_hash, timestamp}` | Agent调用工具（不记录完整参数，仅hash） |
| `TOOL_RESULT` | `{seq_id, tool_name, result_tokens, success, error?, duration_ms, timestamp}` | 工具执行结果摘要 |
| `COMPRESSION` | `{seq_id, level, input_tokens, output_tokens, duration_ms, timestamp}` | 压缩事件 |
| `CHECKPOINT` | `{seq_id, messages_tokens, memory_size, pending_tasks[], timestamp}` | 会话快照 |

### 事件格式示例

```jsonl
{"seq":1,"type":"USER_INPUT","content_hash":"a1b2c3","timestamp":"2026-05-20T10:00:00Z"}
{"seq":2,"type":"TOOL_CALL","tool":"read_file","params_hash":"d4e5f6","timestamp":"2026-05-20T10:00:01Z"}
{"seq":3,"type":"TOOL_RESULT","tool":"read_file","result_tokens":1200,"success":true,"duration_ms":45,"timestamp":"2026-05-20T10:00:01Z"}
{"seq":4,"type":"CHECKPOINT","messages_tokens":45200,"memory_size":12,"pending_tasks":["fix_bug_1"],"timestamp":"2026-05-20T10:05:00Z"}
{"seq":5,"type":"COMPRESSION","level":1,"input_tokens":98000,"output_tokens":65000,"duration_ms":2,"timestamp":"2026-05-20T10:10:00Z"}
```

## 重放/恢复机制

```
FUNCTION replay_session(walFile):
    lastCheckpoint ← NULL
    eventsAfterCheckpoint ← []

    ── 第一遍扫描：找最近checkpoint ──
    FOR EACH line IN walFile (逆序):
        event ← parseJSON(line)
        IF event.type == "CHECKPOINT":
            lastCheckpoint ← event
            BREAK

    ── 第二遍扫描：从checkpoint之后重放 ──
    startSeq ← lastCheckpoint?.seq ?? 0
    FOR EACH line IN walFile WHERE line.seq > startSeq:
        event ← parseJSON(line)
        eventsAfterCheckpoint.append(event)

    ── 重建会话状态 ──
    sessionState ← {
        pendingTasks: lastCheckpoint.pending_tasks,
        messagesTokens: lastCheckpoint.messages_tokens,
        replayEvents: eventsAfterCheckpoint
    }
    RETURN sessionState
```

**恢复场景**：
- **进程崩溃**：重启时从WAL恢复会话状态，重放未完成的事件
- **网络中断**：API调用中断时，从WAL确定最后成功步骤，避免重复操作
- **手动回滚**：定位到特定 seq_id 的checkpoint，将对话状态回滚到该点

---

# AI构建提示

以下是面向AI编码助手的实现指引，不是面向用户的文档。

```
BUILD INSTRUCTIONS FOR AI:

1. 首先实现 tokenCounter 模块 —— 它是所有压缩算法的基础。
   使用 tiktoken（对应模型的编码器），不要用 len/4 估算。
   tokenCounter 必须提供：
   - count(text: str) → int
   - countMessages(messages: list) → int
   - countStructured(msg: dict) → int  （含 role 和 tool_calls 的 overhead）

2. 压缩管道按 Level 1→4 的顺序实现。
   每个Level是一个独立类，实现统一的 compress(request)→CompressionResult 接口。
   不要在 CompressionPipeline.compact() 中写 if-else 分发——使用策略链模式，
   每个策略返回 Optional[CompressionResult]，链式尝试直到第一个非None。

3. MemoryManager 必须是异步安全的。
   短期缓冲区用 asyncio.Lock 保护，长期存储用文件锁或DB事务。
   auto-dream 必须在后台线程/协程中执行，不得阻塞主Agent循环。

4. SessionWAL 写入路径必须使用 append-only 文件打开模式（'a'）。
   每个事件写入后调用 flush()（非 fsync，仅在checkpoint时 fsync）。
   WAL文件按 session_id 命名：wal_{session_id}.jsonl

5. 恢复机制的关键：compaction后必须立即在WAL中写 CHECKPOINT 事件，
   记录当前压缩级别、剩余token数、待处理任务列表。
   这使得崩溃恢复时可以知道"压缩到了哪一步"。

6. 不要在压缩后丢弃文件内容引用 —— 维护一个 currentFiles[] 列表，
   每次 compaction 后重新注入到 system prompt 中。

7. hasAttemptedReactiveCompact 标志：
   - 初始化为 false
   - 任何一次 compaction 调用后设为 true
   - 仅在成功处理LLM响应后重置为 false
   - 如果 compaction 后立刻再次触发 compact（错误恢复循环），
     检测到 flag=true 时跳过压缩，返回错误让上层决定降级或放弃
```

---

# 规模适应性指南

## Minimal 配置

适用于：原型开发、个人项目、单次短对话。
- 压缩：仅 Level 1 Snip。Snip阈值设为50条消息。
- 记忆：不使用。每次对话从头开始。
- WAL：不使用。崩溃后对话无法恢复。
- Token计数：允许 `len/4` 估算。

```
示例场景：写一个200行的Python脚本，对话不超过30轮。
压缩永远不触发，上下文完全足够。
```

## Professional 配置

适用于：日常开发、中等复杂度项目、多文件编辑。
- 压缩：完整四级管道。Snip阈值=20条，Microcompact阈值=4000 tokens，Collapse窗口=15条，Autocompact token目标=50%。
- 记忆：文件级。四分类存储为独立JSON文件，auto-dream仅触发条件B（session结束）。
- WAL：JSONL文件，每100事件checkpoint一次。
- Token计数：使用tiktoken精确计数。

```
示例场景：跨5个文件的bug修复，对话100+轮。
Level 1-3覆盖95%压缩需求，仅在极端情况下触发Level 4。
```

## Enterprise 配置

适用于：持续运行Agent、大型项目、多session协作。
- 压缩：四级+压缩恢复（compaction后自动重建被压缩的上下文）。
- 记忆：向量数据库（如Qdrant/Chroma）。四分类各建一个collection。
  - User记忆索引在 `user_preferences` collection
  - Project记忆增量更新，每次文件变更自动更新embeddings
  - auto-dream全量触发（条件A+B+C），在后台协程中执行，不阻塞主循环
- WAL：JSONL + SQLite双写（WAL用于实时恢复，SQLite用于查询统计）。
- Token计数：模型原生tokenizer + 预留1000 token buffer。
- 附加值：压缩事件可观测（metrics上报压缩频率、各级别占比、节省token数）。

```
示例场景：持续运行数月的CI/CD Agent。
Enterprise配置确保跨session记忆连续，压缩管道维持成本可控。
```

---

# 检查清单

- [ ] tokenCounter使用模型原生tokenizer，非估算
- [ ] Snip后注入system消息声明"已剪断"
- [ ] Microcompact按工具类型差异化阈值
- [ ] Microcompact标记已截断消息，防止重复截断
- [ ] Context-Collapse不修改原messages数组，仅读时投射
- [ ] Collapse去重检查（bloom filter）
- [ ] Autocompact从尾向头扫描，保留最近10条消息
- [ ] Autocompact摘要使用6字段结构化模板
- [ ] 压缩后恢复：文件内容、Skill上下文、Plan、任务列表
- [ ] hasAttemptedReactiveCompact标志正确维护
- [ ] 压缩后写入WAL CHECKPOINT事件
- [ ] 记忆四分类各独立存储，auto-dream对各类用不同策略
- [ ] auto-dream异步执行，不阻塞Agent主循环
- [ ] WAL追加写入，每行JSON独立
- [ ] WAL恢复机制可处理崩溃/中断/手动回滚

---

# 常见陷阱

## 陷阱1：压缩后丢失关键状态

**症状**：Agent在压缩后突然"失忆"——忘记正在编辑的文件、忘记当前Plan的第几步、忘记已加载的Skill指令。

**根因**：压缩算法只处理了消息历史，但没有主动重建易失上下文。

**解决（必须实现）**：
- 每轮压缩完成后，执行 `activeRestore` 步骤：
  1. 检查 `currentFiles[]` 列表，对每个当前工作文件调用 `read_file` 并将结果注入为 system 消息
  2. 检查 `activeSkill`，将 Skill 的核心指令（前1500 tokens）重新注入 system prompt
  3. 检查 `activePlan`，将计划摘要（当前步骤+下一步）注入 system prompt
  4. 检查 `pendingTasks[]`，将待处理任务列表注入 system prompt
- `activeRestore` 是压缩管道的强制后置步骤，不是可选优化。

## 陷阱2：无限压缩循环

**症状**：compaction → 释放空间 → LLM生成大量输出 → 再次触发compaction → 释放空间 → ... 死循环。

**根因**：压缩后上下文仍然不足，或压缩释放的空间被新响应立即填满。

**解决（必须实现）**：
- `hasAttemptedReactiveCompact` 标志：
  - 初始值 `false`
  - compaction() 调用时设为 `true`
  - 仅在成功接收并处理完一次完整的LLM响应后重置为 `false`
  - 如果 `true` 时再次检测到需要压缩：**跳过压缩**，返回 `CONTEXT_EXHAUSTED` 错误
- 上层捕获 `CONTEXT_EXHAUSTED` 后执行降级策略：
  - **Professional**：仅保留最后3条消息+system prompt，强制Level 4压缩
  - **Enterprise**：触发全量Autocompact+clear所有非关键记忆

## 陷阱3：Token计数不精确

**症状**：明明预算还有空间，API却报 `context_length_exceeded`。或者：明明还可以发更多消息，却过早触发压缩。

**根因**：使用 `len(content)/4` 估算，忽视 tool_calls、role 标注、system prompt 等元数据的token开销。

**解决**：
- 必须使用模型原生tokenizer（tiktoken或HuggingFace tokenizer匹配模型）
- 每条消息的token计数必须包含：`role` 字段的markers（~4 tokens）+ 内容本身的tokens + `tool_calls` 结构的JSON overhead
- 预留5%安全buffer：`effectiveBudget = maxTokens * 0.95`
- 在budget的85%处触发压缩（而非100%），为压缩过程本身预留操作空间

## 陷阱4：auto-dream阻塞主循环

**症状**：session结束时Agent卡死数秒。

**根因**：auto-dream中调用了LLM进行归纳，而归纳请求阻塞了主循环退出。

**解决**：
- auto-dream必须在独立的后台协程/线程中执行
- session结束时的auto-dream使用 `timeout`（例如5秒），超时则直接写原始条目（不归纳）
- 不要等待auto-dream完成才返回结果给用户

## 陷阱5：WAL文件无限增长

**症状**：长时间运行后 WAL 文件达到数GB。

**解决**：
- 每次CHECKPOINT后，标记该checkpoint之前的所有事件为"可归档"
- 每N个checkpoint后（例如10个），将旧事件归档到 `wal_archive/`，删除主WAL中已归档行
- archive保留7天，过期自动清理

---

## 下一步

完成Phase 5后，进入 **Phase 6: 权限安全**（参考 `references/06-phase-permissions.md`）