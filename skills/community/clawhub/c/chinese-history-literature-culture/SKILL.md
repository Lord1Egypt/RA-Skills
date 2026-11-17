---
name: chinese-history-literature-culture
description: >
  Write, polish, and cite Chinese-language articles on Chinese history,
  literature, and culture (Five Dynasties & Ten Kingdoms, silk, Dream of the
  Red Chamber, 洛神赋, 脂砚斋, etc.). Use when the user shares their own
  outline, notes, or stream-of-thought for a 中文历史/文学/文化 article and
  wants the agent to follow that thought-flow (must), expand with web
  research, and produce a polished, well-cited draft. Output is in Chinese
  (simplified by default); source material may be in any language. Covers
  creation, polishing, fact-checking, and source selection.
---

# 中文历史·文学·文化写作 (Chinese History / Literature / Culture Writing)

Write, polish, and cite Chinese articles about Chinese history, literature, and culture. The user supplies the thinking; you supply the structure-faithful expansion, web research, and citations. Output is Chinese (Simplified by default); source material may be in any language. This skill complements `astro-sync` (publishing); for the 繁简 twin and 配图 steps see **Repo conventions**.

## Golden rules

1. **Follow the user's thought-flow — must.** Their outline, sequencing, analogies, claims, and conclusions are the skeleton. Preserve them. Never silently restructure into a generic essay, drop points, or swap in your own thesis.
2. **Keep their voice.** Polish wording and grammar. Do not flatten a personal, essayistic voice into a generic prose style.
3. **Cite, don't assert.** Every historical or literary claim is checked against sources (see Phase 2). Anything unverifiable is NOT asserted — it goes to the corrections doc under 待核实 (Phase 5).
4. **Flag before replacing.** If the user's thought contains a factual error, keep their intent. Propose the corrected wording. Get explicit approval before swapping it in. Source: AGENTS.md, "Get approval before any change".
5. **Never cite a source you have not opened and checked** (no ghost citations — see Phase 3).

## Inputs

- `source` — the user's raw text: an outline, bullet notes, a stream of thought, or a rough draft (pasted or a file path).
- `mode` — `create` (notes → article), `polish` (improve an existing draft, preserving structure/voice), or `cite` (add or verify citations, or combine with polish). Ask if unclear.
- `audience` / `tone` — optional. Default: general literate audience.

## Source quality — trusted vs. untrusted

**Trusted:** Wikisource (维基文库) primary texts; official academic institutions and museums (kaogu.cn, cssn.cn, 故宫博物院 dpm.org.cn, 中国丝绸博物馆 chinasilkmuseum.com, 国家图书馆, university presses); reference dictionaries (汉典 zdic.net); academic presses & canonical editions (中华书局, 上海古籍, 人民文学, 商务印书馆); referenced Wikipedia entries; peer-reviewed journals / CNKI.

**NOT trusted** (never evidence): 微博 / WeChat / 头条 / 抖音 / TikTok / 哔哩哔哩 / 澎湃新闻 The Paper / 光明网 gmw.cn / personal blogs / 百度百科 无参考文献词条 / forum posts / AI outputs.

**Site-level ban, not topic-level** — 澎湃 / 光明网 are blocked on these repos for every topic and every article. They may be read as leads (they often quote a real book's pages), but a claim backed only by them is **待核实**. Chase the underlying primary text or academic edition instead: for 《红楼梦》 variant readings, the Wikisource scans of 程甲本 / 程乙本 / 甲戌本 / 庚辰本 quote-verify the reading directly, which beats any commentary about it. Standing instruction from the user, 2026-10-28.

## Workflow

### Phase 1 — Understand the thought-flow

1. Read the input end to end.
2. Restate the user's **own** structure back to them: sections, key claims, and connecting logic. List anything you plan to add, cut, or move.
3. Confirm before writing, unless they asked for an immediate draft and the structure is unambiguous.

### Phase 2 — Research & source curation

4. **Search each fact independently**. Prefer site-restricted queries on trusted domains (e.g. `site:zh.wikisource.org 洛神赋`).
5. **Cross-check with ≥2 independent sources.** Record disagreements in the corrections doc rather than silently picking a side.
6. **Prefer primary text over commentary.** Verify the exact wording and chapter/回目. One verified source suffices for well-established primary-text facts (a poem's wording, a chapter number). Reserve ≥2 for contested, interpretive, or attributive claims.
7. **Verify chapter attributions against the original text, not memory** (e.g.《红楼梦》刘姥姥一进荣国府=第六回, 元妃省亲=第十八回;《诗经》titles vs《毛诗正义》).
8. **《红楼梦》versions.** Two families whose 回目 *and* 正文 differ: **脂评抄本** (甲戌/己卯/庚辰…, ending at ch80) and **程高本** (程甲/程乙, 120 回; 后四十回 by 程伟元/高鹗).
   - **脂批 ceiling**: 脂批 exists only for ch1–80. Reject any 脂批 claim on a 后四十回 event unless a specific 本 + 回 is named.
   - **Name the edition when quoting**. Where readings differ, list the variant (e.g. 第四十一回回目 庚辰本"栊翠庵茶品梅花雪　怡红院劫遇母蝗虫" / 程甲本"贾宝玉品茶栊翠庵"; 盘费 / 盘缠).
   - **脂批 check (红楼梦 articles only).** For each chapter an article quotes, look up 脂批 on the same passage in a 脂本. Example: 维基文库《脂砚斋重评石头记》, which mixes 甲戌/庚辰/己卯 comments. If a comment exists, quote it verbatim with its edition label and chapter. If none exists, add nothing to the article. Before labelling a comment with one edition, confirm the source's abbreviation (甲/甲夹/甲眉). Don't guess.

**Fetching primary texts — practical tips**
- Wikisource《红楼梦》uses zero-padded paths: `紅樓夢/第041回` (URL-encoded). `第四十一回` 404s.
- GBK/mojibake sites: fall back to zh.wikisource.org, 识典古籍, 古文岛, 国学梦.
- 脂本 extent / 回目 lists: publisher catalogue pages (e.g. nlcpress.com for 庚辰本).

### Phase 3 — Source verification (verify the truth)

A trusted domain is not proof — the claim must be **present in the source's content**.

9. **Open each source and locate the exact passage.** If you cannot retrieve it, you may not cite it (→ 待核实).
10. **Match claim ↔ source one-to-one.** If a source doesn't say what the draft claims, drop it or fix the claim.
11. **Check independence.** Two sources that copy one another count as ONE.
12. **Watch for ghost citations** (plausible title but no copy, quote not found, or only secondary mentions). AI- or memory-invented citations must be removed.
13. **High-risk claim types — verify verbatim or drop:** (i) character dialogue. (ii) usage statistics about an author/text. (iii) 批语归因 without 本 + 回. Worked examples: `docs/260808-corrections-by-citation.md`, `docs/260822-corrections-by-citation.md`.
14. **After writing, run the Phase 6 sweep** over the finished draft — that re-verification lives there (below), not twice.

### Phase 4 — Write / polish

15. Write in Simplified Chinese by default. Follow the user's section order. Mark each fact-supported sentence with a citation marker.
16. **Remove duplication** — each fact appears once per entry. Cut restatements across bio/analysis/intro/conclusion.
17. **Glosses (canonical rule).** Use precise terminology at first use. Annotate uncommon characters with pinyin as `字（pinyin）`, verified against a dictionary. Examples (with the correct reading): 菂（dì）、霁（jì）、诔（lěi）、绡（xiāo）、垄（lǒng）、鲛（jiāo）、縠（hú，一种绉纱）、忡（chōng）、姽婳（guǐ huà）、茜（qiàn）、麝（shè）、铰（jiǎo）、嬤（mó，旧读 mā）；classical-verse characters: 杕杜（dì dù）、蝃蝀（dì dōng）、隮（jī）、淇（qí）、滺滺（yōu yōu）、桧（guì）、睆（huàn）、菅（jiān）、澌（sī）、钏（chuàn）. **Never place a gloss inside a verbatim quote** — put it outside the closing quote (e.g. `……齐根铰下"（"铰"读 jiǎo）`). Don't annotate common characters.
18. **Structure.** Use the same heading level within a list-style article. Use no hierarchy labels (附录/补充). Put the conclusion last. Keep max heading depth at `###` (deeper → bold run-in labels, no 4.2.3 levels).
19. **Citations.** Inline `[¹]`, `[²]`… plus a 引用来源 / 参考文献 list (author, title, edition or publisher. For Wikisource, the text and edition. For web sites, the site, title, and access date). For web sources, give a **clickable URL** (e.g. the Wikisource 回 URL) as well as the access date. Quote verbatim exactly (chapter/回目 included).

### Phase 5 — Corrections doc (conditional)

20. If every claim verifies, **no corrections doc** is created.
21. Unverifiable / contradictory items go to `docs/YYMMDD-corrections-by-citation.md`, structured per `docs/260808-corrections-by-citation.md` (校核总表 / 已修正逐条明细 / 待核实清单 / 引用来源清单).
22. If the article already appears in an older corrections doc, cross-reference it (e.g. "260808 #35") instead of re-litigating. Keep the 处置分类 (①已修正 / ②待核实 / ③已核对) consistent.

### Phase 6 — Post-write self-review (defect-pattern sweep)

Re-read the finished draft once, hunting the recurring defects below. Fix each in place. Also confirm the re-verification step. Exact wording matches the cited edition (note variants, don't silently "correct"). Attribution (author/title/chapter) is right. Every inline marker `[ⁿ]` maps 1:1 to the 引用来源 list.

23. **Count your own numbers** — a "这 N 个字" claim must match the quote (real defect: "这八个字" used for an 11-character quote).
24. **Cite the 余论 / 背景** too — no uncited broad assertion (e.g. "戏子在清代是贱籍").
25. **Allusions need a source** (e.g. "千红一哭，万艳同悲" → 第五回"千红一窟""万艳同杯").
26. **State count/list ambiguity honestly** (e.g. the twelve actors — 菂官早亡、蕊官补入).
27. **Attribution & excerpt boundaries** — speaker/source exact (敕谕 vs 叙述语). Don't drop an opening clause that shifts the sense.
28. **Label interpretation** (索隐 / 自传 / 家国 / 象征) as the reader's, attributed. Assert verifiable textual facts as facts (e.g. 索隐派读《红楼梦》为康熙朝政治小说 — mark it as a reading).
29. **Pinyin** — reading verified (旧读 noted).
30. **Simplified-only sweep** — scan for Traditional/variant characters that slipped in (e.g. 嬤/嬷, 與/与, 歸/归).
31. **Verbatim-quote fidelity** — don't modernize pronouns (他→她) or alter punctuation (，→；) inside quotes.
32. **Edition / 回数 consistency** — keep 八十回 / 一百二十回 / 后四十回 statements consistent and non-contradictory (e.g. avoid "通行的《红楼梦》八十回，后四十回…").
33. **Citing a popular interpreter** — attribute to a named work (e.g. 蒋勋《蒋勋细说红楼梦》). Label the author's personal impressions distinctly.

## Genre: 物象细读 (object-as-lens close reading)

A recognized article type: take one object from the primary text (a medicine, garment, dish, colour) and read it as a lens on the whole work.

- Fix the object's exact chapter(s) and read the surrounding scene, not just one sentence.
- Trace it outward in rings — 物 → 人物 → 家族 → 时代/国 — each ring anchored to a verifiable textual detail.
- Frame the outermost ring as a reader's interpretation (attributed to a named school or scholar). Cite the work's own boundary statements. Pair the object with an echo elsewhere (草蛇灰线).

## 体例：原文引文块 + 多注（作者偏好的格式）

*这是**排版体例**，与第 2 条的"文风"不同：它只规定引文与注释怎样摆放，语言的声音仍归作者。*

Close-reading articles read best when each section leads with the primary text. A format the user likes:

- **Quote first, then read.** Open each section with a **blockquote of the original passage** (1–3 per section), then the reading. Keep other quotations inline.
- **脂批 in its own block.** Quote a 脂批 in a separate blockquote, placed after the original passage it comments on. Never put it in the same blockquote as the original text. Label it `脂批（edition，夹批/眉批/侧批，chapter）：…`.
- **多注.** Gloss colour names, garments and objects at **first occurrence** in parentheses (e.g. `石青（近乎黑的深蓝）`). Gloss each term once.
- **Never gloss inside a verbatim quote** — put the gloss outside the closing quote (canonical rule: Phase 4 item 17).
- **"注" ≠ length.** 多注 vs 少注 is about *how many annotations*, not how long the piece is: a long essay can be 少注, a short one 多注. Set the density by the target reader, not the word count.
- **Rare characters** (e.g. 䰖, 羓) — add a common rendering so they don't show as missing-glyph boxes.

## 色词 / 服饰考释 (colour & garment terms)

- **Where to verify 传统色名**: 中国丝绸博物馆"乾隆色谱"(reconstructed from the 乾隆 weaving-bureau dye records — 蓝八色、黄五色、红四色、紫五色、绿六色…; `chinasilkmuseum.com`); 汉典 `zdic.net` (词义 / 釉色); 故宫博物院 `dpm.org.cn`; referenced 维基百科 colour entries. **不采** 知乎 / 百度百科 / 博客.
- **Gloss vs claim.** A reader-help gloss ("蜜合色≈浅黄白") is editorial — **no citation needed**. A statement *about* a colour's status or use ("石青是清代官服主色") is a **claim** — cite it, or mark 待核实.
- **Widely-cited ≠ verifiable.** 清·李斗《扬州画舫录》"浅黄白色曰蜜合" is quoted everywhere for 蜜合色, but the book is **not on 维基文库** — without checking the text itself, mark 待核实. 传统色名 are fuzzy; some (e.g. 靠色) have no reliable definition — don't invent one.
- **《红楼梦》fact-check examples** (worked examples, not general rules): 第五十回 reads 仇十洲《**双艳图**》, not 艳雪图; 黛玉 is **not** "通篇不写衣饰" (第八回、第四十九回 both have real outfit descriptions) — avoid absolutes. Reading a person's colour as a "code" is a *reader's interpretation* — label it (item 28).

## Repo conventions

See `AGENTS.md` — filenames `docs/<YYMMDD>-<slug>.md`, images `imgs/<YYMMDD>-<slug>.<ext>` referenced as `../imgs/<file>`, README kept in sync, no nested `.git`, corrections doc only when there is something to record.

**Publishing side-steps** (separate skills): 繁体孪生（zh-hans → zh-hant）见 `simplified-to-traditional`. 配图 / 信息图 见 `custom-infographic`.

## Verification checklist

- [ ] Thought-flow preserved — same order, points, conclusions.
- [ ] Claims sourced (≥2 independent where contested, primary text preferred). Chapter attributions verified. 《红楼梦》edition named and 脂批 within ch1–80.
- [ ] 《红楼梦》: 脂批 checked for each quoted passage. Where one exists, it is quoted with its edition label.
- [ ] Sources opened and located. Independent. No ghost citations. High-risk quotes found verbatim.
- [ ] No fact stated twice within an entry. Conclusion not restating the intro.
- [ ] Citation markers map 1:1 to 引用来源 entries.
- [ ] Interpretation labelled. Textual facts asserted as facts.
- [ ] No untrusted-source claim used as evidence. Unverifiable items in the corrections doc.
- [ ] Pinyin verified (旧读 noted). Simplified-only sweep done. Quotes unaltered. Every gloss sits outside the quote it explains.
- [ ] 回数/版本 consistent. Popular-interpreter views attributed. Personal impressions labelled.
- [ ] Close-reading 体例: each section opens with a blockquote of the original. Colour/garment terms glossed at first use.
- [ ] Filename `YYMMDD-slug`. Images `../imgs/`. README in sync. Stated word count matches actual CJK count (`python3 -c "import re;print(len(re.findall(r'[\u4e00-\u9fff]',open('FILE').read())))"`).
- [ ] Nothing committed unless the user explicitly asks.

## Error handling

- **Draft conflicts with sources** → show the discrepancy and both sides. Propose the fix. Wait for approval.
- **Sources conflict, neither clearly right** → record both under 待核实. Present the conflict with evidence.
- **Source paywalled/unavailable** → use the other independent source. Note the gap.
- **Ambiguous structure** → ask. Don't guess the outline.
- **No reliable source** → 待核实. Don't assert. Tell the user.
