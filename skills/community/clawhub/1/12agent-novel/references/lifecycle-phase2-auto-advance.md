# Phase 2 自动推进、批量写作、读者模拟机制（闭环增强版）

> 下文出现的 `read()`、`readConfig()`、`sessions_spawn()` 等代码块均为**示意性伪代码**，用于说明调度逻辑与输入拼装方式，不代表宿主环境必须提供同名 API。

## 批量写作

用户指令格式："写第X章到第Y章"

1. Coordinator 解析范围
2. 先执行 `references/resume-protocol.md`
3. 对每章判定轨道（常规/重点），从 `meta/config.md` 读取 `key_chapters`
4. **顺序执行完整闭环**：每章必须完成对应 Phase 2 工作流并 closed 后，才允许进入下一章
5. 每章完成后：向用户反馈进度、更新 `metadata.json`、更新 `workflow-state.json`、检查滚动摘要触发、检查读者模拟触发
6. 异常处理：遇模型拒绝且无法回退 → 暂停 → 报错通知用户
7. 全部完成后：汇总报告

> 批量写作不是"连写正文"，而是"连续执行多个章节闭环"。

---

## 自动推进机制

### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| auto_advance_chapters | 正整数 | 4 | 一次自动写N章 |
| write_interval_seconds | 正整数 | 6 | API缓冲间隔 |
| auto_confirm | 布尔 | false | 是否自动确认 |

### 快捷配置

| 场景 | chapters | interval | confirm |
|------|----------|----------|---------|
| 中速日常（默认） | 4 | 6 | false |
| 高速大批量 | 8 | 4 | false |
| 慢速审慎 | 2 | 10 | false |

### 自动推进流程

```text
1. 初始化
   → 执行恢复协议
   → remaining = auto_advance_chapters
   → current_chapter = X
   → status = "running"

2. 循环（while remaining > 0）
   → 执行当前章节写作（双轨工作流）
   → 确认本章已 closed
   → 成功后：remaining--, current_chapter++
   → 执行存档+滚动摘要+读者模拟触发检查
   → 等待 write_interval_seconds 秒
   → 反馈进度

3. 全部完成后：
   → 汇总报告
   → remaining = 0
   → status = "completed"
   → resumeRequired = true
```

> 若某一章未完成 closed，循环必须中止，不得"先写下一章再补档"。

---

## 状态管理

`meta/metadata.json` 扩展字段：

```json
{
  "writingProgress": {
    "autoAdvance": {
      "enabled": true,
      "remaining": 8,
      "totalRequested": 10,
      "currentChapter": 15,
      "intervalSeconds": 6,
      "autoConfirm": false,
      "status": "running"
    }
  }
}
```

`meta/workflow-state.json` 约束：

```json
{
  "chapterWorkflow": {
    "currentChapter": 15,
    "lastClosedChapter": 14,
    "resumeRequired": false,
    "currentTrack": "normal"
  },
  "milestoneAudit": {
    "lastMilestoneAuditChapter": 0,
    "lastAuditResult": "green",
    "pendingWarnings": [],
    "nextAuditChapter": 20
  }
}
```

状态流转：`idle` → `running` → `completed` / `paused` / `failed`

---

## 章节闭环检查（自动推进专用）

每轮循环结束前，Coordinator 必须确认：
- 当前章正文已写入 `chapters/ch{NNN}.md`
- `chapter_name.md` 已更新
- `metadata.json` 已更新
- `workflow-state.json` 已更新
- tracker 已更新
- 触发检查已执行（Rolling Summary / Reader Feedback）
- 已向用户汇报该章或该批次进度

若任一项为否：
- `autoAdvance.status = "paused"`
- `resumeRequired = true`
- 记录日志到 `archive/archive.md`
- 停止循环

**里程碑审计检查（每章 closed 后必须执行）：**

```text
if (lastClosedChapter % 20 === 0 && lastClosedChapter > 0
    && lastMilestoneAuditChapter < lastClosedChapter) {
  // 暂停自动推进循环
  autoAdvance.status = "paused"
  // 执行里程碑审计（见 references/milestone-audit.md）
  // 审计完成后恢复循环：autoAdvance.status = "running"
}
```

> 里程碑审计触发优先级高于继续推进下一章。审计结果为 🔴 红色时，不得恢复自动推进，需等待用户指令。

---

## 异常处理

1. 捕获异常（模型拒绝、API失败、超时>120s、P0违规、闭环失败）
2. 立即暂停（`status = "paused"`）
3. 标记 `resumeRequired = true`
4. 记录日志到 `archive/archive.md`
5. 向用户提供选项：继续 / 跳过 / 停止

---

## 恢复机制

- 用户发"继续写作" → **先执行恢复协议** → 读取 autoAdvance 状态 → 从断点恢复
- 用户发"停止写作" → `status = "idle"`, `remaining = 0` → 保存进度 → `resumeRequired = true`

---

## 滚动摘要生成规则

触发时机：每完成 5 章时生成一次；或完成幕 / 大节点时立即生成

\u003e **异步执行：** 以 `mode: "run"` 触发后主控不等待结果，立即记录 `lastRollingSummaryChapter = endCh` 并继续推进。结果由子 Agent 自行写入 `references/rolling-summary.md`。主控在下一章恢复协议时检查文件是否已写入，若缺失则补做。

调用 RollingSummarizer Agent

```javascript
sessions_spawn({
  task: `${read("references/agent-rolling-summarizer.md")}

【本次任务】
将第${startCh}章到第${endCh}章压缩为≤2200字的滚动摘要。

【输入材料】
- 前期摘要: ${existingSummary}
- 最近5章原文: ${recentChapters}

【输出格式】
## 滚动摘要 Ch${startCh}-Ch${endCh}
### 主题进展与情感主弧
### 核心角色当前心理状态与关系变化关键节点
### 已埋设但未回收的重要伏笔清单
### 当前世界/势力/主角状态概要`,
  label: "rolling-summarizer-ch" + endCh,
  model: readConfig("meta/config.md", "rollingSummarizer"),
  mode: "run"  // 异步，主控不阻塞等待
})
```

触发后立即记录：
- `lastRollingSummaryChapter = endCh`

若子 Agent 执行失败（下一章恢复协议检查时发现文件未写入）：
- Coordinator 生成过渡摘要写入 `references/rolling-summary.md`
- 在 `archive/archive.md` 标记"待补正式摘要"

---

## 读者模拟触发

自动触发：每完成 5 章
手动触发：用户发"读者反馈"

\u003e **异步执行：** 以 `mode: "run"` 触发后主控不等待结果，立即记录 `lastReaderFeedbackChapter = endCh` 并继续推进。结果由子 Agent 自行写入 `archive/reader-feedback/feedback-ch{NNN}.md`。主控在下一章恢复协议时检查文件是否已写入，若缺失则补做。

```javascript
sessions_spawn({
  task: `${read("references/agent-reader-simulator.md")}

【本次任务】
分析最近5章（Ch${startCh}-Ch${endCh}）的全文内容，给出读者视角反馈。

【输入材料】
- 最近5章原文（全文）: ${recentChapters}
- 需要时可附带最近5章的滚动摘要作为辅助: ${rollingSummary}

【输出要求】
节奏评估、爽点分布、情感浓度分析、具体改进建议；请更像资深书评人，语气可以直接，问题必须具体到章节/场景/原因`,
  label: "reader-simulator-ch" + endCh,
  model: readConfig("meta/config.md", "readerSimulator"),
  mode: "run"  // 异步，主控不阻塞等待
})
```

触发后立即记录：
- `lastReaderFeedbackChapter = endCh`

若子 Agent 执行失败（下一章恢复协议检查时发现文件未写入）：
- 记录失败原因到 `archive/archive.md`
- 不阻断已 closed 的章节
- 必须在后续恢复协议中被识别为待补项
