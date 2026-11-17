# Cross-Database Literature Search: Selection, Strategy, Syntax Adaptation and Labeling

> English summary: methodology for cross-database literature search — choose databases by question type (not by habit), build layered search strategies, adapt syntax per database, normalize to a minimum field set, dedupe and prepare for screening, and label preprints / evidence status (Tier 1/2/3/P). This fills the manual-database layer (Embase / Cochrane / WoS / registries / preprints) that sits beyond ct-literature's existing automated OpenAlex + Europe PMC + Semantic Scholar sources.
>
> **Adapted from**: `multi-database-literature-collector` — AIPOCH, MIT License
> **Source**: https://github.com/aipoch/medical-research-skills
> **Migrated**: 2026-08-04 (into ct-literature)

---

## 1. Relation to ct-literature's automated sources

`ct-literature` already retrieves and merges three **API-accessible, keyless** sources automatically:

| Automated (already implemented) | Role |
|---|---|
| OpenAlex | Primary, citation-rich, broad coverage |
| Europe PMC | MEDLINE / MeSH biomedical precision |
| Semantic Scholar | Citation ranking (optional, rate-limited) |

This file governs the **manual / subscription / non-API layer** that a systematic review still needs, and the general methodology (strategy construction, syntax adaptation, tiering) that applies to *all* sources including the automated ones.

| Manual layer | When it must be added |
|---|---|
| **Embase** | Drug, pharmacology, European journals; mandatory for a Cochrane-grade drug SR |
| **Cochrane Library (CENTRAL)** | Controlled-trial and review-oriented clinical evidence |
| **Web of Science** | Citation-indexed retrieval, cross-disciplinary coverage |
| **ClinicalTrials.gov / registries** | Ongoing and unpublished trials (→ delegate to `ct-registry`) |
| **bioRxiv / medRxiv / arXiv** | Preprints and methods not yet indexed |
| **Google Scholar** | Broad recall, citation chaining, grey literature |

---

## 2. Database selection rules

Select by **question type, not by habit**.

1. Use at least 2–3 databases for any cross-database collection task.
2. Justify each choice with a concrete purpose — never add a database to lengthen the list.
3. For every selected database, state:
   - why it is included,
   - what it is expected to contribute,
   - what it is likely to miss.

Worked mapping:

| Question type | Minimum set |
|---|---|
| Drug efficacy SR / meta-analysis | OpenAlex + Europe PMC + Embase + CENTRAL |
| Safety / pharmacovigilance evidence base | OpenAlex + Europe PMC + Embase (+ `ct-safety` for FAERS) |
| Methodological / statistical question | OpenAlex + WoS + arXiv |
| Landscape / competitive intelligence | OpenAlex + registries (`ct-registry`) + preprints |
| Rapid background for a protocol introduction | OpenAlex + Europe PMC only (declare the limitation) |

---

## 3. Search strategy construction

Optimize recall first; narrow later.

**Elements to build (as relevant)**

- disease / condition terms
- intervention / exposure / biomarker / mechanism terms
- outcome or evidence-type terms
- modality / method terms
- synonyms, abbreviations, spelling variants (US/UK)

**Layered strategy**

```
Layer 1  broad core concept search              (recall anchor)
Layer 2  concept × evidence-type refinement     (RCT / SR / meta-analysis filters)
Layer 3  optional recent-update layer           (date-restricted, for surveillance runs)
```

**Principles**

- Start broad enough to avoid premature exclusion.
- Add narrowing only when the topic is too diffuse.
- Apply date filters only when the user asks or the task is update-oriented.
- Apply study-type filters only when necessary — they silently drop conference abstracts and preprints.

**Required transparency** — always report: key terms used, synonym logic, filters applied, and restrictions deliberately *not* applied.

---

## 4. Database syntax adaptation

Never copy one query string across databases unchanged.

| Database | Query style | Field focus | Known compromise |
|---|---|---|---|
| **PubMed / Europe PMC** | Controlled vocabulary + free text | MeSH where appropriate, plus `[tiab]` | MeSH indexing lags ~6–12 months; MeSH-only queries miss recent papers |
| **Embase** | Emtree + free text | `/exp` explosion, `:ti,ab` | Subscription required; Emtree ≠ MeSH, must re-map drug terms |
| **Cochrane CENTRAL** | Simplified MeSH + free text | Trial-oriented | Poor for observational designs |
| **Web of Science** | Topic search `TS=`, phrase logic | Citation-linked retrieval | No controlled vocabulary; phrase precision matters |
| **Google Scholar** | Short, concise queries; phrase search | Full text | Noisy, unstable metadata, no reproducible export — use for recall and citation discovery, not as a primary record source |
| **Preprint servers** | Focused, narrow queries | Title/abstract | Must be explicitly labeled as preprints |

For each database used, document: query style, field focus, date filters, and the database-specific compromise accepted.

---

## 4.1 Chinese databases (CNKI / 万方 / SinoMed) and Web of Science

> 中文小节 / Chinese subsection. Covers the databases a China-facing evidence base
> (NMPA context, Chinese-population studies, journals not indexed in MEDLINE, 学位论文
> and 会议论文) cannot skip, plus the Web of Science syntax note.

**⚠️ 各库字段符随版本调整，使用前请以该库当期检索说明为准。**
The field codes and the exact/fuzzy operators below are the *commonly seen* forms, not a
guarantee: CNKI / 万方 / SinoMed have all changed their search UIs and 专业检索 syntax
across versions. Two rules that keep you safe:

1. **Prefer the UI drop-downs over hand-written codes.** All three databases expose
   高级检索 with a field drop-down (主题 / 题名 / 关键词 / 摘要 / 作者 / 作者单位 / 期刊)
   plus an 精确 / 模糊 toggle and a 并含 / 或含 / 不含 logic selector. Selecting the field
   from the drop-down is version-stable; typing a code is not.
2. **Run a minimal validation query first.** Before pasting the full strategy, run
   `A AND B` (two single words) in the same box. If the current version rejects it, find
   out what it accepts *before* transcribing the full strategy — never assume.

### 4.1.1 What is safe to assume (all three)

| Element | Support |
|---|---|
| Boolean `AND` / `OR` / `NOT` (upper case) | Supported; the only operator set to rely on |
| Parentheses `( )` for grouping | Supported in the professional/expert search box; ⚠️ in a single 高级检索 row it may not be — split OR-groups across rows using 或含 instead |
| Exact phrase | English double quotes `"…"` in the professional box; ⚠️ in 高级检索 rows the 精确/模糊 toggle is the reliable control |
| Truncation / wildcards | **Differs per database and per version — verify per run, do not assume `*` behaves as it does in PubMed** |

### 4.1.2 Field codes (common forms — ⚠️ verify against the current help page)

| Semantic field | CNKI 中国知网 | 万方 WanFang | SinoMed 中国生物医学文献服务系统 |
|---|---|---|---|
| 主题 (title+keywords+abstract) | `SU=` exact / `SU%` fuzzy | `主题:(…)` | use the 高级检索 field drop-down (推荐) |
| 题名 / title | `TI=` / `TI%` | `题名:(…)` | drop-down; ⚠️ command-box code not assumed here |
| 关键词 / keywords | `KY=` / `KY%` | `关键词:(…)` | drop-down |
| 摘要 / abstract | `AB=` / `AB%` | `摘要:(…)` | drop-down |
| 作者 / author | `AU=` | `作者:(…)` | drop-down |
| 作者单位 / affiliation | `AF=` | `作者单位:(…)` | drop-down |
| 期刊 / source | `JN=` (⚠️ older versions used `LY=`) | `刊名:(…)` | drop-down |

SinoMed deliberate omission: its 高级检索 is drop-down driven and its 智能检索 applies
its own term mapping, so **no command-box field codes are asserted for SinoMed in this
document**. Use the drop-downs, or read the code list off the in-product help page.

### 4.1.3 Worked conversion of the §3 strategy

Running example — P: 非小细胞肺癌 / NSCLC · I: 奥希替尼 / osimertinib ·
evidence type: RCT OR 系统评价/Meta 分析.

**CNKI — 高级检索 (drop-down path, most stable)**

| 行 | 逻辑关系 | 字段 | 匹配 | 值 |
|---|---|---|---|---|
| 1 | — | 主题 | 模糊 | 非小细胞肺癌 |
| 2 | 并含 | 主题 | 模糊 | 奥希替尼 |
| 3 | 并含 | 主题 | 模糊 | 随机对照试验 |
| 4 | 或含 | 主题 | 模糊 | 系统评价 |
| 5 | 或含 | 主题 | 模糊 | Meta分析 |

Row 3–5 is the OR-group expressed as 或含 rows rather than one parenthesised expression.
⚠️ The row-to-row combination order (whether the OR-group is evaluated before the AND)
is version-dependent — check the hit count of the OR-group alone first, then add the
AND rows and confirm the count shrinks as expected.

**CNKI — 专业检索 (⚠️ codes per current help page)**

```
SU='非小细胞肺癌' AND SU='奥希替尼' AND (SU='随机对照试验' OR SU='系统评价' OR SU='Meta分析')
```

**万方 — 专业检索 (⚠️ codes per current help page)**

```
主题:(非小细胞肺癌) AND 主题:(奥希替尼) AND (主题:(随机对照试验) OR 主题:(系统评价) OR 主题:(Meta分析))
```

**SinoMed — 高级检索**

```
行1  主题 / 常用字段 = 非小细胞肺癌      (AND)
行2  主题 / 常用字段 = 奥希替尼          (AND)
行3  主题 / 常用字段 = 随机对照试验      (AND)
行4  主题 / 常用字段 = 系统评价          (OR)
行5  主题 / 常用字段 = Meta分析          (OR)
研究类型 / 文献类型 → 用「限定条件」面板选择，而不是写进检索式
```

SinoMed exposes 文献类型 and 年份 through its 限定条件 panel rather than the query
string — use the panel, and record in the PRISMA appendix that the filter came from the
panel (it is not reproducible from the query text alone).

**Web of Science**

```
TS=("non-small cell lung cancer" OR NSCLC) AND TS=(osimertinib)
   AND (TS=("randomized controlled trial") OR TS=("systematic review") OR TS=(meta-analysis))
```

WoS notes: `TS=` = topic (title + abstract + author keywords + KeyWords Plus); `TI=` title,
`AB=` abstract, `AK=` author keywords, `AU=` author, `PY=` publication year, `SO=` source
title, `DO=` DOI. Operators: `AND` / `OR` / `NOT`, plus `NEAR/x` and `SAME` for
proximity. `"…"` is an exact phrase. `*` is a right-hand (and mid-word) wildcard whose
behaviour is **not** identical to PubMed's — verify with one probe before relying on it.
WoS has **no controlled vocabulary**, so synonyms, abbreviations and spelling variants
must be enumerated by hand; this is the accepted compromise recorded in §4.

### 4.1.4 Export (no API — manual)

None of CNKI / 万方 / SinoMed exposes a documented public search API, and all three are
subscription-gated. **This skill does not crawl them.** Records must be exported by an
agent or by browser automation first, then imported (§9).

| Database | Export entry | Formats | Note |
|---|---|---|---|
| CNKI | 检索结果页 → 勾选 → 导出/参考文献 | RefWorks / NoteExpress / EndNote / GB/T 7714 (⚠️ availability varies) | per-batch cap (⚠️ commonly seen: 50 / 500) — export in batches |
| 万方 | 检索结果页 → 导出 | RefWorks / NoteExpress / EndNote / 自定义 | per-batch cap — export in batches |
| SinoMed | 结果集 → 输出 / 保存 | 文本 / RefWorks (⚠️) | per-batch cap — export in batches |

Per-record `source` must be set to `CNKI` / `WanFang` / `SinoMed` at import time so the
merged evidence base stays source-attributable (§5 source-preservation rule).

---

## 5. Result normalization

A cross-database collection is only usable if records are normalized to one schema.

**Minimum record fields**

`title` · `authors` · `year` · `journal/venue` · `source_database` · `abstract_or_snippet` · `study_type` · `direct_link` · `doi` · `pmid` · `evidence_status` · `preliminary_tier`

**DOI rule** — include the DOI when available and verified. If absent or unverifiable, write `DOI not available` or `DOI not verified`. **Never insert placeholder DOI strings.**

**Link rule** — every formal record needs a real, verifiable direct link: DOI landing page, PubMed, PMC, journal page, or preprint server page.

**Source preservation rule** — never strip source metadata; keep the originating database on every record even after merging. (`ct-literature`'s merge step already carries a `source` field — keep it populated for manually added records too.)

---

## 6. Deduplication and screening readiness

Fields that must survive merging for deduplication to work: `title`, `authors`, `year`, `doi`, `pmid`, `journal`, `source_database`.

Output must support: title/abstract review · study-type filtering · source-specific backtracking · preprint separation · later full-text retrieval.

Always state the next step explicitly: deduplicate → title/abstract screen → separate preprints → prioritize Tier 1 reading.

---

## 7. Preliminary priority layering

First-pass organization, **not** final inclusion.

| Tier | Definition |
|---|---|
| **Tier 1** | Highly likely core papers, directly relevant to the question |
| **Tier 2** | Possibly relevant / borderline, needs screening |
| **Tier 3** | Background, context, indirect support |
| **Tier P** | Preprints — separated regardless of likely relevance |

Tiering signals: directness to the question · study-type relevance · recency (when appropriate) · population/intervention/condition/mechanism match · original evidence vs background context.

**Restriction** — tiering must never be presented as a final inclusion/exclusion decision. That belongs to a screened PRISMA flow.

---

## 8. Evidence-status labeling

Do not mix evidence-status categories into one unlabeled list. Required labels:

- Peer-reviewed original study
- Review
- Guideline / consensus
- Trial registration
- **Preprint**
- Background / context paper

**Preprint rule** — preprints must be clearly labeled and, where possible, separated (Tier P). Never describe a preprint as peer-reviewed unless verified. If evidence status cannot be confirmed from source metadata, say so explicitly rather than guessing.

---

## 9. Cross-database mode in ct-literature

Trigger phrases: "cross-database", "multi-database", "Embase", "Cochrane", "Web of Science", "systematic review search strategy", "PRISMA search" (Chinese trigger phrases are mirrored in SKILL.md `triggers`).

Behaviour in this mode:

1. Run the automated three sources as usual.
2. Emit a **manual-search worklist**: for each additional database, the adapted query string, the expected contribution, and the expected gap.
3. Provide an import slot so manually exported records can be normalized into the same schema and merged/de-duplicated with the automated set.
4. Label every record with evidence status and preliminary tier.
5. Report the full strategy (terms, synonyms, filters, per-database adaptation) so the search is reproducible in a PRISMA appendix.

### 9.1 Chinese-database import slot (CNKI / 万方 / SinoMed)

**本技能不做中文库实时抓取** — no public API, subscription-gated, and the export step is
interactive. The import slot is a *file contract*, not a crawler.

> **升级项 I（2026-11-02）**：导入路径已从「手工转 payload JSON」升级为**一行 CLI 直接吃
> 用户导出的 RIS / JSON**，CJK 去重整固也已内置（繁简 / 全半角 / 中英标点不再撕裂去重）。
> 仍**不含任何爬虫、Cookie、浏览器驱动**——一次站点访问都没有。

**Step 1 — 在浏览器里检索并导出（用户自己的机构权限）**

1. 按 §4.1.3 的检索式在 CNKI / 万方 / SinoMed 检索，全选 → 导出 → 选 **RIS**（推荐）
   或 **JSON**（§4.1.4）。
2. 文件名带上库名（`cnki_export.ris` / `wanfang_2024.ris` / `sinomed.json`），
   技能据此推断数据源；文件名无特征时用 `--merge-cn-source CNKI` 显式指定。

**Step 2 — 并入检索（一条命令）**

```bash
python scripts/ct_literature.py --topic "<topic>" --run --out-dir ./out \
    --merge-cn ./cnki_export.ris --merge-cn ./wanfang_2024.ris
```

CLI 行为：

- 每个 `--merge-cn` 生成一个 `source` payload（`CNKI` / `WanFang` / `SinoMed` / `VIP`），
  与 OpenAlex / Europe PMC 走**同一套**去重、引文验证、PRISMA 统计；
- 导入留痕写入 `.merged.json → meta.imports`（文件路径 / 源名 / 条数），审计可查；
- 不支持的格式（`.nel` / `.enw` / Excel）**显式报错**并提示转 RIS，不会静默返回 0 条。

**Step 2b — 中国监管证据车道（NMPA / CDE）**

```bash
python scripts/ct_literature.py --topic "<topic>" --run --with-guidelines \
    --guidelines-region china
```

`--guidelines-region` 取 `china` / `global` / `both`（不传 = 不过滤，向后兼容）。
判定规则：**显式 `region` 字段优先**；字段缺失时按机构名兜底推断
（`CMA` / `CDE` / `NMPA` / `NHC` / `CACA` / `CSCO` → `china`，其余 → `global`）。
之所以要兜底：现网语料 96 条**全部没有 `region` 字段**，只认字段会让 china 车道恒返回
0 条。兜底后实测 `all=96 · china=4 · global=92`（CMA 中华医学会 4 条），推断结果回填到
每条记录的 `region` 字段，报告里可直接看到车道归属。

> 中文主题也能命中：`--with-guidelines` 在 0 命中时会按「英文检索式 → 各 OR 分支 → 最长词」
> 依次重试（如 `(type 2 diabetes OR T2DM)` → `diabetes`），事件 `guidelines_i18n_retry` 留痕。

**Step 3 — 跨轮累积（living review）**

```bash
python scripts/ct_literature.py --topic "<topic>" --run --out-dir ./out \
    --merge-existing ./out/.merged.json --merge-cn ./cnki_export.ris
```

**Dedup（CJK）— 已在代码内解决**

`normalize._norm_title` 对含 CJK 的题名走 `adapters/cn_ref_normalizer.normalize_cn_title`：
全角 ASCII → 半角、高频繁体 → 简体（受控单字表）、中文标点剥离、空白/大小写归一。
归一只用于**生成去重 key**，不回写 `title` 原文（原文保真优先）。

- 已覆盖：繁简异体、全半角、中英标点、全角空格。
- **未覆盖**：受控表之外的生僻繁体字（原样保留，不臆造）；同义改写的题名（需人工复核）。
- 校验口径：`merged.count` 与各文件 `导出条数之和 - duplicates_removed` 应能对上；
  对不上时按 DOI 缺失条目人工抽验。

**Zotero 本地库作为补充源（升级项 H）**

```bash
python adapters/zotero_import.py --list                       # 看集合路径
python scripts/ct_literature.py --topic "<topic>" --run \
    --zotero-import "肿瘤/NSCLC"
```

只读 Zotero 本地 API（`127.0.0.1:23119`，无 key、MCP-free、请求显式绕过系统代理）。
集合路径按名称逐级解析，0 命中或同名歧义**显式报错**；子附件与笔记不计入文献数。
Zotero 未运行时不阻断主检索，只在事件流里如实告警。

**Other field mismatches to fix at conversion:** `year` may be a full date string;
`authors` may be a single `;`-joined string; `publication` may carry the 中文刊名 only.
`cn_ref_normalizer.parse_ris` already splits `;`/`，`-joined authors and extracts the
4-digit year, so the common CNKI/万方 RIS shapes need no manual fixing.

**Cochrane (CDSR) note:** the Cochrane Database of Systematic Reviews is now retrievable directly via `--cochrane` — a verified Europe PMC journal filter (identical to meta-analysis's in-skill dedup probe, so cross-skill hit counts stay consistent). No manual browser step is needed for CDSR. Embase / Web of Science remain manual (subscription).
