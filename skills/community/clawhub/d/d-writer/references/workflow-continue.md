# 模式 B：续写已有书

## 触发时机

书已存在，往下写。

## 步骤

1. **定位当前书**：若有多本且未指定，列出候选并询问。
2. **确定下一章章号**：从连续章节文件和 `chapters/index.json` 确定最新落硬盘章节——不要只信一份陈旧的状态文件。
3. **读受保护上下文**：
   - `author_intent.md`（含不可妥协项）
   - `current_focus.md`
   - `story_frame.md` / `story_bible.md`
   - `volume_map.md` / `outline.md`
   - `book_rules.md`
   - `current_state.md`（事实表 + 道具账本 + 空间锚点）
   - 相关角色档案
   - `pending_hooks.md`（活跃钩子）
4. **读可压缩上下文**：
   - 最近几章摘要
   - 最近 1–3 章结尾（**用于场景续接判断与开头 / 收尾类型轮换**，不是用来在下一章复述的信息）
   - `audit-drift.md`
5. **创建 `runtime/chapter-NNNN.intent.md`**（每章都创建）：
   - chapter goal
   - outline node
   - current task
   - reader expectation
   - hooks to advance / resolve / keep buried
   - must keep / must avoid
   - **章首 / 章末**：开头类型 + 收尾断章类型（对照 `references/chapter-craft.md` 类型库，均须与近 3 章轮换）
   - required end-of-chapter change（章末"画面上出现什么"，不是"总结出什么"）
6. **起草**：从选定的上下文起草，而不是把整个项目都堆进来。开写前读 `references/chapter-craft.md`：
   - **章首三行入戏**：前三行落在正在发生的事上，禁止回顾式承接；回顾前情 ≤2 句且必须夹带新信息。
   - **章末断章**：按断章技法库在能量上升沿切，禁止总结本章 / 金句升华 / 宣布计划 / 情绪命名；钩子推进等元数据只进 `chapter_summaries.md`，绝不写进正文。
   - **类型轮换**：开头类型与收尾类型均不得与近 3 章相同。
7. **双层质量门禁（子代理审查）**：

   审计**不得**由起草同一上下文自评——这会导致文风维度（维 10/20/21/22/23）自评失效、审-改循环收敛到局部最优。审计必须在独立子代理中以**新鲜读者视角**运行。

   ### 7.1 主代理准备审计包

   起草完成后，主代理按体裁裁剪出激活维度清单，并准备审计包：

   ```
   ## 章节草稿
   {chapter draft 全文}

   ## 激活的审计维度（体裁裁剪后）
   {active dimension IDs + 完整的判定规则文本，从 references/audit-dimensions.md 复制}

   ## 连续性事实（仅用于审计，非写作指引）
   - 主角：<名字、身份、当前状态>
   - 当前地点/时间：<...>
   - 已知事实：<仅与本章情节直接相关的，从 current_state.md 事实表裁剪>
   - 道具状态：<仅本章可能出现的道具，从 current_state.md 道具账本裁剪，含 origin 与最近两章变化事件>
   - 空间锚点：<仅本章场景，从 current_state.md 空间锚点裁剪>
   - canon 数字锚点：<本章出场角色的「canon 数字锚点」表裁剪（仅 anchor_id + 事项 + 值），从角色卡「canon 数字锚点 Number Anchors」区块提取>
   - 活跃钩子：<仅本章相关的 hook_id + 一句话，从 pending_hooks.md 裁剪>
   - 近 3 章开头/收尾/过渡摘要：<从 chapter_summaries.md 与近 3 章正文提取，附 chapter-craft.md 类型标注，供维 42/43 比对>
   ```

   **关键原则**：连续性事实是**从 current_state.md 中裁剪的纯事实**，不含"作者想让读者感受到什么"、不含大纲、不含角色档案、不含完整 current_state。canon 数字锚点与此不冲突：**排除的是角色档案中的写作指引（欲望 / 弧线 / 技法），数字锚点是可判定事实，必须给到审计子代理**——否则"卡说 21 岁、正文写 20 岁"这类冲突永远无法被冷读发现。

   ### 7.2 启动子代理审计

   用 Agent 工具启动子代理（`subagent_type: "general-purpose"`），提示词核心：

   > 你是一名"新鲜读者"审计员。你正在审读一本中文网络小说的一个章节。**你没有读过大纲、作者意图或任何前文章节** —— 请以第一次阅读的读者身份来读这篇草稿。
   >
   > 先通读全文，标记阅读体验断裂处；再按以下激活维度逐维审计。每维给出 pass/fail/unknown + 具体证据（引用原文）+ 修改建议。
   >
   > 特别注意文风问题：重复句式、AI 标志语、段落节奏单调、转折可预测、套话密度、跨章重复。

   子代理**不持有**：大纲 / 作者意图 / 角色档案 / 完整 current_state / 前文章节正文（仅持有审计包中的最小事实 + 近 3 章摘要）。

   ### 7.3 子代理返回结构化报告

   子代理按以下格式返回：

   ```markdown
   # 审计报告

   ## 第一层：驻场初筛（10 点）
   - [PASS/FAIL] 维度名：证据 "..." → 建议 "..."

   ## 第二层：深化审计（激活维度）
   - [FAIL] 维10 词汇疲劳：...
   - [PASS] 维22 公式化转折：...

   ## 文风专项
   - 重复句式：第3/7/14段均以"他……"开头
   - AI标志语："不禁"出现4次（第2/5/9/12段）
   - 节奏：第4-8段均为长段（>120字），建议拆短

   ## 总结
   N 项需修改，M 项建议优化
   ```

   ### 7.4 主代理修改

   主代理根据审计报告修改草稿。主代理持有完整上下文（大纲/意图/角色/状态），能正确实施修改。**不要**逐条"最小修补"——如果报告指出结构性问题（如连续 5 段同节奏、开头方式与近 3 章重复），应做结构性重写。

   ### 7.5 可选二审

   修改后，可再次启动子代理二审（同一审计包格式，附修改后的草稿 + 原报告）。若二审仍有 ≥2 个 blocking 项，主代理再次修改。**二审为上限**，避免无限循环。

   ### 7.6 审计发现留痕

   未当场修复的审计发现，必须落记录（`audit-drift.md`）。

8. **事务式落盘**（详见 `references/file-contract.md` 的"章节落盘事务流程"）：
   - 按序写入：`chapters/NNNN_<title>.md` → `chapters/index.json` → `chapter_summaries.md` 行（含**章节 delta**）→ `current_state.md`（事实表 + 关系 + 道具账本 + 空间锚点）→ `pending_hooks.md` → `book.json`（status / updatedAt 同步）→ intent 的「实际偏离 Deviation Log」（若产出偏离 intent 的 goal / 必须场景 / 章末画面）
   - **字数禁手写**：`chapters/index.json` 的 wordCount 必须由 `python scripts/rebuild_index.py <book-dir>` 生成，禁止手写数值
   - 道具账本**三核对**：数量、状态、存放位置——三项逐一对着本章正文末态核对，不允许只改数量
   - **新增固定物件 / 布局变化 → 空间锚点登记**（新列或新锚点行，遵循 valid_until 失效规则）
   - **hook 收敛复查**：对本章 summary 的 events 逐项自问 advance / resolve / defer；notes 出现"揭露 / 兑现 / 真相"字样的 hook 必须重新评估 lifecycle_status（揭尽 → resolved 或收窄为新子 hook）；正文推进了某 hook 内容的，`last_advanced_chapter` / `chapters_since_advance` 同步
   - 全部写入后运行一致性验证：`python scripts/validate_book.py <book-dir>`（FAIL 则修复后再落盘）
   - 完成后创建章末快照 `snapshots/<NNNN>/`（含 `manifest.json`）
   - **不要重写仪表盘**——它运行时自会读取最新文件
9. **合并审核询问（仅在任务终点一次）**：若是本轮写作任务的**最后一章**（单章，或连续创作的终点），主代理询问用户"是否进入合并审核？"——**连续创作时中途各章完成不打断、不询问**。进入后范围由用户决定（全部 / 部分 / 指定区间），执行见 `references/workflow-combined-audit.md`。

## 相关文档

- 文件职责与权威顺序：`references/file-contract.md`
- 章节落盘事务流程：`references/file-contract.md`
- 章节 delta 模板：`references/templates.md`
- 章首 / 章末技法（起草前必读）：`references/chapter-craft.md`
- 双层质量门禁与子代理审查机制：`references/audit-dimensions.md`
