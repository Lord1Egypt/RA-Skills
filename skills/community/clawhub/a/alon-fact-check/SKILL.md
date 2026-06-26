---
name: alon-fact-check
description: USE WHEN user wants to verify factual claims from text or a URL with authoritative sources, or trace a claim back to its original or official source URL. Extracts explicit verifiable claims, searches primary or professional fact-checking sources, and returns a structured credibility report or source trace with links. Do not use for opinion editing, general research summaries, or advice generation.
version: 0.1.2
tags:
  - research
  - fact-checking
  - verification
  - web
trigger: /fact-check
---

# Alon Fact Check Skill

Verify the credibility of information by finding authoritative sources with links and credibility scores.

## Input

The user provides either:
- **Text**: A claim, paragraph, or article content to fact-check
- **URL**: A link to a web page whose content needs fact-checking
- **Source tracing request**: A claim or quote where the user wants the original, official, or earliest reliable source URL

## Workflow

### Step 1: Parse Input

- If input is a URL: use the host's available web reader, browser, or search tools to fetch readable page content. If the page cannot be accessed, ask the user to paste the relevant text.
- If input is text: use directly
- If the user asks to find the original source, official source, primary URL, earliest source, citation source, or where a claim came from, use **Source Tracing Mode** before the normal fact-check report.

### Source Tracing Mode

Use this mode when the user's main goal is to locate the source of a claim rather than score the whole source's reliability. Example requests include "find the official source", "trace this claim", "where did this number come from", "original URL", "官方出处", "原始出处", "溯源", "源头", or "出处链接".

**Goal**:
- Find the most authoritative original or official URL that directly supports the exact claim.
- Distinguish between the original source, official confirmation, secondary reporting, and copied/aggregated mentions.
- Include useful secondary mentions such as articles, social posts, newsletters, or reposts when they help explain where the user may have seen the claim or how the claim spread.
- Preserve the exact claim, including amounts, dates, eligibility conditions, product names, scope, and quoted wording.
- If no original source is found, return the best available source and clearly say what is missing.

**Search strategy**:
- Start with exact-phrase searches for the distinctive words, numbers, product names, and quoted fragments in the claim.
- Search likely official domains before general media when the entities are known. Examples: `site:cloudflare.com`, `site:stripe.com`, `site:support.stripe.com`, official docs, press releases, support pages, filings, or original research pages.
- Use reverse-citation tracing: when a secondary article links or names a source, open that source and continue until the earliest official or primary source is reached.
- For monetary amounts, eligibility promises, product terms, discounts, credits, limits, dates, or partner benefits, prefer official terms, support pages, announcement blogs, partner pages, or archived official pages over media coverage.
- Keep a short source chain: user-provided claim or source -> inspected secondary mention if relevant -> official/original source.
- Do not call a secondary article, social post, or repost the "source", "origin", or "传播源头" unless the user provided it as their source or the searched evidence establishes it as the earliest known source. If it was merely found during search, label it as `found secondary mention`, `传播节点`, or `用户可能看到的传播节点`.
- When listing inspected secondary mentions or propagation nodes, include URLs for a few representative examples so the user can open and compare how the claim is spreading. Prefer 1-3 typical links over a long dump.

**Classification**:
- `Official original source`: first-party page from the relevant organization that directly states the claim.
- `Official confirmation`: first-party page that confirms the claim but may not be the earliest source.
- `Primary non-official source`: original paper, filing, dataset, court record, transcript, or direct artifact.
- `Secondary source`: article, blog, newsletter, social post, or aggregator that reports the claim but is not the source of record.
- `Found secondary mention`: a searched and inspected article, post, newsletter, or repost that carries the claim but is not proven to be the user's source or the earliest source.
- `Not found`: no source directly supporting the exact claim was found.

**Trace confidence**:
- `High`: an official, primary, or first-party source directly supports, contradicts, or narrows the exact claim.
- `Medium`: a reliable secondary source is found, or an official/primary source supports only part of the claim.
- `Low`: only reposts, social posts, vague mentions, inaccessible pages, or broken source chains are found.
- Trace confidence describes the reliability of the source chain, not the claim's truthfulness. If a fact-check verdict is also provided, keep claim credibility separate as `Credibility`.

**Output format**:

```
## Source Trace

**Claim**: [exact claim being traced]
**Best Source**: [title] [Official original source / Official confirmation / Primary non-official source / Secondary source / Found secondary mention / Not found]
URL
**Why This Source**: [1-2 sentences explaining why it is the best source and whether it directly states the claim]
**Source Chain**:
- [user-provided claim or source if available]
- [found secondary mention or intermediate source if relevant, with label and URL]
- [official/original source]
**Trace Confidence**: High / Medium / Low
**Notes**: [missing conditions, ambiguity, archive/access limitations, or whether the source only partially supports the claim]
```

If the user also asks whether the claim is true, continue into the normal fact-check workflow after the source trace and include a compact verdict.

### Step 2: Understand Source Content

Before searching, briefly understand what the source says.

- For URL input: identify the page title, publisher/site, visible publication or update date when available, content type, and the article's main point.
- For long pasted text, article-like text, transcripts, or multi-paragraph input: write a 1-3 sentence content summary before claim extraction.
- The summary must state the source's core thesis or stance, not just list topics covered. Prefer this shape: "The source argues/claims that [core point], using [main evidence/examples], while [important caveat or framing if present]."
- For short text containing only one or a few direct claims: skip the summary unless it helps clarify ambiguity.
- In the final report, include `Source Summary` for URL input and `Content Summary` for long pasted text. Omit this field for short direct claims.
- Do not treat the URL host's reputation as evidence that the claims are true. The summary only establishes what is being checked.
- Keep article claims separate from later evidence found during verification.

### Step 3: Extract Verifiable Claims

From the content, identify **1-5 distinct, verifiable factual claims**. For long articles, default to the **3 most central or consequential claims** unless the user asks for exhaustive checking. Do not split, infer, or invent claims just to reach a target count. A good claim:

- Contains a specific subject + specific assertion (e.g. "WHO classified aspartame as possibly carcinogenic in 2023")
- Is objectively checkable (not opinions, predictions, or value judgments)
- Is non-trivial (skip common knowledge like "water boils at 100°C")

Filter out: subjective opinions, vague statements, rhetorical questions, common knowledge.
Do NOT extract implicit/derived claims — only claims explicitly stated in the source text.
For URL or long-text input, base the claims on the source/content summary and original text, not on external search results.

For comparative, ranking, or status claims, preserve the comparison metric in the extracted claim. Do not collapse ambiguous wording such as "largest", "leading", "big shareholder", "better", "top", "overtook", or "first" into a single interpretation before verification.

### Step 4: Search and Verify Each Claim

For each claim, perform searches in the order that fits the claim type. Use the host's available search and browsing tools. Open and inspect sources before citing them; do not cite a search result snippet that was not verified.

**Round 1 — Choose the right first source**

- For medical, scientific, legal, financial, policy, or statistics claims: start with primary or domain-authoritative sources.
- For viral rumors, social media claims, public controversies, manipulated images/videos, and political talking points: start with professional fact-checking sites, then verify against primary sources where possible.
- For time-sensitive claims involving "latest", "currently", "this year", "approved", "announced", prices, policies, statistics, or rules: verify both the source publication date and the event/effective date.

Chinese fact-checking / rumor-checking sites:
- `piyao.org.cn` (中国互联网联合辟谣平台)
- `thepaper.cn` (澎湃明查)

Chinese domain-supporting sources:
- `dxy.com` (丁香医生 — medical and health explanations)
- `guokr.com` (果壳 — science communication)

English fact-checking sites:
- `snopes.com`
- `reuters.com/fact-check`
- `factcheck.afp.com`
- `fullfact.org`
- `politifact.com`
- `apnews.com`

**Round 2 — Domain-specific authoritative sources (score 4-5)**

Based on the claim's topic, search domain-specific authoritative databases:

| Domain | Priority Sources | site: filter |
|--------|-----------------|-------------|
| Health/Medical | PubMed (peer-reviewed), Cochrane Library, WHO, CDC | `pubmed.ncbi.nlm.nih.gov`, `who.int`, `cdc.gov` |
| Science/Tech | Nature, Science, peer-reviewed journals | `nature.com`, `science.org` |
| Government/Policy | Official government sites | `.gov` domains |
| Finance/Economics | Fed, IMF, World Bank, SEC filings | `federalreserve.gov`, `imf.org`, `worldbank.org` |
| Statistics/Data | Official statistical bureaus | `stats.gov.cn`, `census.gov`, `oecd.org` |

**IMPORTANT**: arXiv is a preprint repository — papers there are NOT peer-reviewed. Cite arXiv only when no peer-reviewed version exists, and always note "preprint, not peer-reviewed".

**Round 3 — General authoritative search**

If targeted searches do not settle the claim, use general authoritative search. Score results by source type:

| Source Type | Score | Examples |
|-------------|-------|---------|
| Official/Government (.gov) | 5 | who.int, cdc.gov, gov.cn |
| Peer-reviewed journal | 5 | nature.com, science.org, PubMed-indexed journals |
| Major news wire | 4 | reuters.com, apnews.com, xinhua.net |
| Mainstream media | 3 | bbc.com, nyt.com, caixin.com |
| Industry authority/Encyclopedia | 2-3 | wikipedia.org, industry associations |
| Social media/Blogs/Forums | 1 | twitter.com, weibo.com, zhihu.com, reddit.com |

**Credibility caps**:
- No opened/verifiable source: ❓ Unverified, max 1/5
- Only social media, blogs, or forums: max 2/5
- Only mainstream media or encyclopedia sources: max 3/5
- Professional fact-checking source without inspected primary evidence: max 4/5
- At least one relevant primary source, official dataset, peer-reviewed source, or professional fact-check that directly inspects primary evidence: max 5/5
- Do not let cross-validation override these caps

**Cross-validation bonus**: If a claim is supported by ≥2 independent authoritative sources from different source types, upgrade its credibility by at most one level within the caps above.

**Search planning**:
- Before searching, map each claim to its preferred source type and 1-2 focused search queries.
- Include at least one contradiction-oriented query for uncertain or controversial claims, using terms such as `false`, `debunked`, `misleading`, `retracted`, `辟谣`, `误导`, or `撤回`.
- Search for the highest-risk or most consequential claim first when there are 4-5 claims.
- Stop searching once the verdict is well-supported within the source caps.

**Comparative, ranking, and status claims**:
- Before judging claims about relative position or replacement (for example, "largest", "top", "leading", "big shareholder", "overtook", "no longer", "best", or "first"), identify the comparison metric.
- Do not conflate related metrics. Examples: committed investment vs paid-in investment, ownership percentage vs voting power, board seat vs control, revenue vs profit, market share vs users, benchmark score vs real-world performance, nominal value vs inflation-adjusted value.
- If the user's wording is ambiguous, evaluate the plausible interpretations separately when possible. State which interpretation is true, false, misleading, or unverified.
- If the metric cannot be verified from reliable sources, mark the relative-status claim as ❓ Unverified or ⚠️ Misleading rather than forcing a single conclusion.

**High-stakes topics**:
- For medical, legal, financial, public safety, or civic/policy claims, prioritize official, regulatory, primary, or peer-reviewed sources before media summaries.
- Do not provide personalized medical, legal, financial, or safety advice. State only what the evidence supports about the claim.

**Cost control**:
- ≤3 claims: 2 search rounds per claim
- 4-5 claims: full search for top claims, simplified for minor ones
- Total searches: keep under 15

### Step 5: Analyze and Classify

For each claim, determine one of:

| Verdict | Meaning |
|---------|---------|
| ✅ True | Supported by multiple authoritative sources |
| ⚠️ Misleading | Contains a kernel of truth but is exaggerated, out of context, or omits key nuance |
| ❌ False | Contradicted by authoritative sources |
| ❓ Unverified | Insufficient evidence found either way |

### Step 6: Output Report

**Output format — conclusion first, then structured details:**

Use the same language as the final answer for all headings and field labels in the template.
For longer inputs, the report must include both:
- `Source Summary` for URLs or `Content Summary` for long pasted text: what the source text says, before external verification.
- `Summary`: what the verification found, after checking evidence.

**Summary quality**:
- The top `Summary` must be conclusion-first but not shallow. Include the decisive qualifiers that help the user understand the verdict.
- Across all domains, include the condition, scope, baseline, comparison, time frame, magnitude, mechanism, or exception when those details determine what is actually true.
- Prefer concrete quantities over vague qualifiers. If evidence supports it, state approximate counts, percentages, absolute changes, risk ratios, prices, dates, sample sizes, rates, thresholds, or other decision-relevant ranges. Avoid vague wording such as "certain amount", "large increase", "significant effect", or "some risk" when a defensible quantity is available.
- If sources use different units, baselines, or ranges, report the most decision-relevant range and say it is approximate.
- The goal is not technical detail for its own sake. The goal is to make clear: what exactly is true, under what conditions, compared with what baseline, by roughly how much, and what exception changes the answer.
- For misleading claims, explicitly state the narrower true version of the claim.
- For ambiguous comparative/status claims, state the metric-specific version that is true. Example: "X is larger by ownership percentage, but Y remains a major investor by committed capital" rather than simply "X is the big shareholder."
- If the summary would lose the key nuance when shortened to one sentence, use 2-3 concise sentences.

```
## Fact-Check Report

**Source**: [article title or first 20 chars of input]
**Source Summary / Content Summary**: [1-3 sentence summary of the source's core thesis/stance, main evidence/examples, and important caveat or framing; omit for short direct claims]
**Overall Assessment**: ★★★★☆ (4/5)
**Summary**: [1-3 sentence overall conclusion with key qualifiers such as condition, scope, baseline, comparison, time frame, magnitude, mechanism, or exception when relevant]
**Source Note**: Brackets after each source describe source type or why it is credible. They are not citation numbers and do not replace claim credibility.

⚠️ [N] of [M] claims need attention (misleading/false/unverified)

---

### Claim #1
**Claim**: [the original claim]
**Verdict**: ✅ True
**Credibility**: ★★★★★ (5/5)
**Sources**:
  - WHO/IARC official announcement [official health agency]
    https://www.iarc.who.int/...
  - Reuters coverage [major news wire]
    https://www.reuters.com/...

---

### Claim #2
**Claim**: [the original claim]
**Verdict**: ⚠️ Misleading
**Credibility**: ★★☆☆☆ (2/5)
**Note**: [brief explanation of what's misleading]
**Sources**:
  - Snopes fact-check — "[title]" [professional fact-checking org]
    https://www.snopes.com/...
  - BBC analysis [mainstream media context]
    https://www.bbc.com/...
```

For Chinese output, use Chinese labels and compact count wording:
- Prefer `⚠️ 1/1 条声明需要关注` over mixed-language text like `1 of 1 条陈述需要关注`.
- Prefer `声明` consistently. Do not alternate between `声明` and `陈述`.

For a single short claim, keep the report compact:
- Omit `Source Summary / Content Summary`.
- Use a compact but complete `Summary`; do not omit decisive qualifiers such as dose, exposure, subtype, magnitude, or exception.
- Use exactly one `Claim #1` section.
- Include 2-3 sources maximum.

**Overall assessment calculation**:
- Start from the average claim credibility.
- If any claim is ❌ False, cap overall assessment at 2/5.
- If any claim is ⚠️ Misleading or ❓ Unverified, cap overall assessment at 4/5.
- If most claims are unverified, overall assessment should be ❓ Unverified even if one claim is true.

**Report assembly**:
- Assemble the final report once, after all checked claims are complete. Do not stream, paste, or patch partial claim sections into the final answer.
- Before sending, compare the final report against the checked claim list. If any duplicate section, missing claim text, repeated verdict line, source mismatch, or malformed source line appears, rewrite the final report cleanly from the checked claim list.
- Prefer a shorter clean report over a longer report that risks duplicated sections or copied paragraphs.

## CRITICAL Output Rules

- **NEVER repeat any content**. Each section appears exactly ONCE. No duplicated tables, sources, or paragraphs.
- **Final self-check before sending**: verify claim numbering is sequential, no section is duplicated, every source belongs to the claim it is listed under, and there are no dangling or malformed source lines.
- **Each source must be a separate bullet with its URL on the next line**. Never put two sources on the same visual line, and never let a URL run into the next bullet.
- **Keep each claim section under 150 words** excluding sources. Brief explanation + verdict only. No long essays.
- **No "practical advice" or "tips" sections**. This is a fact-checking tool, not a lifestyle guide.
- **No ASCII tables unless essential**. Prefer simple lists or inline descriptions.
- **Each claim gets at most 2-3 sources**. Pick the most authoritative, don't dump everything you found.
- **Sources must directly support or contradict the specific claim**. Do not reuse a source from another claim unless it directly addresses the current claim.
- **Explain source labels once near the top**. Source labels describe source type or why it is credible; they are not citation numbers and are separate from claim credibility.
- **Include dates when they matter**. For time-sensitive claims, include the source publication date or event/effective date in the note or source label.
- **For each source, briefly explain WHY it's credible** in brackets. Examples:
  - `[PubMed — peer-reviewed medical journal]`
  - `[WHO official — UN health agency]`
  - `[Reuters — major news wire]`
  - `[Snopes — professional fact-checking org]`
  - `[arXiv — preprint, NOT peer-reviewed]`

## Language Rules

- Output language matches the input language (Chinese input → Chinese output, English → English)
- Headings, field labels, verdict names, and notes must also match the output language
- Claim extraction and search queries should match the source language
- For Chinese claims, search in Chinese first, then supplement with English searches if needed
- Always include direct links to sources

## Important Notes

- Never fabricate URLs or search results. Only cite sources actually found during verification
- If a search returns no useful results for a claim, mark it as ❓ Unverified rather than guessing
- Distinguish clearly between correlation and causation in scientific claims
- Pay attention to dates — a source from 2020 may not be current for a claim about 2024
- Watch for claim drift: verify the exact claim stated, not a weaker, stronger, or adjacent claim that is easier to source
- If a source quotes another source for the key evidence, try to inspect the original source before citing it as decisive
- If the input contains no verifiable claims (all opinions/subjective), say so directly instead of forcing an analysis

## Follow-up Handling

If the user asks whether the report is complete (for example, "没了？", "anything else?", or "is that all?"):
- First answer directly whether the core fact-check is complete.
- Then provide at most 3-4 concise supplemental data points only if they materially clarify the verdict.
- Do not add new unsupported claims, advice, or a second full report unless the user asks for deeper follow-up.

## About Alon

Public skill from Alon's real daily workflows.

- GitHub: https://github.com/alondotsh
- ClawHub: https://clawhub.ai/u/alondotsh
- X: https://x.com/alondotsh
- WeChat Official Account: alondotsh
