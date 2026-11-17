# Academic and Technical Chinese

**Before writing or editing anything for a paper or a technical document**, read the 术语 rows in the glossary box `## Boxes` in `~/Clawic/data/chinese/memory.md` names, and any `artifacts/` 术语表 for that paper or product. A term rendered two ways inside one paper is a defect a reviewer will name.

**Contents:** [Self-Reference](#self-reference) · [论文 Structure](#论文-structure) · [摘要 and 关键词](#摘要-and-关键词) · [Academic Register](#academic-register) · [Hedging and Claim Strength](#hedging-and-claim-strength) · [Technical Terminology](#technical-terminology) · [References and Citation](#references-and-citation) · [Figures, Tables, and Formulas](#figures-tables-and-formulas) · [Technical Documentation](#technical-documentation) · [What Gets Written Down](#what-gets-written-down)

## Self-Reference

| Form | Use |
|---|---|
| 本文 | "This paper" — the default subject for anything the paper does: 本文提出…, 本文认为… |
| 本研究 | "This study" — for the work rather than the document |
| 笔者 | "The present author" — for opinion and judgement, used sparingly |
| 我们 | Acceptable in co-authored papers in many fields; check the journal |
| 我 | A register error in a Chinese paper, in every field |

我认为 in a 论文 is the most common register mistake made by writers who learned Chinese conversationally. 本文认为 is the same claim at the right altitude.

## 论文 Structure

Standard shape for a Chinese journal article or thesis chapter:

摘要 → 关键词 → 引言 → 相关工作 / 文献综述 → 方法 → 实验 / 结果 → 讨论 → 结论 → 参考文献 → 致谢 (theses) → 附录

- 引言 states the problem, the gap, and what this paper does — in that order, and the "what this paper does" paragraph is expected to be explicit: 本文的主要贡献如下：（1）…（2）…
- 相关工作 in Chinese papers is often more descriptive and less argumentative than the Western equivalent; a critical literature review is welcome in humanities and unusual in engineering.
- Numbering uses the decimal system inside a paper (1、1.1、1.1.1) rather than the 公文 hierarchy (`punctuation.md`).
- Theses (学位论文) carry additional mandated sections — 独创性声明, 授权书, 中英文摘要 — and their format is set by the university, not the journal.

## 摘要 and 关键词

- 摘要 is typically 200-300 字 for a journal article and longer for a thesis; **the journal's own guidelines override any general figure**, and they vary widely. Check before writing to a length.
- The abstract is a miniature of the paper — 目的、方法、结果、结论 — and takes no citations, no abbreviations defined nowhere else, and no 本文 filler like 本文首先介绍了…然后….
- 关键词: 3-5, separated by 分号 (；) in most journals, ordered general to specific. They are indexing terms, not a summary.
- English abstract (英文摘要) is required by most Chinese journals and is not a word-for-word translation — it follows English academic conventions, including the passive voice Chinese avoids (`translate`).

## Academic Register

| Casual | Academic |
|---|---|
| 很多 | 大量 / 众多 / 大部分 |
| 差不多 | 大致相当 / 基本一致 |
| 因为 | 由于 / 鉴于 |
| 所以 | 因此 / 故 |
| 但是 | 然而 / 但 |
| 用 | 采用 / 利用 / 借助 |
| 做 | 进行 / 开展 (one of the few places 进行 is correct) |
| 看出 | 表明 / 显示 / 可见 |
| 提高了 | 提升了 / 改善了 |
| 我们发现 | 结果表明 / 研究发现 |

Note the exception: SKILL.md Rule 6 deletes 进行 + noun in ordinary prose, and academic Chinese is where 进行实验, 开展研究 and 予以验证 are genuinely the register. The rule is about machine-flavoured *ordinary* text; a paper that reads colloquially fails a different test.

## Hedging and Claim Strength

Chinese academic writing hedges with a distinct vocabulary, and mismatching the hedge to the evidence is what reviewers catch:

| Strength | Phrasing |
|---|---|
| Demonstrated | 结果表明 / 实验证明 / 数据显示 |
| Supported | 结果支持…的假设 / 与…的结论一致 |
| Suggested | 结果提示 / 可能表明 / 在一定程度上说明 |
| Speculative | 推测 / 有待进一步验证 / 尚需更多证据 |
| Limitation | 本研究的局限在于… / 受样本量限制 |

证明 (proves) is strong and should be reserved for mathematics and formal results; using it for a statistical association is the claim-inflation reviewers flag first.

## Technical Terminology

- **One term, one rendering, per document.** The same English term appearing as 鲁棒性 in section 2 and 稳健性 in section 4 is a defect even though both are correct.
- Established Chinese renderings exist for most technical vocabulary and are not negotiable: 算法, 数据库, 并发, 缓存, 梯度下降, 卷积. Inventing a new one reads as not knowing the field.
- **First occurrence carries the English in brackets**: 鲁棒性（robustness）. Thereafter Chinese only. Some journals invert this for very new terms.
- Untranslated English is acceptable in mainland technical writing for acronyms and tool names (GPU, Transformer, Docker) and less so in Taiwanese writing (`regions.md`).
- Mainland and Taiwan diverge sharply in technical vocabulary: 软件/軟體, 数据/資料, 程序/程式, 算法/演算法, 内存/記憶體, optimization 优化/最佳化. A paper written for a Taiwanese journal needs the Taiwanese term set, not a script conversion.
- 名词委 (the national committee on scientific terminology) publishes standardised renderings for many fields; where a discipline has one, it settles arguments.

## References and Citation

- **GB/T 7714** is the Chinese national bibliographic standard and is what most Chinese journals require. Its distinguishing features: a document-type marker in brackets after the title — [J] journal article, [M] monograph, [D] dissertation, [C] conference paper, [S] standard, [P] patent, [EB/OL] online resource — and author names in 姓名 order with given names abbreviated for Latin-script authors.
- Two citation systems coexist: 顺序编码制 (numbered by order of appearance, superscript [1]) and 著者-出版年制 (author-year). The journal picks; do not mix.
- Chinese-language and English-language references are usually listed together, Chinese first, though some journals separate them.
- 参考文献 is the cited list; 注释 (footnotes) carry commentary and are numbered separately in humanities papers.
- Verify the exact required shape against the target journal's 投稿须知 — GB/T 7714 has editions and journals customise it.

## Figures, Tables, and Formulas

- 图1, 表1, 式(1) — numbered sequentially, referenced in the text before they appear.
- **Table captions go above the table; figure captions go below the figure.** The reverse is a copy-editing error every Chinese journal catches.
- Captions are bilingual in many journals: 图1 系统架构 / Fig.1 System architecture.
- Units follow the international system with half-width formatting inside the number (`punctuation.md`): 3.5 kg, 25 ℃.
- Formulas are numbered right-aligned in brackets and referenced as 式(1), not 公式1.

## Technical Documentation

Not a paper, and a different register again — product documentation, API docs, internal design documents:

- Imperative and short. 点击「保存」 not 用户可以点击保存按钮来保存.
- Second person 你 or no person at all; 您 in user-facing documentation for consumer products, 你 for developer documentation.
- UI strings in the document match the product exactly and go in 「」 or quotes; if the product is in English, the string stays in English (`translate`).
- Code, commands, paths and identifiers are half-width and never translated.
- 注意 / 警告 / 危险 as the escalation ladder for callouts, matching the international 
convention of caution / warning / danger.
- Chinese technical documentation conventionally uses more headings and shorter sections than English does, because Chinese characters are dense and long paragraphs are heavy on screen.

## What Gets Written Down

- **Every technical term rendered for the first time, with the English source** → a `### Terms` row with the field and the date. In a paper this is not optional bookkeeping: consistency across sections is what the row buys.
- **A per-paper or per-product 术语表** once there are more than a handful → `artifacts/terms-<paper-or-product>.md`, with its `## Boxes` line. Different papers may legitimately use different renderings; one shared glossary would force a false consistency.
- **The target journal's requirements that cost effort to find** — abstract length, citation system, whether the English abstract is a translation → `## Environment`, keyed by journal name.
- **A reviewer's terminology or register correction** → `### Corrections`, with the reviewer's wording. Reviewer corrections are the most authoritative input this domain gets.
