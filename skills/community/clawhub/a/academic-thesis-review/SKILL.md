---
name: academic-thesis-review
description: Multi-round review skill for Chinese management-oriented master's theses, especially MBA, MEM, and MPA, with applicability to similar professional and applied research theses.
license: MIT
metadata:
  author: wmpluto
  version: "1.1.0"
  repository: https://github.com/wmpluto/academic-thesis-review-skill
  github_profile: https://github.com/wmpluto
  compatibility:
    - OpenCode
    - OpenClaw
    - Claude Code
---

# Skill: Academic Thesis Review (Chinese Master's Thesis)

## Description
Multi-round academic review of Chinese Master's theses (硕士学位论文). Uses a 3-round review strategy (macro → per-chapter → inter-chapter consistency). Acts as a strict professor reviewer, producing actionable revision comments in Chinese. Supports iterative version cycles.

## Trigger Phrases
- "审阅论文" / "review thesis"
- "论文评审" / "学术评审"
- "帮我看看论文" / "论文有什么问题"
- "再做一轮审阅" / "修改后再看看"

## Prerequisites
- Thesis file in `.docx` format
- Python available for text extraction (zipfile + xml.etree.ElementTree)
- If `review_results.md` exists in the working directory, iterative mode is triggered automatically (see Phase 1 § Prior Review Detection)

---

# Part I: Rules & Instructions

## Core Rules

### Execution Order

```
Round 1 ─┐                             ┐
         ├─ (parallel or sequential) ───├→ Round 3 → Consolidate → User revises
Round 2 ─┘                             ┘
```

- **Round 1** and **Round 2** have **no hard dependency** on each other. The agent may run them in parallel or sequentially depending on its own capabilities and context constraints.
  - **Round 1:** reviews the full thesis text. Output: macro structure review + chapter dependency map.
  - **Round 2:** reviews chapters **sequentially in document order**. Each chapter review has access to the summary cards of all previously reviewed chapters. Output: per-chapter issues + per-chapter summary cards.
- **Round 3** depends on **both** Round 1 and Round 2 completing. It reconciles their outputs, then reviews chapter pairs. Output: inter-chapter consistency issues + pair coverage log.
- All 3 rounds review the **same original text** — the user revises only after all rounds complete.

### Default Thesis Assumption

Standard master's thesis structure: abstract → introduction → literature/theory → methodology → analysis/results → conclusion → references → appendices. No restriction on research topic, industry, or case type.

**Non-standard fallback:** If the thesis uses non-standard chapter names or merged chapters, map chapters by function: research problem → literature support → method design → results delivery → conclusion.

### Conflict Resolution (authoritative — all rounds defer to this)

1. **Evidence first, then severity.** If R2/R3 evidence overturns an R1 finding, the severity follows the new evidence — do not preserve R1's higher severity for a claim R2/R3 disproved.
2. If Round 2 and Round 3 disagree on the same finding, prefer the conclusion backed by **more direct full-text evidence**.
3. If multiple rounds independently confirm the same issue but at different severities, keep the **higher severity**.

### Verification Types

All review checklists use these labels. Defined once here; referenced throughout.

- **[D]** = directly verifiable from thesis text
- **[S]** = suspicion only — flag for closer look, agent cannot confirm
- **[M]** = requires manual verification outside thesis text (original Word file, source literature, or external facts)

### Severity Rubric

- 🔴 **Immediate fix** — threatens credibility, conclusion validity, or defense safety (data contradictions, unanswered research questions, method-result mismatch, clear factual errors, substantive cross-chapter conflicts)
- 🟡 **Strongly recommended** — weakens academic quality but not immediately fatal (underdeveloped argument, weak literature-method link, unstable terminology, loose structure)
- 🟢 **Quality improvement** — wording, polish, or refinement that does not affect conclusions

---

## Phase 1: Text Extraction

Extract plain text from `.docx` via Python:

```python
import zipfile, xml.etree.ElementTree as ET

docx_path = r'<PATH_TO_DOCX>'
z = zipfile.ZipFile(docx_path)
doc_xml = z.read('word/document.xml')
tree = ET.fromstring(doc_xml)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
paragraphs = tree.findall('.//w:p', ns)
full_text = []
for p in paragraphs:
    runs = p.findall('.//w:r/w:t', ns)
    line = ''.join(r.text for r in runs if r.text)
    if line.strip():
        full_text.append(line)
result = '\n'.join(full_text)
```

Output to `review_artifacts/thesis_full_text_<YYYYMMDD_HHMMSS>.txt`. Create directory if it does not exist. Note paragraph count and character count as baseline metrics.

### Preparation

After extraction, prepare:
- **Full text file** — for Round 1
- **Per-chapter split files** — for Round 2
- **Thesis summary block** — title + full Chinese abstract + full English abstract + table of contents (~500-1000 chars), used as context prefix in Rounds 2 and 3

### Chapter Splitting Rules

- Split by **top-level chapter headings** (e.g., `第1章`, `第一章`, `1 绪论`)
- Sub-headings (level 2/3) belong to their parent chapter
- **Long chapter**: read in subsection chunks during Round 2, but output one consolidated result and one summary card per top-level chapter
- **Short chapter**: flag as structure weakness in Round 2; do not auto-merge unless user confirms
- **Ambiguous boundaries**: ask user to confirm rather than guessing

### Prior Review Detection (Iterative Mode)

After extraction, check whether `review_results.md` exists in the current working directory.

**Not found → First-version mode:**
- Version = 第1版
- No prior issues to load
- Proceed normally

**Found → Iterative mode:**
1. Parse the prior `review_results.md` to extract:
   - Prior version number → increment by 1 for the new review
   - All prior issues from "本版问题清单" with their severity, location, and description
2. Classify each prior issue by its "位置" field:
   - Issues with location "全局" → redistribute to relevant chapters in Round 2
   - Issues with location "第X章" → **Round 2** (injected in Phase B when reviewing that chapter)
   - Issues with location "第X章→第Y章" → **Round 3** (injected when reviewing that pair)
3. Verification marking (applied in Phase B of Round 2 and in Round 3):
   - Issue is resolved → mark ✅已修改
   - Issue is partially addressed → mark ⚠️部分修改, describe what remains
   - Issue is unchanged → mark ❌未修改

### Iterative Mode: Issue Injection Strategy

**Key Principle: Separation of Discovery and Verification**

To prevent anchoring bias (agent treating prior issues as a checklist instead of performing independent review), the injection strategy is designed as follows:

**Round 1: No injection**
- Execute exactly as first-version mode (completely independent)
- Do NOT inject any prior issues, including "全局" issues
- Rationale: Issues found in Round 1 are typically also discoverable in Round 2/3; verifying global issues through specific chapters is more precise

**Round 2: Two-phase per-chapter review**
- **Phase A (Independent Discovery):** Review chapter with NO historical issues visible
- **Phase B (Historical Verification):** Inject chapter-specific issues + relevant "全局" issues for verification
- See §2.x for detailed Phase A/B execution rules

**Round 3: Cross-chapter verification**
- Inject cross-chapter historical issues (位置="第X章→第Y章")
- Execute spot checks on chapters that declared "无新发现" in Phase A

**Anti-Shortcut Rules:**
- ✅ **DO:** Complete Phase A output before seeing any historical issues. Use dimension coverage checklist to confirm systematic review.
- ❌ **DON'T:** Combine Phase A and Phase B. Skip the dimension coverage checklist. Claim "no new issues" without checklist evidence.

### Extraction Limitations

- Figures/images lost — only captions and in-text references survive
- Table structure flattened to rows of text
- Formulas may be fragmented or missing
- Cross-references (图X.X, 表X.X) survive as text but actual targets cannot be verified
- Headers/footers and page numbers not extracted

---

## Phase 2: Three-Round Review

### Round 1: Macro Structure Review

**Input:** Full thesis text. *(In iterative mode: NO prior issues injected — execute as first-version mode)*
**Focus:** Bird's-eye structural and logical assessment. Do NOT give line-level edits.
**Long-input fallback:** If the full thesis exceeds stable single-pass context, read in large sequential chunks with overlap, then do one pass over all Round 1 findings to ensure cross-chunk consistency before outputting the dependency map.

#### 1.1 Reading Order
1. Title page & metadata
2. Table of contents
3. Chinese abstract + keywords
4. English abstract + keywords
5. All chapters — read sequentially for structural flow
6. References
7. Appendices

#### 1.2 Review Checklist

| Item | What to Check | Type |
|------|--------------|------|
| **Overall structure** | Chapter layout logical? Chapters proportional? | [D] |
| **Research question → Conclusion chain** | All research questions answered in conclusion? Any silently dropped? | [D] |
| **Logic flow** | Each chapter leads naturally to the next? Logical jumps or missing bridges? | [D] |
| **Terminology consistency (global)** | Key terms used consistently throughout? | [D] |
| **Theory utilization** | How many theories introduced vs. actually used? Flag bloat. | [D] |
| **Completeness** | All promised analyses delivered? Limitations discussed? Future work? | [D] |
| **Factual self-consistency** | Dates, statistics contradict each other *within* the thesis? | [D] |
| **Factual accuracy (external)** | Do named facts match known reality? | [M] — flag suspicious values only |
| **Section proportionality** | Chapters too short for their function, or too long and overloaded? | [D] |
| **Innovation & contribution** | Are innovation points explicitly stated? Are they supported by the thesis body? **Calibration: master's theses (especially part-time/professional) are NOT expected to produce high-level innovation. Applying existing methods to a new context or combining known approaches in a novel way IS acceptable — the key requirement is that innovation points exist, are clearly articulated, and are not fabricated.** Flag missing or unsubstantiated claims, not low novelty. | [D] for whether stated; [S] for whether substantiated |
| **Practice relevance** *(if practice-oriented)* | Is the research grounded in a real-world problem or case? Does the thesis produce actionable recommendations, not just theoretical conclusions? Does it demonstrate problem-solving ability? | [D] |
| **Abstract consistency** | Chinese and English abstracts match each other and faithfully represent the thesis? | [D] |
| **References (overview)** | Format consistency, recency, relevance | [D] |

#### 1.3 Required Output: Chapter Dependency Map

Output a chapter dependency map at the end of Round 1. This drives Round 3 pair selection.

Format:
```
章节逻辑依赖关系：
- 🔴 第1章 → 第5章：[依赖关系说明]
- 🔴 第3章 → 第4章：[依赖关系说明]
- 🟡 第2章 → 第3章：[依赖关系说明]
- ...
```

- `A → B` = A makes a promise / sets scope; B should deliver or remain consistent
- 🔴 = must check in Round 3 · 🟡 = check if evidence supports it · 🟢 = advisory, low priority
- Principle: **谁承诺，谁兑现，这两章就要配对。** See Appendix A for common patterns.

---

### Round 2: Per-Chapter Deep Review

**Input per chapter:** Thesis summary block + current chapter full text + summary cards of all previously reviewed chapters.
**Execution:** Sequential, in document order. *(In iterative mode: two-phase execution per chapter — see §2.x)*
**Focus:** Detailed intra-chapter quality. Line-level issues are caught here.

**First chapter note:** When reviewing the first chapter, no prior summary cards exist. Skip the "交付" field in that chapter's summary card.

#### 2.1 Review Dimensions

| Dimension | What to Check | Type |
|-----------|--------------|------|
| **Data Consistency** | Numbers in tables match text? **Actively recalculate** totals, percentages, and derived values from raw data — do not just check whether they "look right." If raw numbers are available, verify that reported percentages/scores are arithmetically correct. | [D] |
| **Internal Logic** | Argument flows logically? Claims supported? Logical leaps? | [D] |
| **Methodology Rigor** | Method selection rationale stated and internally consistent? | [D]/[S] |
| **Quantitative checks** *(if applicable)* | Statistical test choices, sample size, validity/reliability — apply only for quantitative empirical work | [S]; definitive judgment [M] |
| **Literature Review** | Research gap articulated? Key competing works cited? Gap justifies this study? | [D] for presence; [M] for citation accuracy |
| **Citation adequacy** | Major claims backed by citations? Unsupported assertions? | [S]; whether source supports claim is [M] |
| **Language & Style** | Typos, repeated chars (的的/了了), grammar errors (病句), punctuation misuse (中英文标点混用), inconsistent terminology, colloquial language in academic text, overly long/convoluted sentences | [D] |
| **Factual accuracy (internal)** | Dates/numbers consistent *within this chapter*? | [D] |
| **Factual accuracy (external)** | Real-world claims plausible? | [S]/[M] — flag only |
| **Chapter Framing** | Opening bridges from previous chapter? Closing sets up next? | [D] |
| **Chapter Proportion & Function** | Too short for its function? Too long and overloaded? | [D] |

**Proactive expansion rule:** When the thesis uses a specific research method (survey, AHP, regression, case study, grounded theory, etc.), the agent must proactively apply that method's academic validation criteria — not just check the generic dimensions above. The agent's own domain knowledge is the source for method-specific checks; the skill does not enumerate them.

See Appendix B for chapter-type-specific focus areas.

#### 2.2 Special Section Responsibilities

- **Abstracts** — Round 2: wording quality, terminology stability, grammar; whether abstract claims overstate the body
- **References** — Round 2: flag uncited claims or mismatched citations **[S]**; whether cited source supports the claim is **[M]**
- **Appendices** — Treat as a distinct Round 2 unit: questionnaires, interview guides, supplementary tables, coding schemes

#### 2.x Iterative Mode: Two-Phase Per-Chapter Review

**Applies only when `review_results.md` exists (iterative mode).**

In iterative mode, each chapter review is split into two sequential phases to prevent anchoring bias:

**Phase A: Independent Discovery (NO historical issues visible)**

Input: Thesis summary block + current chapter full text + prior chapter summary cards

Output format (to `review_working.md`):
```markdown
### 第X章 [章节名] - Phase A 独立发现

**审阅维度覆盖：**
- [x] 数据一致性：[具体检查内容，如"核算了表4.2共5处百分比，均正确"]
- [x] 内部逻辑：[具体检查内容，如"检查了论证链A→B→C，逻辑成立"]
- [x] 方法严谨性：[具体检查内容] 或 [N/A - 本章无方法论内容]
- [x] 文献引用：[具体检查内容] 或 [N/A]
- [x] 语言规范：[具体检查内容，如"未发现病句或标点问题"]
- [x] 章节衔接：[具体检查内容，如"开篇承接第2章结论，结尾为第4章铺垫"]

**独立发现问题：**
| 编号 | 严重度 | 问题 | 位置 | 类型 |
|------|--------|------|------|------|
| D-1  | 🟡     | ...  | L123 | [D]  |

*若未发现新问题：*
> 经独立审阅上述维度，本章未发现新问题。
```

**Phase B: Historical Issue Verification (inject after Phase A completes)**

Input: Phase A output + historical issues for this chapter (including relevant "全局" issues)

Output format (to `review_working.md`):
```markdown
### 第X章 - Phase B 历史问题验证

**注入问题：** [#1] [#7] [#19-A]

| 编号 | 原问题概述 | 验证结果 | 说明 |
|------|-----------|----------|------|
| [#1] | Wilcoxon Z/p矛盾 | ❌未修改 | L1965仍为Z=-5.059, p=0.593 |
| [#7] | 研究问题未编号化 | ❌未修改 | L162-168仍为叙述式 |

**章节摘要卡（定稿）：**
[标准摘要卡格式]
```

**Sequencing Rule:** Phase A MUST be complete and output to working file BEFORE Phase B input is provided. The agent may NOT "peek ahead" at historical issues during Phase A.

**Dimension Coverage Checklist Requirement:** The checklist in Phase A must include **specific descriptions** of what was checked (not just checkmarks). This serves as verifiable evidence that independent review was performed.

#### 2.3 Required Output: Per-Chapter Summary Card

Output after each chapter. Used by Round 3 for orientation and dependency map validation.

```
## [章节编号] [章节标题]

**核心论点：** 1-2句话
**承诺（本章对后续章节的承诺）：**
- [例如"将在第4章用AHP验证该评价体系"]
**交付（本章兑现了前序章节的哪些承诺）：**
- [例如"兑现了第2章提出的三层指标框架"]
**关键数据/定义：** 关键数字、术语定义、模型名称（供跨章核对）
**本章问题摘要：** 🔴🟡问题概览（1-3条最关键的）
```

During Round 3 setup, compare summary cards against Round 1's dependency map:
- Summary shows dependency Round 1 missed → **add to Round 3**
- Round 1 mapped dependency no summary confirms → **demote or remove**

Conflict with Round 1: default to Round 2 evidence (per Core Rules § Conflict Resolution).

---

### Round 3: Inter-Chapter Consistency Review

**Input per pair:** Thesis summary block + both summary cards + both chapter full texts. In iterative mode: also receives cross-chapter prior issues for verification.
**Pairs:** Merged from Round 1 dependency map + Round 2 summary card validation.

#### Pair Selection Stopping Rule

- **🔴 pairs** — mandatory
- **🟡 pairs** — review only if summary cards show concrete promise/deliverable link or data/terminology risk; skip otherwise
- **🟢 pairs** — skip unless user requests exhaustive mode

#### Coverage Transparency

Output at end of Round 3:
```
章节配对审查覆盖情况：
✅ 已完成：第1章 → 第5章（🔴，研究问题→结论回应）
✅ 已完成：第3章 → 第4章（🔴，方法→结果兑现）
⏭ 已跳过：第2章 → 第3章（🟡，摘要卡无具体承诺/交付链接）
⏭ 已跳过：第4章 → 第5章（🟢，未进入本轮）
```

#### Spot Check Mechanism (Iterative Mode Only)

**Purpose:** Validate Round 2 Phase A "无新发现" claims through targeted re-examination. Provides a deterrent against superficial review.

**Trigger Conditions:**
A spot check is triggered when ALL of the following are true:
1. A chapter's Phase A declared "本章未发现新问题"
2. AND that chapter has historical 🔴 issues OR 3+ historical 🟡 issues

**Procedure:**
1. Select 1-2 subsections (500-1000 characters each) from the triggered chapter
2. Perform focused re-review on **two dimensions only**: data consistency + terminology consistency
3. Output result to `review_working.md`

**Limits (Cost Control):**
- Maximum **3 spot checks** per review cycle
- Each spot check covers **500-1000 characters only**
- Focus on **2 dimensions only** (data + terminology)

**Output Format (to `review_working.md`):**
```markdown
### 抽查验证

**章节：** 第X章 §X.X（L###-L###）
**抽查原因：** Phase A声明无新发现，但该章有历史🔴问题[#1][#5]
**抽查维度：** 数据一致性、术语一致性
**抽查结果：**
- ✅ 未发现Round 2遗漏的问题（支持Phase A声明）
- ⚠️ 发现潜在遗漏（需补充至问题清单）：
  - [问题描述]
```

**Integration with Final Output:**
- Spot check results are recorded in `review_working.md` only
- If spot check finds omissions, add them to the consolidated issue list with tag `[抽查补充]`
- `review_results.md` format remains unchanged (user does not see spot check details)

#### Reading Strategy (per pair)

**Full-text reading of both chapters is MANDATORY.** Summary cards are navigation index only.

1. Read both summary cards → understand expected promise/deliverable relationship and key data points
2. Read Chapter A in full → note claims, numbers, definitions, commitments
3. Read Chapter B in full → actively cross-check against Chapter A notes
4. Document all inconsistencies found

**Long-input fallback:** If a chapter pair exceeds stable single-pass context, read each chapter in chunks but ensure a final cross-check pass covers all noted data points and commitments from both chapters before concluding.

#### Pre-Round 3: Dependency Map Reconciliation

1. List Round 1's dependency pairs
2. Check each summary card's "承诺"/"交付" against Round 1's pairs
3. Produce **final pair list**: confirmed + newly discovered − demoted
4. Document changes briefly

#### Review Checklist (per pair)

| Item | What to Check | Type |
|------|--------------|------|
| **Terminology alignment** | Same concepts use same terms across chapters? | [D] |
| **Data/number consistency** | Same statistics, sample sizes, dates consistent? | [D] |
| **Scope alignment** | Chapter B delivers what A promised? B introduces undeclared scope? | [D] |
| **Cross-reference suspicion scan** | Suspicious 图/表/章/节 references or numbering jumps? | [S]/[M] |
| **Logical continuity** | Transition makes sense? Logical gaps or contradictions? | [D] |

Cross-references are **not a primary hard-check item** — only flag suspicious cases for manual Word verification.

---

## Phase 3: Consolidation & Output

After all 3 rounds, consolidate into a single **issue-centric** document. Each issue appears once; originating round noted in brackets.

### Output Files

| File | Location | Content |
|------|----------|---------|
| `review_results.md` | Working directory | Final consolidated review (user-facing deliverable) |
| `review_working_<YYYYMMDD_HHMMSS>.md` | `review_artifacts/` | Round 1 dependency map, Round 2 summary cards, Round 3 pair logs, all intermediate findings |
| `thesis_full_text_<YYYYMMDD_HHMMSS>.txt` | `review_artifacts/` | Extracted plain text from docx (Phase 1 output) |

**Directory structure:**
```
working_directory/
├── review_results.md
└── review_artifacts/
    ├── thesis_full_text_20260325_143052.txt
    └── review_working_20260325_143052.md
```

**Notes:**
- Create `review_artifacts/` directory if it does not exist
- Timestamp format: `YYYYMMDD_HHMMSS` (local time)
- Working file serves as execution evidence and traceability record
- In iterative mode, each review cycle creates a new timestamped working file

### Working File Structure (Iterative Mode)

In iterative mode, `review_working.md` must include the following sections to serve as execution evidence:

```markdown
# 评审工作文档（第X版）

## Round 1: 宏观结构审阅
[依赖关系图 + 宏观发现]

## Round 2: 逐章深度审阅

### 第1章 [章节名] - Phase A 独立发现
**审阅维度覆盖：** [详细checklist]
**独立发现问题：** [列表或"无"]

### 第1章 - Phase B 历史问题验证
**注入问题：** [编号列表]
**验证结果：** [表格]
**章节摘要卡：** [标准格式]

[...其他章节...]

## Round 3: 跨章一致性审阅
[配对审查记录]

## 抽查验证
[抽查记录，如有]

## 历史问题验证汇总
[所有历史问题的验证状态汇总表]
```

**Key Points:**
- Phase A and Phase B records must be clearly separated
- Dimension coverage checklist must include specific descriptions (not just checkmarks)
- Spot check records (if any) must be included
- This structure provides traceability for the review process

### Consolidation Rules

**De-duplication:** Keep the most specific/actionable version of each issue. Other rounds noted as supporting evidence only. When merging related-but-distinct issues, verify they truly share the same root problem — two issues that share a *topic* (e.g., both about Chapter 1) but target different *defects* (e.g., tone vs. evidence gap) must remain separate entries.

**Conflict resolution:** See Core Rules § Conflict Resolution.

**Coverage verification (mandatory before finalizing):** Before writing the final output, confirm that every distinct finding from all 3 rounds is either included in the consolidated issue list, explicitly merged into another issue, or dropped with a stated reason. No finding may be silently lost.

**Iterative mode — prior issue handling:**
- All prior issues verified by the rounds are collected here
- Issues marked ✅已修改 go into "修订情况核查" only (not into the problem list)
- Issues marked ⚠️部分修改 go into both "修订情况核查" and the problem list (tagged `[部分修改]`)
- Issues marked ❌未修改 go into both "修订情况核查" and the problem list (tagged `[延续]`)
- Newly discovered issues in this review are tagged `[新发现]` in the problem list

**Persistent issues:** If the same issue has been flagged across 3+ consecutive versions:
1. Acknowledge explicitly ("已连续N版提出")
2. Provide minimum-cost fix — exact replacement text + location
3. Assess defense risk
4. Version 4+: shift to "if you cannot fix, prepare an oral answer for defense"

**Convergence criteria** (assess and report in 总体评价):
- [ ] Zero 🔴 items
- [ ] All 🟡 either fixed or accepted with defense prep
- [ ] No new issues in full 3-round review
- [ ] Suspicious cross-references flagged for manual Word check

### Output Template

**Template instructions (do NOT include these in the final document):**
- §一 修订情况核查: include only in iterative mode (prior `review_results.md` exists). Omit entirely in first-version mode.
- §二 问题清单: contains ALL current open items (unfixed prior + partially fixed prior + newly discovered). In first-version mode, all issues are implicitly `[新发现]` and the tag may be omitted.
- §三 收敛评估: include only in iterative mode.
- [S] items must use uncertain wording ("疑似…""建议核查…"); [M] items must state what needs manual verification.

```markdown
# 硕士学位论文评审意见（第X版）

**论文题目：** ...
**学位类别：** ...
**评审日期：** ...

---

## 一、修订情况核查

| # | 原问题概述 | 原严重度 | 修改状态 | 评价 |
|---|-----------|---------|---------|------|
| 1 | ... | 🔴 | ✅已修改 | 数据已更正 |
| 2 | ... | 🟡 | ⚠️部分修改 | 第2章已改，第4章仍有3处 |
| 3 | ... | 🔴 | ❌未修改 | 仍缺失 |

---

## 二、本版问题清单

**排序：** 🔴优先，同级别按影响范围（全局 > 跨章 > 单章）排序。

每条格式：
> **[编号] [🔴/🟡/🟢] [延续/部分修改/新发现] 问题标题**
> - **位置：** 第X章 / 第X章→第Y章 / 全局
> - **来源：** [R1] / [R2] / [R3]（可多项）
> - **验证状态：** [D]已确认 / [S]疑似 / [M]需人工核查
> - **问题描述：** 具体说明，引用原文
> - **修改建议：** 可操作的具体建议

### 🔴 必须修改
### 🟡 强烈建议修改
### 🟢 建议修改

---

## 三、总体评价

### 优点（3-5条）
### 整体结论与修改优先级
### 收敛评估

---

## 四、审查覆盖情况

### 4.1 章节配对覆盖（Round 3 coverage log）
### 4.2 人工核查待办（[M]类问题）
- [ ] [具体项目]

---

## 五、答辩提醒（可选）
```

---

## Output Specification

- **Language:** Chinese, with English terms where academically standard
- **Format:** Markdown (.md), filename `review_results.md`
- **Tone:** Strict but constructive — every criticism paired with a specific fix suggestion
- **Priority:** 🔴🟡🟢 consistently used across all rounds and versions

---

# Part II: Reference Knowledge

The following sections are **reference material** for the agent to consult during review. They are not execution rules.

---

## Appendix A: Default Dependency Patterns

Common dependency pairs for standard thesis structure. Use as starting point for Round 1 dependency map.

| Pair | What to Check |
|------|---------------|
| **Introduction → Literature Review** | Research questions fully covered by literature? Irrelevant literature present? |
| **Introduction → Conclusion** | Every research question answered? Conclusion claims within intro scope? |
| **Literature Review → Methodology** | Conceptual framework operationalized in method? Method justified by gap? Terminology consistent? |
| **Methodology → Results** | Every described method/instrument executed and reported? Undescribed methods appearing? Variable names consistent? |
| **Results → Discussion/Conclusion** | Every finding discussed? Over-interpretation beyond data? Statistical conclusions match data? |

---

## Appendix B: Chapter-Specific Focus Areas

Additional focus when reviewing specific chapter types in Round 2.

| Chapter Type | Additional Focus |
|-------------|-----------------|
| **Introduction** | Research gap specificity, innovation points clearly stated and not overstated, stated framework matches actual thesis structure |
| **Literature Review / Theory** | Theory bloat (describe 5, use 2), citation format, gap analysis → methodology link |
| **Methodology** | Rationale stated, internal consistency; *(if quantitative)* sample justification, validity/reliability, reproducibility |
| **Results / Analysis** | Table-text data consistency; *(if quantitative)* test choices, hypotheses; *(if qualitative)* interpretation grounded in evidence |
| **Discussion / Conclusion** | No over-interpretation, all questions answered, limitations honest; *(if practice-oriented)* actionable recommendations for practitioners, not just theoretical implications |
| **English Abstract** | Grammar, non-idiomatic phrasing ("Aiming at", "Firstly/Secondly"), keyword consistency |
| **Appendices** | Alignment with main text; *(if survey)* question design, scale coverage, response options |

---

