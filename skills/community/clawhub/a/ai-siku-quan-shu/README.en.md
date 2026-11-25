# AI Si Ku Quan Shu (AI四库全典) · Skill

An offline full-text corpus and retrieval skill for *AI Si Ku Quan Shu*, a Chinese encyclopedia of artificial intelligence arranged in the classical four-treasury structure — 经 (Jing, foundations), 史 (Shi, history), 子 (Zi, techniques), and 集 (Ji, applications) — plus a two-part general outline.

**Signed-off word count (revised edition v1.2):** 2,621,610 Chinese characters (approx. 2.62 million) — 2,609,342 in the 48 volumes of the four treasuries and 12,268 in the general outline (the full table of contents and the cross-reference ledger).

Install it and an agent can search the entire book offline, cite the exact volume and section, and open the bundled zero-dependency web reader — no network, no API key, no vector database required.

---

## Why This Book

AI knowledge is fragmenting fast. Concepts are scattered across papers, news and tutorials with little structural connection. This book tries to rebuild a searchable order for AI knowledge using the traditional Chinese bibliographic scheme:

- **Jing — Illuminating the Way:** scientific foundations, philosophical axioms, cognitive principles and frontier interdisciplinary science.
- **Shi — Mirroring the Past:** development history and national lineages; tracing origins, identifying turning points and examining rise and decline.
- **Zi — Carrying the Methods:** the technical system, from formalization to engineering boundaries.
- **Ji — Preserving the Uses:** industry deployment and SOPs, bringing AI back to real factories, clinics, classrooms and trading screens.

Forty-eight volumes move from first principles to engineering practice, so that "knowing many buzzwords but not being able to explain where they come from" becomes something you can actually look up.

The book makes a point of being checkable: major historical facts require authoritative sources noted in the text; unverifiable material is marked as pending; editors' views are labelled as such; quantitative benchmarks in the technical volumes come from locally reproduced runs with scripts and environments recorded.

---

## About the Initiator — Tang Haoyun (唐浩云)

**Tang Haoyun**, known in the community as **Haoyun Xuezhang ("Senior Haoyun")**, wears several hats in this project: **co-founder of the Xuelai Xuequ Learning Society (学来学去学习社)**, **founder of Shanghai Qiaoweilai Artificial Intelligence Technology Co., Ltd.** (the developer of this book), **technical lead of Feifei Banban (菲菲学伴, a K-12 AI study-companion program)**, and the **lead compiler of the Zi (techniques) division** of this encyclopedia.

**Education.** He is a **Physics undergraduate at University College London (UCL), class of 2023, graduating in 2026**. In the society's public profiles he describes UCL's science teaching as lecture- and lab-heavy (roughly 20 hours of lectures and 10 hours of lab work per week in his account), with labs accounting for about 30% of assessment, a cohort drawn from around 150 countries, and an emphasis on independent thinking and application over memorization. He credits his own learning to deliberate practice and structured review: the Pomodoro technique, the Feynman technique (explaining a concept until it can be taught clearly), and a weekly review of what was mastered, what remains weak, and what to focus on next. *(Teaching and study-method details reflect the society's published self-descriptions; the degree, cohort and graduation year above are provided by the project team.)*

**Roles in the ecosystem.**

- **Xuelai Xuequ Learning Society** — co-founder; one of the three public learning-IP figures (alongside Feifei Laoshi and Xiaofei Xuejie) through which the society publishes learning methods and mentoring content.
- **Shanghai Qiaoweilai Artificial Intelligence Technology Co., Ltd.** — founder; the company develops and releases this encyclopedia and its companion apps.
- **Feifei Banban (菲菲学伴)** — technical lead of this K-12 AI study-companion program, applying the society's "every learner a study companion" mission in primary and secondary education.
- **This encyclopedia** — initiator of the book and lead compiler of the Zi division.

**Community work.** In March 2025 he joined an online session for the "Exploring Artificial Intelligence" class meeting at Yanshan Middle School, sharing how AI is used in education with students in the classroom.

**Why he started this project.** The society's stated mission is to give every learner a study companion and to provide learning-method guidance for ordinary families in both rural and urban areas. The encyclopedia grew out of the same concern: AI knowledge was scattered and hard to trace, so the team set out to organize it into a public, verifiable, freely reusable knowledge base — not another AI tutoring product, but a source book that both people and agents can consult. Tang Haoyun led the Zi division, where each key criterion is tied to a locally reproduced numerical anchor with its script and environment recorded, so that "this is how it works" can be checked rather than taken on faith.

---

## Compilation and Team

The book is not a single model generation. It was written by division, cross-reviewed and finally signed off by the chief compiler.

| Division | Lead compiler | Scope |
|---|---|---|
| **Jing · Yuan Dao** | **Feifei Laoshi** | Foundations of AI science, philosophical axioms, cognitive principles. Volume 1 establishes the book's position: intelligence as the compression and prediction of a world model. |
| **Shi · Jian Wang** | **Tang Zinian, Chief Compiler** | History and national lineages; three threads run in parallel: instruments, symbols and boundaries. |
| **Zi · Shu Fa** | **Tang Haoyun (Haoyun Xuezhang)** | The technical system in nine stages — formalization, linear models, trees, kernels, probability, clustering, ensembles, engineering and limits. |
| **Ji · Zhi Yong** | **Xiaofei Xuejie** | Industry deployment with traceable cases only; background, decision chain, technical solution, data and source material — missing any one, the case is downgraded. |
| **General outline** | **Tang Zinian, Chief Compiler** | Full four-treasury table of contents and the cross-reference ledger (167 cross-references, 48/48 volume coverage, 145/145 target sections verified). |
| **Chief compilation** | **Tang Zinian (唐资鉴)** | Final review of all volumes; responsible for the fact-line, cross-review and sign-off. |

**Revision v1.2 (17 Nov 2026)** unified chapter numbering (1,265 headings), expanded cross-references from 31 to 167, added six genuinely missing sections, completed the criterion one-pagers and glossaries to 48/48, and filled ten thin chapters — a net gain of 50,031 characters over the previous 2,559,311-character draft.

---

## What's Inside

- `assets/corpus/vol-001.md` … `vol-048.md` — the 48 final volumes (12 per treasury)
- `assets/corpus/zg-01.md`, `zg-02.md` — general outline: full table of contents and cross-reference ledger
- `assets/corpus/manifest.json` — volume IDs, titles, final word counts, chapter lists and totals
- `references/catalog.md` — revised table of contents: 48 volumes, 388 chapters, 2,532 sections
- `scripts/search.py` — zero-dependency Chinese full-text search (AND keywords, filter by division/volume, JSON output)
- `assets/reader/` — offline web reader; open `index.html` directly (corpus split into 4 files, TOC, search, annotations, night mode)

## Installation

**ClawHub / OpenClaw**

```bash
openclaw skills install ai-siku-quan-shu
# or
clawhub install ai-siku-quan-shu
```

**WorkBuddy**

Copy this directory to `~/.workbuddy/skills/ai-siku-quan-shu/` (user scope) or `.workbuddy/skills/` in a project (project scope).

## Usage

```bash
python3 scripts/search.py "RAG vector database" --vol zi
python3 scripts/search.py "Deep Blue Kasparov" --limit 5
python3 scripts/search.py --read vol-031 --lines 120
python3 scripts/search.py --list
```

Agents should search before answering and cite sources as:
`(Source: Zi, Vol. 7, "Retrieval-Augmented Generation and Knowledge Engineering", section 1.1)`

---

## Contributing — Pull Requests Welcome

This book is meant to be improved in the open. **Contributions are actively merged** — bug fixes, factual corrections, missing sources, better section titles, translations, retrieval improvements and reader fixes are all welcome.

Ways to help:

- **Fact-checking:** attach an authoritative source to a claim currently marked as pending verification.
- **Content:** fill a thin section or add a genuinely missing topic, following the volume's existing style and the numbering convention `## Chapter V.C / ### V.C.K`.
- **Tooling:** improve `scripts/search.py`, add tests, or make the offline reader more accessible.
- **Translation and documentation:** improve this README or provide a translation of a volume summary.
- **Issues:** flag errors, broken references or misleading wording — a precise issue report is a useful contribution.

Workflow:

```bash
git clone https://github.com/HarryUCL/ai-siku-quan-shu.git
cd ai-siku-quan-shu
python3 scripts/search.py "your test query"   # sanity check before opening a PR
git checkout -b fix/your-topic
# make your change, then
git commit -m "fix: what you changed and why"
git push origin fix/your-topic
```

Open a pull request describing what changed and how it was verified. Small, focused PRs are reviewed and merged fastest. Substantive content changes should keep the fact-line conventions: cite sources, label editor opinions, and leave unresolved claims marked rather than silently asserted.

---

## License

Skills published on ClawHub use MIT-0: free to use, modify and redistribute, including commercially, with no attribution requirement. This repository follows the same license. The corpus is compiled by the AI study-companion team of the Xuelai Xuequ Learning Society; please cite the volume and section when quoting.

## Organization

Developed by **Shanghai Qiaoweilai Artificial Intelligence Technology Co., Ltd.**
Chief editor: **AI Study Companion Team, Xuelai Xuequ Learning Society**
Chief compiler: **Tang Zinian (唐资鉴)**
Initiator and Zi-division lead: **Tang Haoyun (唐浩云 / Haoyun Xuezhang)** — co-founder, Xuelai Xuequ Learning Society; founder, Shanghai Qiaoweilai AI Technology Co., Ltd.; technical lead, Feifei Banban; UCL Physics class of 2023 (graduating 2026)
