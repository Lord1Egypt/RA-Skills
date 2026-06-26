# Target-Paper Results Style Adaptation Mode — Full Specification

Moved from main SKILL.md §19.

## Core Principle

This mode performs **structure/style modeling, not content imitation**.

**Allowed to transfer:** Results organization, subsection order, paragraph sequence, figure/table narrative strategy, statistical reporting order, cautious language patterns, Results–Discussion boundary style, target-journal tone and formatting.

**Forbidden to transfer:** Original sentences, target paper data, target paper statistics, target paper conclusions, target paper theoretical interpretations, author-specific writing style, analysis structures incompatible with user's design.

---

## Step 1: Extract Target Results Style Profile

Extract from target paper: A) Results structure (subsection headings, order), B) Paragraph-level writing pattern, C) Statistical reporting convention, D) Figure/table narrative style, E) Cautious language and boundary, F) Transferable vs. risky style distinction.

**Transferable-vs-risky distinction must include:**
- **Transferable:** subsection order, figure-first approach, main → supplementary progression, simple effects post-interaction, restrained null-result wording
- **NOT transferable:** text-table contradictions, strong causal language in cross-sectional studies, Discussion-level mechanisms in Results, author conclusions beyond data support

---

## Step 2: Design-Match Check

Check dimensions: study design match, statistical type match, figure/table type match, result order transferability, modules that should NOT transfer.

If mismatch, label: transferable structures, non-transferable structures, alternatives.

---

## Step 3: Build Style Transfer Plan

Short plan covering: transferable structures, non-transferable content, paragraph order for user data, suitable writing patterns, patterns NOT applicable, user's target journal format preservation, output depth selection.

---

## Step 4: Write User Results from User Data Only

Target paper provides only: structure, writing order, statistical reporting habits, figure narrative approach, cautious tone.

Target paper does NOT provide: statistics user didn't give, variables user didn't give, significance user didn't give, figure trends user didn't give, conclusions user didn't give.

---

## Default Output Format (Gating Rule)

8-section format only when BOTH:
1. Target source is accessible (PDF / Results text / v3.0 output)
2. At least 3 specific writing evidence points extracted from target source

8-section output:
1. 【目标文献 Results 写法提取】
2. 【设计匹配与可迁移性判断】
3. 【适配到本文的结果组织方案】
4. 【可直接使用的结果段】
5. 【统计报告检查】
6. 【结果与讨论边界提醒】
7. 【与目标文献的相似点和差异】
8. 【可选替代表达】

If conditions not met → fallback format (see §19.14 in main SKILL).

---

## Key Guardrail Rules

### Target Source Resolution & Fail-Closed (§19.14)
Must establish Source Ledger: Target source / User data source / User draft source / Missing target.
If Target source is missing → stop target-paper adaptation, switch to fallback.

### Input Decontamination (§19.15)
Content under "我的数据"/"用户数据" tags is user data, NOT target paper evidence. Only content explicitly labeled as target paper can be used for style extraction.

### Minimum Evidence Rule (§19.16)
Must provide ≥3 specific evidence points from actual Target source before claiming style extraction.

### Partial Extraction Limits (§19.17)
Based on extraction coverage: Sufficient for design mismatch judgment → Sufficient for limited style extraction → Insufficient for full style adaptation. Never claim "complete extraction" on partial read.

### Design-Incompatible Fallback (§19.18)
When target design is fundamentally incompatible with user design, switch to design-incompatible handling: most structures non-transferable, organization driven by user data + general Results conventions, never claim style transfer.

### Anti-Test-Context Carryover (§19.19)
Never reference internal test names (Test A/B/C/D) or historical test results in formal output.

---

## Additional Guardrails

### Target-Paper Risk Extraction Rule (§19.7)
Target paper errors/contradictions must NOT be migrated as "learnable writing." Mark as "不可迁移 / 风险写法."

### Derived-Statistic Source Rule (§19.9)
Any statistic calculated from user-provided basics must be labeled "根据用户提供信息推算." Never label derived statistics as "user input."

### No-Assumed-Target-Metadata Rule (§19.10)
Never infer target paper metadata (sample size, statistics, subject characteristics) from domain knowledge when not provided.

### No-Placeholder Table/Figure Rule (§19.11)
Never write "Table X shows..." or "Figure X presents..." in formal Results unless user provided the table/figure number AND content.

### Variable Translation Rule (§19.12)
First occurrence: Chinese name (English original). Subsequent: Chinese name only.

### Cross-Sectional Mediation Prefix Rule (§19.13)
All direct/indirect/total effects must carry "统计" prefix in cross-sectional studies. Hard self-check.
