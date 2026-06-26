# Phase 2 常规章节工作流（硬闭环版，典型 2-3 次子 Agent 调用）

> 下文出现的 `read()`、`readConfig()`、`sessions_spawn()` 等代码块均为**示意性伪代码**，用于说明调度逻辑与输入拼装方式，不代表宿主环境必须提供同名 API。

## 轨道判定

常规章节 = 不满足以下任何条件的章节：
- 用户手动指定"重点章"
- 细纲标注高潮/转折/情感爆发
- 首章(Ch1) / 末章(ChN)
- 幕间分界章（从 meta/config.md 的 key_chapters 读取）

---

## 先决条件（强制）

进入本流程前，Coordinator 必须先：

1. 读取 `references/workflow-state-machine.md`
2. 读取 `references/resume-protocol.md` 并完成恢复校验
3. 确认 `meta/metadata.json.project.phase = 2`
4. 确认 `meta/workflow-state.json.phaseState.currentPhase = 2`
5. 确认不存在未闭环章节

若任一项不满足：禁止直接开写。

---

## 工作流

### Step 0：恢复与轨道锁定（强制）

Coordinator 必须更新 `meta/workflow-state.json`：
- `chapterWorkflow.currentChapter = chapterNum`
- `chapterWorkflow.currentTrack = "normal"`
- `chapterWorkflow.chapterEntryChecklistComplete = false`
- 重置 `currentChapterArtifacts`
- `resumeRequired = false`

---

### Step 1：Coordinator 读取存档 + 写前核查（强制）

读取：固定层（世界观摘要+角色摘要+大纲）+ 滚动摘要 + 本章相关伏笔/关系 + 最近 1-3 章原文。

> **Session Cache 优化：** 固定层（world.md 摘要 / 角色圣经摘要 / outline.md）在同一会话内只需读取一次，后续章节直接复用，无需重复读取文件。会话重启或发生世界观/角色/大纲变更时刷新。详见 `references/session-cache.md`。

> **强制写前核查清单（Coordinator 必须先回答再规划）：**
> - [ ] 上章结尾场景/情绪/悬念 → 本章开头如何承接？
> - [ ] 主角当前状态（位置/修为/持有物）？
> - [ ] 本章需要推进的伏笔ID？需要回收的伏笔ID？
> - [ ] 本章涉及的角色关系有无需要推进的？
> - [ ] 本章在全书节奏中的定位（铺垫/上升/高潮/过渡）？
> - [ ] 本章字数目标？（从meta/project.md读取，默认4000字）

→ 如任一项无法回答：先查阅追踪表补全
→ 全部确认后：输出本章规划（关键事件/节奏/钩子/字数目标）

完成后更新：
- `chapterEntryChecklistComplete = true`
- `currentChapterArtifacts.plan = true`

---

### Step 2：spawn MainWriter 初稿+润色（单次调用）

```javascript
sessions_spawn({
  task: `${read("references/agent-main-writer.md")}

【本次任务】
完成第${chapterNum}章的初稿+润色，一次性输出可交付版本。

【输入材料】
- 风格锚定: ${read("meta/style-anchor.md")}
- 本章细纲: ${chapterOutline}
- 本章规划: ${chapterPlan}
- 世界观摘要: ${worldSummary}
- 角色圣经摘要: ${characterSummary}
- 滚动摘要: ${rollingSummary}
- 最近3章原文: ${recentChapters}
- 本章相关伏笔/关系: ${onDemandContext}
- 字数目标: ${wordTarget}字（允许${minWords}-${maxWords}字）

${isSensitive ? sensitivityConstraint : ""}

请先生成完整初稿，然后直接进行语言流畅度、氛围浓度、感官细节、节奏感的全面润色，最终输出经过完整润色的可直接交付的章节正文。`,
  label: "main-writer-ch" + chapterNum,
  model: readConfig("meta/config.md", "mainWriter"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

**必须附带 `meta/style-anchor.md` 全文。** 高敏感内容必须附加敏感度 Prompt 约束。

完成后更新：
- `currentChapterArtifacts.draft = true`
- `currentChapterArtifacts.polish = true`

---

### Step 3：一致性检查（不可跳过）

检查触发条件（任一满足即调用 OOCGuardian）：
1. 本章细纲标注：高潮/转折/情感爆发/关键节点
2. 上章有读者反馈或 Coordinator 感知到潜在 OOC / 逻辑风险
3. 本章涉及新增重要角色/势力/设定/伏笔
4. 距上次 OOCGuardian 检查已 **≥4章**（即 `currentChapter - lastOocCheckChapter ≥ 4`）
5. 本章字数 ≥ 4800 字

**触发时** → spawn OOCGuardian：

```javascript
sessions_spawn({
  task: `${read("references/agent-ooc-guardian.md")}

【本次任务】
对第${chapterNum}章进行一致性检查。

【输入材料】
- 滚动摘要: ${rollingSummary}
- 上一章原文: ${prevChapter}
- 本章正文: ${currentChapter}
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

**未触发时** → Coordinator 轻量自查（对照角色圣经摘要 + 滚动摘要 + 本章细纲，输出 100-200 字自查结论，并写入 archive/archive.md 或章节整合记录）

完成后更新：
- `currentChapterArtifacts.oocCheck = true`
- 若调用了 OOCGuardian：`lastOocCheckChapter = chapterNum`

---

### Step 4：Coordinator 整合修正 → 输出终稿

**无 OOC 调用时：** 基于 Step 2 输出 + 自查结论微调后定稿

**有 OOC 调用时：** 依据 OOC 报告逐项修正；P1 以上问题未修复前，不得归档 closed

输出：标题 / 字数 / 正文 / 版本标记
写入：`chapters/ch{NNN}.md`

---

### Step 5：更新存档 + 触发检查 + 向用户汇报（强制闭环）

> **使用 `references/chapter-commit-template.md`：** 在执行任何写入前，先在内存中填写提交清单，然后按顺序一次性完成所有写入，避免分散遗漏。

必须完成以下全部事项：

- 更新 `meta/metadata.json`（`currentChapter`, `lastCompletedChapter`, `chapters` 条目）
- 更新 `chapters/chapter_name.md`（追加本章编号↔中文名称映射，格式：`| ch{NNN} | 《章节名称》 | {字数} | {日期} |`）
- 更新 `references/state-tracker.md`, `references/relationship-tracker.md`, `references/plot-tracker.md`（三项合并为一次集中写入）
- [每5章] **异步触发** RollingSummarizer（`mode: "run"`，不等待结果，仅记录"已触发"；失败时由 Coordinator 写过渡摘要并标记待补）
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

> **未完成上述任一项，不得进入下一章。**

---

## 典型路径

```text
恢复校验 → 写前核查 → MainWriter(1次) → [OOCGuardian抽样] → Coordinator整合 → 存档闭环 → 用户汇报
```

子 Agent 调用次数：典型 2 次（MainWriter + 条件触发 OOCGuardian 时为 3 次）
