# Workflow State Machine（执行状态机）

> 本文定义 12agent-novel 的硬执行门槛。Coordinator 必须把它当作状态机，而不是建议性流程。

## 一、总原则

1. 未通过入口检查，不得进入下一步。
2. 未完成章节闭环，不得进入下一章。
3. `meta/metadata.json` 与 `meta/workflow-state.json` 必须同步。
4. 任何恢复写作场景，都必须先执行 `resume-protocol.md`。
5. 用户授权边界、Iron Rules 与 style-anchor.md 属于硬约束，不得降级为“参考”。

---

## 二、Phase 状态流转

```text
initialized -> phase0_ready -> phase1_ready -> phase2_ready -> phase3_ready
```

### Phase 流转条件

- `phase0_ready`：项目目录、基础元数据、模型映射已初始化
- `phase1_ready`：世界观 / 角色 / 大纲 / 细纲 / 风格锚定已完成并定稿
- `phase2_ready`：准备进入正文写作
- `phase3_ready`：项目已存在正文，允许重写 / 补设定 / 调整大纲

> 任何时候若基础文档缺失，禁止强行提升到下一 Phase。

---

## 三、章节状态流转

```text
idle
  -> resumed
  -> entry_checked
  -> planned
  -> drafted
  -> polished
  -> battle_adjusted(optional)
  -> ooc_checked
  -> final_reviewed(optional for key chapters, optional for normal chapters only when upgraded)
  -> archive_synced
  -> reported
  -> closed
```

### 不可跳过的最小闭环

#### 常规章节（normal）
- resumed
- entry_checked
- planned
- drafted
- polished
- ooc_checked（若未触发 OOCGuardian，则必须有 Coordinator 轻量自查记录）
- archive_synced
- reported
- closed

#### 重点章节（key）
- resumed
- entry_checked
- planned
- drafted
- polished
- ooc_checked
- final_reviewed
- archive_synced
- reported
- closed

> 任一必需节点未完成，`lastClosedChapter` 不得前移。

---

## 四、currentChapterArtifacts 字段约定

`meta/workflow-state.json` 中 `currentChapterArtifacts` 含义：

- `plan`: 本章规划已完成
- `draft`: 初稿已完成
- `polish`: 润色稿已完成
- `battlePass`: 战斗专项替换已完成（无战斗时可保持 false）
- `oocCheck`: OOC 检查 / 自查已完成
- `finalReview`: FinalReviewer 终审已完成（重点章节必须为 true）
- `archiveSync`: metadata / chapter_name / trackers / rolling summary triggers 已完成同步
- `userReport`: 已向用户汇报本章结果

---

## 五、强制拦截条件

出现以下任一情况，Coordinator 必须停止进入下一章：

1. `resumeRequired = true`
2. `chapterEntryChecklistComplete = false`
3. `archiveSync = false`
4. 达到 Rolling Summary 触发阈值但未执行
5. 达到 Reader Feedback 触发阈值但未执行
6. `meta/metadata.json` 与 `meta/workflow-state.json` 章号不一致
7. Iron Rules 检出 P0 / P1 未修复问题

---

## 六、允许降级 vs 不允许降级

### 允许降级
- ReaderSimulator 失败时可记录失败并延后重试
- RollingSummarizer 失败时可暂时由 Coordinator 生成过渡摘要，但必须记录并在后续补齐正式摘要
- BattleAgent 在不满足触发条件时可不调用

### 不允许降级
- 恢复协议
- 写前核查
- style-anchor.md 全文喂入 MainWriter
- OOC 检查（重点章节强制；常规章节至少自查）
- metadata / tracker / chapter_name / 章节状态同步

---

## 七、文件写入失败处理

当 Coordinator 执行落盘操作（写入 `metadata.json`、`workflow-state.json`、`chapters/`、tracker 等）时，若遇到写入失败：

> **前提约束（写入顺序的基础规则）：** 章节正文文件（`chapters/ch{NNN}.md`）写入成功，是后续所有状态文件（`workflow-state.json`、`metadata.json`、tracker 等）更新的前提。若正文写入失败，所有状态文件均不得更新，避免状态超前于实际内容。

1. **立即停止**：不得继续推进到下一章
2. **重试一次**：对同一文件重试写入操作
3. **重试仍失败**：
   - 标记 `resumeRequired = true`
   - 将失败详情记录到 `archive/archive.md`（包含章节号、失败文件名、时间）
   - 向用户报告具体失败项
   - 停止自动推进
4. **禁止跳过**：不得以"下次补写"方式跳过任何必须落盘的文件

> 写入失败是硬阻断条件，与 OOC P1 未修复同级。

---

## 八、建议的 Coordinator 执行口令

每次进入 Phase 2 前，先自问：

> 我现在是在执行一个有 gate 的状态机，还是在凭印象续写？

若答案不是前者，立即停下并执行恢复协议。
