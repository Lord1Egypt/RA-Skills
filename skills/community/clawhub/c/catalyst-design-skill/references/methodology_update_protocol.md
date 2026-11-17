# 方法论动态更新机制（Update Protocol）

> 目的：使 catalyst-design 的方法论体系能随新增文献**主动演进**，而非静态固定。
> Purpose: let catalyst-design's methodology **evolve proactively** with new literature, rather than stay static.
> 触发时机：**仅当用户在对话中明确要求更新知识库时**（例如"更新你的方法论 / 记住这条"）才执行本闭环；默认不触发，技能保持只读。参见 SKILL.md 工作流第 4 步。
> Trigger: run this loop **only when the user explicitly opts in within the conversation** (e.g., "update your methodology"); by default it is not triggered and the skill stays read-only. See SKILL.md workflow step 4.

---

## 一、更新触发源（多来源融合）| Update triggers (multi-source fusion)

| 来源 Source | 触发方式 Trigger | 处理要点 Handling notes |
|---|---|---|
| catalyst-search 检索结果 `[CS]` | 用户提供文献矩阵，或本技能建议 catalyst-search 补检<br>User supplies matrix, or skill suggests catalyst-search re-check | 已含 DOI，可直接校验入库<br>Already has DOI; verify & commit directly |
| 用户经 AI 对话 / 其他 skill 获取的文献 `[AI]` | 用户在对话中粘贴/上传文献片段或结论<br>User pastes/uploads snippets or conclusions in chat | **须补齐 DOI/出处**后再入库；无法核实的降为 [EXP]<br>**Must add DOI/source** before commit; unverifiable → downgrade to [EXP] |
| 其他外部渠道 `[EXT]` | 会议、专利、标准、行业报告、课题组内部数据<br>Conference, patent, standard, industry report, group-internal data | 注明具体出处(专利号/标准号/会议名)，标注非同行评议<br>Name exact source (patent/no./standard/no./conf. name); mark non-peer-reviewed |

## 二、更新闭环流程（五步）| Update loop (five steps)

```
① 采集 Capture  → ② 校验 Verify  → ③ 归类 Classify  → ④ 入库 Commit  → ⑤ 复核/淘汰 Review
```

1. **采集(Capture)**：从触发源提取"设计规律/参数/方法"候选条目，记录原始出处。
   - Extract candidate "rule/parameter/method" entries from the trigger; record original source.
2. **校验(Verify)**：
   - 核实真实性：优先取有 DOI/专利号/标准号者；[AI] 来源须能溯源，否则降为 [EXP] 并标"待验证"。
     - Authenticity: prefer entries with DOI/patent no./standard no.; [AI] must be traceable, else → [EXP] "to verify".
   - 评估置信度：多来源交叉→★★★；单一可靠来源→★★；经验/单点→★。
     - Confidence: multi-source cross → ★★★; single reliable → ★★; empirical/single-point → ★.
3. **归类(Classify)**：判定归属层级 L1 理论 / L2 方法工具 / L3 参数 / L4 验证，分配编号 `层号.序号`。
   - Decide layer L1/L2/L3/L4 and assign ID `layer.seq`.
4. **入库(Commit)**：
   - 写入 `design_methodology.md` 对应层级表格（含来源标签、置信度、更新日期）。
     - Write to the matching layer table in `design_methodology.md` (source tag, confidence, update date).
   - 同步在 `methodology_registry.md` 追加一行台账（编号/摘要/来源/DOI/置信/日期/状态）。
     - Append one registry row in `methodology_registry.md` (ID/summary/source/DOI/conf/date/status).
5. **复核/淘汰(Review)**：
   - 冲突：新证据与旧条目矛盾时，保留高置信/新时效者，旧条目状态改为 `superseded` 并注明被谁取代。
     - Conflict: keep higher-confidence / newer; set old entry to `superseded` and note what replaces it.
   - 过期：历史条目每季度复核；被推翻的标 `deprecated`，不删除以保留审计痕迹。
     - Stale: review historical entries quarterly; overturned → `deprecated` (kept, not deleted, for audit trail).

## 三、条目状态机 | Entry state machine
`active`（生效）→ `superseded`（被更新证据取代）/ `deprecated`（已废弃）/ `pending`（待验证，多见于 [AI]/[EXP]）。
`active` (in effect) → `superseded` (replaced by newer evidence) / `deprecated` (obsolete) / `pending` (to verify, common for [AI]/[EXP]).
- 仅 `active` 条目参与生成设计建议；`pending` 可提示但须标"待验证"。
  - Only `active` entries feed advice; `pending` may be hinted but must be labeled "to verify".

## 四、执行约定 | Conventions
- **增量优先 | Incremental first**：默认追加新条目，不覆盖历史；确需修改则在 registry 记一次变更记录。
  - Append by default, don't overwrite history; if edit needed, log a change in the registry.
- **来源不可省 | Source mandatory**：任何入库条目必须带来源标签；无法溯源者不得标为 [CS]/[EXT]。
  - Every committed entry must carry a source tag; untraceable ones must not be labeled [CS]/[EXT].
- **周期复核 | Periodic review**：建议每季度或每积累 ≥10 条新证据时，对 L1–L4 全表做一次时效与冲突复核。
  - Suggest quarterly, or every ≥10 new evidences, a full L1–L4 recency & conflict review.
- **与检索联动 | Link with search**：当某设计方向证据不足(仅 [EXP])时，主动建议调用 catalyst-search 补检以升级为 [CS]。
  - When a direction is under-evidenced (only [EXP]), proactively suggest catalyst-search re-check to upgrade to [CS].
