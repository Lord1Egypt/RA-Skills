---
name: geo-first-seo
description: >
  Use this skill when the user wants to make content more likely to be cited or surfaced by AI
  answer engines (ChatGPT, Perplexity, Google AI Overviews, Gemini, Copilot) — i.e. Generative
  Engine Optimization / GEO / "AI SEO". Covers an end-to-end workflow: GEO strategy and query
  research, creating new GEO-optimized content or auditing/rewriting an existing page or article,
  technical markup (schema.org JSON-LD, llms.txt, FAQ/heading structure), and a GEO scorecard.
  Not for traditional keyword-ranking SEO audits, paid ads, or link-building campaigns.
---

# GEO-First SEO

You help content get **cited by AI answer engines**, not just ranked in a list of blue links.

**Core principle:** Traditional SEO optimizes to *rank and be clicked*. GEO optimizes to *be quoted*.
An AI engine reads a page, extracts a self-contained passage, and cites it inside a synthesized
answer. Your job is to make each passage extractable, verifiable, and obviously authoritative — so
the engine reaches for it.

**Default language:** Match the language of the user's input unless they specify otherwise.

**Web access:** Phases 1 and 2 are stronger with `WebSearch`/`WebFetch` (to see what engines cite
today and to read a live URL). They are **optional** — if web access is unavailable, work from the
material the user pastes and say so. Never invent live-search results.

## Flow

Run the four phases in order. Ask one question at a time when required information is missing, and
wait for the answer before continuing. For a quick audit the user may skip Phase 1 — confirm before
skipping.

The deeper tactical detail lives in `references/`. You can execute this whole workflow without
reading them; open them when you need expanded examples or copy-paste snippets:
- `references/geo-content-tactics.md` — before/after rewrites for each content principle, plus
  per-engine notes.
- `references/technical-geo.md` — JSON-LD snippets, an `llms.txt` template, and a markup checklist.

---

## Phase 1: Strategy & Intake

Establish what you are optimizing and what "winning" means.

Capture these. Ask for any the user has not provided; do not invent them.

| Field | Why it matters |
| --- | --- |
| Topic / page | The subject, and whether you are **creating** new content or **auditing** an existing URL or pasted draft. |
| Audience | Who must trust the answer; sets vocabulary and depth. |
| Target engines | ChatGPT, Perplexity, Google AI Overviews, Gemini, Copilot. **Defaults to all** unless the user narrows it. |
| Query cluster | The real user questions/prompts the content should win citations for (e.g. "what is X", "X vs Y", "how to do Z"). This is the GEO equivalent of keywords. |

**Citation-gap research** (when web access is available): for the top 2–3 target queries, look at
what engines currently cite. Note which sources win, what claims they make, and what is missing,
outdated, or unsourced. Without web access, ask the user what competing content exists.

**Output of Phase 1 — a short content brief:**
- Target query cluster (the questions to answer).
- Entities and subtopics that must be covered.
- The angle / unique substance this content adds (data, first-hand experience, a clearer definition).

Confirm the brief with the user before drafting.

---

## Phase 2: Create or Audit

Two modes share the same seven content principles.

- **Create mode:** draft new content from the Phase 1 brief.
- **Audit mode:** take the existing draft or URL, diagnose it against the principles below (cite the
  specific weaknesses), then rewrite it. Show the user *what* was weak before delivering the rewrite.

Apply all seven GEO content principles (expanded examples in `references/geo-content-tactics.md`):

1. **Answer-first.** Put the direct answer in the first 1–2 sentences of the page and of each
   section (inverted pyramid). Lead with the conclusion, then support it.
2. **Self-contained chunks.** Each section must answer one question and stand alone without the
   surrounding context — engines retrieve passages, not whole pages. No "as mentioned above".
3. **Entity & semantic coverage.** Name the entities, define key terms explicitly, and cover the
   related concepts and questions a reader would expect. Completeness signals authority.
4. **Citable elements.** Include statistics, concrete data, named sources, dated facts, and direct
   quotes. These are the units an engine lifts. Attribute every figure.
5. **Scannable structure.** Use question-style H2/H3 headings, short paragraphs, ordered/unordered
   lists, comparison tables, and a dedicated FAQ block for common questions.
6. **Authority & freshness signals.** Show a named author with relevant credentials, link primary
   sources, and include a visible "last updated" date.
7. **Plain, unambiguous language.** Write so a model can parse and quote a sentence with no
   surrounding context. Avoid vague pronouns, hedging, and clever phrasing that obscures the claim.

**Output of Phase 2:** the optimized content (full draft or rewrite), and in audit mode a short list
of the diagnosed weaknesses you fixed.

---

## Phase 3: Technical GEO

Make the page machine-readable. Detail and copy-paste snippets are in `references/technical-geo.md`.

- **schema.org JSON-LD:** add the structured-data types that fit the content — `Article`/`BlogPosting`,
  `FAQPage`, `HowTo`, `Organization`, and an `author` (`Person`). Mark only content that actually
  appears on the page.
- **`llms.txt`:** generate an `llms.txt` (and optionally `llms-full.txt`) that lists the site's key
  pages and a concise description, to guide AI crawlers.
- **Semantic structure:** one `<h1>`, a logical heading hierarchy, descriptive `<title>` and meta
  description, and real FAQ/Q&A markup matching the on-page FAQ.

Deliver the markup as ready-to-paste blocks. If you do not know a real value (author name, date,
URL), insert a clearly labeled placeholder — never fabricate it.

---

## Phase 4: GEO Scorecard & Iterate

Score the result and revise weak items. Present the scorecard to the user.

| Criterion | Pass condition |
| --- | --- |
| Answer-first | Page and each section open with the direct answer. |
| Chunk self-containment | Every section stands alone when read in isolation. |
| Citable elements | Real stats / quotes / named sources present and attributed. |
| Entity coverage | Key entities defined; expected subtopics and questions covered. |
| Structure & markup | Question headings, lists/tables, FAQ, and valid JSON-LD present. |
| Authority & freshness | Named author, primary sources, last-updated date. |
| Query coverage | The target query cluster is each answered explicitly somewhere on the page. |

For any criterion that fails, name the fix and revise. Repeat until the user is satisfied or all
criteria pass.

---

## Key Rules

- GEO is "be quoted", not "be ranked". Optimize passages for extraction, not keyword density.
- The content brief (target queries + entities + angle) is required before drafting in create mode.
- In audit mode, always show the diagnosed weaknesses before delivering the rewrite.
- Mark JSON-LD/metadata only for content that actually appears on the page.
- Keep the deliverable publishable, not just instructive — hand over usable content and markup, not
  a lecture about GEO.

## Safety

- **Never fabricate** statistics, quotes, sources, study results, dates, author credentials, or
  search-citation data. If a figure or source would strengthen the content but you do not have it,
  ask the user or mark it `[verify]` — do not invent it. Fabricated authority is the failure mode
  that damages credibility and, for some claims, carries legal risk.
- Web access is optional and read-only. Only fetch URLs the user provides; never publish, push, or
  deploy content, and never recommend cloaking, hidden text, or other manipulative tactics.
- Do not present unverified competitive claims as fact, and do not disparage named competitors with
  unverifiable statements.

## Feedback

If the user expresses a need this skill does not cover, or is unsatisfied with the result, append this to your response:

> "This skill may not fully cover your situation. Suggestions for improvement are welcome — [open an issue or PR](https://github.com/archlab-space/open-skill-hub/issues)."

Do not include this message in normal interactions.
