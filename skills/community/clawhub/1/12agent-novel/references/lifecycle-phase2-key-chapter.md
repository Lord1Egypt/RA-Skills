# Phase 2 重点章节工作流（硬闭环版，典型 5-6 次子 Agent 调用）

> 下文出现的 `read()`、`readConfig()`、`sessions_spawn()` 等代码块均为**示意性伪代码**，用于说明调度逻辑与输入拼装方式，不代表宿主环境必须提供同名 API。

## 重点章节判定

满足任一条件即为重点章节：
- 用户手动指定"重点章"
- 细纲标注：高潮/转折/情感爆发
- 首章(Ch1)
- 末章(ChN，从meta/config.md读取total_chapters)
- 幕间分界章（从meta/config.md的key_chapters读取）

---

## 先决条件（强制）

进入本流程前，Coordinator 必须先：
1. 读取 `references/workflow-state-machine.md`
2. 读取 `references/resume-protocol.md` 并完成恢复校验
3. 确认 `meta/metadata.json.project.phase = 2`
4. 确认 `meta/workflow-state.json.phaseState.currentPhase = 2`
5. 确认不存在未闭环章节

---

## 工作流

### Step 0：恢复与轨道锁定（强制）

Coordinator 必须更新 `meta/workflow-state.json`：
- `chapterWorkflow.currentChapter = chapterNum`
- `chapterWorkflow.currentTrack = "key"`
- `chapterWorkflow.chapterEntryChecklistComplete = false`
- 重置 `currentChapterArtifacts`
- `resumeRequired = false`

---

### Step 1：Coordinator 读取存档 + 写前核查（强制）

同常规章节，但不得省略任何核查项。

> **Session Cache 优化：** 固定层（world.md 摘要 / 角色圣经摘要 / outline.md）在同一会话内只需读取一次，后续章节直接复用，无需重复读取文件。会话重启或发生世界观/角色/大纲变更时刷新。详见 `references/session-cache.md`。

完成后更新：
- `chapterEntryChecklistComplete = true`
- `currentChapterArtifacts.plan = true`

---

### Step 2：spawn FinalReviewer 做本章规划

```javascript
sessions_spawn({
  task: `${read("references/agent-final-reviewer.md")}

【本次任务】
作为章节规划师，为第${chapterNum}章（重点章节：${chapterType}）设计详细作战图。

【输入材料】
- 风格锚定: ${read("meta/style-anchor.md")}
- 本章细纲: ${chapterOutline}
- 世界观摘要: ${worldSummary}
- 角色圣经摘要: ${characterSummary}

【输出要求】
- 情感节点设计 + 节奏设计 + 关键场景拆解
- 标注风格锚定执行要点
- 标注字数目标`,
  label: "final-reviewer-plan-ch" + chapterNum,
  model: readConfig("meta/config.md", "finalReviewer"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

---

### Step 3：spawn MainWriter → 初稿

```javascript
sessions_spawn({
  task: `${read("references/agent-main-writer.md")}

【本次任务】
完成第${chapterNum}章的初稿（重点章节：${chapterType}）。

【输入材料】
- 风格锚定: ${read("meta/style-anchor.md")}
- 本章细纲: ${chapterOutline}
- 本章规划（FinalReviewer产出）: ${chapterPlan}
- 世界观摘要: ${worldSummary}
- 角色圣经摘要: ${characterSummary}
- 滚动摘要: ${rollingSummary}
- 最近3章原文: ${recentChapters}
- 本章相关伏笔/关系: ${onDemandContext}
- 字数目标: ${wordTarget}字

${isSensitive ? sensitivityConstraint : ""}

请仅输出初稿正文，不做润色。`,
  label: "main-writer-draft-ch" + chapterNum,
  model: readConfig("meta/config.md", "mainWriter"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

完成后更新：`currentChapterArtifacts.draft = true`

---

### Step 4：spawn MainWriter → 润色

```javascript
sessions_spawn({
  task: `${read("references/agent-main-writer.md")}

【本次任务】
对第${chapterNum}章初稿进行全面润色，输出最终润色版本。

【输入材料】
- 风格锚定: ${read("meta/style-anchor.md")}
- 初稿正文: ${draftText}
- 本章规划: ${chapterPlan}

请重点优化：语言流畅度、氛围浓度、感官细节、节奏感。输出完整润色版正文。`,
  label: "main-writer-polish-ch" + chapterNum,
  model: readConfig("meta/config.md", "mainWriter"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

完成后更新：`currentChapterArtifacts.polish = true`

---

### Step 5：[条件] spawn BattleAgent → 战斗段落

仅在细纲/本章规划标注"高强度/复杂/多方战斗"时调用。

```javascript
sessions_spawn({
  task: `${read("references/agent-battle.md")}

【本次任务】
重写第${chapterNum}章的战斗段落。

【输入材料】
- 当前润色版本中的战斗段落: ${battleParagraph}
- 前后各500字上下文: ${context}
- 角色战力信息: ${characterPower}
- 世界观力量体系: ${powerSystem}`,
  label: "battle-agent-ch" + chapterNum,
  model: readConfig("meta/config.md", "battleAgent"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

若触发并替换成功：`currentChapterArtifacts.battlePass = true`

---

### Step 6：spawn OOCGuardian → 一致性检查（强制执行）

重点章节每次都必须执行 OOC 检查。

```javascript
sessions_spawn({
  task: `${read("references/agent-ooc-guardian.md")}

【本次任务】
对第${chapterNum}章（重点章节）进行一致性检查。

【输入材料】
- 滚动摘要: ${rollingSummary}
- 上一章原文: ${prevChapter}
- 本章正文（润色版）: ${polishedText}
- 角色圣经摘要: ${characterSummary}
- 世界观摘要: ${worldSummary}
- 伏笔追踪表: ${read("references/plot-tracker.md")}`,
  label: "ooc-guardian-ch" + chapterNum,
  model: readConfig("meta/config.md", "oocGuardian"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

完成后更新：
- `currentChapterArtifacts.oocCheck = true`
- `lastOocCheckChapter = chapterNum`

---

### Step 7：Coordinator 整合

1. 读取 OOC 守护报告，识别人设冲突 / 设定矛盾 / 伏笔断裂
2. 根据角色圣经与世界观文档进行逻辑修正
3. 替换战斗Agent新段落（如有），校验上下文连贯性
4. 对照 style-anchor.md 检查叙事视角、禁用词、对话风格
5. 输出整合完稿

如有 P1 以上问题未修复，不得进入终审。

---

### Step 8：spawn FinalReviewer → 终审+微调（强制）

```javascript
sessions_spawn({
  task: `${read("references/agent-final-reviewer.md")}

【本次任务】
对第${chapterNum}章整合完稿进行终审，输出终稿。

【输入材料】
- 风格锚定: ${read("meta/style-anchor.md")}
- 本章整合完稿: ${integratedText}
- 本章细纲: ${chapterOutline}
- OOC检查报告: ${oocReport}
- 滚动摘要: ${rollingSummary}

请进行五维度终审（逻辑/情感/节奏/语言/风格），输出：终审报告 + 微调后终稿正文。`,
  label: "final-reviewer-ch" + chapterNum,
  model: readConfig("meta/config.md", "finalReviewer"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

完成后更新：`currentChapterArtifacts.finalReview = true`

---

### Step 9：更新存档 + 触发检查 + 汇报（强制闭环）

> **使用 `references/chapter-commit-template.md`：** 在执行任何写入前，先在内存中填写提交清单，然后按顺序一次性完成所有写入，避免分散遗漏。

必须完成以下全部事项：
- 更新 `meta/metadata.json`（`currentChapter`, `lastCompletedChapter`, `chapters` 条目）
- 更新 `chapters/chapter_name.md`
- 更新 `references/state-tracker.md`, `references/relationship-tracker.md`, `references/plot-tracker.md`（三项合并为一次集中写入）
- [每5章] **异步触发** RollingSummarizer（`mode: "run"`，不等待结果，仅记录"已触发"；失败时由 Coordinator 生成过渡摘要并记录待补）
- [每5章] **异步触发** ReaderSimulator（`mode: "run"`，不等待结果，仅记录"已触发"；失败时记录并延后补做）
- 向用户汇报：完成情况 / 字数 / 亮点 / 下一步建议

> **异步触发说明：** RollingSummarizer 和 ReaderSimulator 以 `mode: "run"` 独立运行，主控不阻塞等待其结果。触发后立即在 `workflow-state.json` 记录 `lastRollingSummaryChapter` / `lastReaderFeedbackChapter`，结果由子 Agent 自行写入对应文件。主控在下一章恢复协议时检查结果是否已写入，若缺失则补做。

完成后更新 `meta/workflow-state.json`：
- `currentChapterArtifacts.archiveSync = true`
- `currentChapterArtifacts.userReport = true`
- `lastClosedChapter = chapterNum`
- `resumeRequired = true`
- `chapterEntryChecklistComplete = false`
- 若已完成 Rolling Summary：`lastRollingSummaryChapter = chapterNum`
- 若已完成 Reader Feedback：`lastReaderFeedbackChapter = chapterNum`

> **重点章节未完成终审或存档闭环，不得进入下一章。**

---

## 子 Agent 调用次数

典型 5 次 / 触发 BattleAgent 时为 6 次

---

## 双轨对比

| 维度 | 常规章节 | 重点章节 |
|------|----------|----------|
| 步数 | 5步 | 9步 |
| 子 Agent 调用 | 2-3次 | 5-6次 |
| 规划 | Coordinator | FinalReviewer |
| 终审 | Coordinator | FinalReviewer |
| OOC检查 | 条件触发 / 至少自查 | 每次强制 |
| 适用场景 | 普通推进/过渡 | 高潮/转折/首末章/幕分界 |
