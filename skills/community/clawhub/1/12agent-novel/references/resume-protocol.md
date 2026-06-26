# Resume Protocol（强制恢复协议）

> 任何“继续写作”“写第X章”“批量写作”“自动推进恢复”场景，Coordinator 都必须先执行本协议。

## 目标

防止 Coordinator 凭会话印象直接续写，必须先基于项目状态完成恢复校验。

---

## 必读文件（按顺序）

1. `references/iron-rules.md`
2. `meta/metadata.json`
3. `meta/workflow-state.json`
4. `meta/config.md`
5. `meta/style-anchor.md`
6. `outline/chapter-outline.md`
7. `references/rolling-summary.md`
8. `references/state-tracker.md`
9. `references/relationship-tracker.md`
10. `references/plot-tracker.md`
11. 最近已完成章节原文（默认最近 1-3 章）

> 若任一关键文件缺失或状态互相矛盾，禁止直接开写；先补档、修正或向用户报告异常。

---

## 恢复检查清单（必须逐项回答）

### A. Phase 状态
- 当前项目处于 Phase 0 / 1 / 2 / 3 的哪一阶段？
- `meta/metadata.json` 与 `meta/workflow-state.json` 的 phase 是否一致？
- 若不一致：先修正状态，再继续。

### B. 当前章节状态
- 当前准备写哪一章？
- `writingProgress.currentChapter`、`lastCompletedChapter`、`lastClosedChapter` 是否一致？
- 是否存在“正文已写完，但 archive / tracker / chapter_name 未同步”的未闭环章节？
- 若存在：先完成该章闭环，不得跳到下一章。

### C. 守护与摘要状态
- 最近一次 OOC 检查停在第几章？
- 最近一次 Rolling Summary 覆盖到第几章？（检查 `references/rolling-summary.md` 是否已有对应批次内容，而非仅看 `lastRollingSummaryChapter` 字段——异步触发后字段已记录，但文件可能尚未写入）
- 最近一次 Reader Feedback 覆盖到第几章？（同上，检查 `archive/reader-feedback/` 目录是否有对应文件）
- 是否已达到应触发而未触发的阈值（5章 / 4章）？
- 若文件缺失但字段已记录：说明异步子 Agent 未完成，需补做后再继续。
- `milestoneAudit.nextAuditChapter` 是否已达到但未执行？（检查 `lastClosedChapter >= nextAuditChapter` 且 `lastMilestoneAuditChapter < nextAuditChapter`）
- 若里程碑审计未执行：先执行审计，再继续写作。

### D. 上下文充分性
- 最近 3 章原文是否可用？
- 本章相关伏笔 / 关系 / 主角状态是否可从追踪表定位？
- style-anchor.md 是否已是 v1.0 正式版？
- 若任一项缺失：先补足上下文。

### E. Phase 3 维护遗留项
- `meta/workflow-state.json` 中 `phase3Maintenance.pendingRewrites` 是否有未处理的章节？
- 若有：向用户展示待处理重写列表，询问是否先处理再继续写作，或确认跳过。
- `phase3Maintenance.cascadeAffectedChapters` 是否有未完成一致性检查的章节？
- 若有：提示用户，由用户决定是否先处理。

---

## 恢复后的动作

恢复检查完成后，Coordinator 必须：

1. 更新 `meta/workflow-state.json`：
   - `resumeRequired = false`
   - `currentChapter = 待写章节号`
   - `chapterEntryChecklistComplete = false`
   - 重置 `currentChapterArtifacts`
2. 明确本章轨道：`normal` / `key`
3. 进入对应的 Phase 2 工作流

---

## 禁止事项

- 禁止只凭聊天历史直接续写
- 禁止绕过 `meta/workflow-state.json` 进入正文阶段
- 禁止在上一章未闭环时直接进入下一章
- 禁止跳过“应触发但未触发”的 OOC / 滚动摘要 / 读者反馈

---

## 恢复失败处理

若恢复校验失败，Coordinator 仅允许以下动作之一：

1. 补档并修正状态
2. 向用户报告具体缺失项
3. 停止自动推进并标记 `resumeRequired = true`
