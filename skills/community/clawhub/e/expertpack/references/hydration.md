# Hydration Reference

The complete lifecycle for filling an ExpertPack with knowledge.

**Core principle:** The goal is not to document everything — it's to document what only this pack can provide. Every hydration decision filters through the EK lens: *Does the model already know this? If yes, minimize. If no, maximize.*

## Source Audit

Before populating, inventory everything available:

- **Existing documentation** — docs, help articles, wikis, READMEs
- **Technical artifacts** — source code, schemas, configs
- **Visual materials** — screenshots, diagrams, UI mockups
- **Video content** — tutorials, demos, training recordings
- **Human experts** — tribal knowledge holders
- **Feedback channels** — support tickets, forums, reviews, bug trackers
- **Published works** (person packs) — books, articles, social media, interviews

## EK Potential by Source Type

| Source Type | Typical EK Density | Notes |
|------------|-------------------|-------|
| Expert tribal knowledge | Very High | Exists only in human heads |
| Undocumented code behavior | High | Real vs. documented behavior |
| Support tickets / complaints | High | Real pain points models can't invent |
| Internal decision records | High | The "why" behind choices |
| Community forums (Reddit, GH Issues) | High | Gotchas, version bugs, compatibility quirks |
| Conference talks / interviews | Medium-High | Practitioner perspective |
| Official documentation | Low-Medium | Often well-represented in training data |
| Technology primers / overviews | Low | Models already know this |

**Priority:** Mine high-EK sources first. Official docs last (and only for scaffolding).

## EK Triage Process

For every piece of extracted content:

1. **Extract** an atomic factual proposition
2. **Blind-probe** 2-3 frontier models with a question derived from the proposition (no pack loaded)
3. **Score** the responses against ground truth:
   - Models get it right → **GK** (general knowledge) → compress to one-line scaffolding
   - Models get it partially right → **Partial** → include but don't over-invest
   - Models get it wrong / refuse → **EK** (esoteric) → full treatment: detailed content, propositions, lead summaries
4. **File** based on classification

**Common-knowledge compaction rule:** When GK must be present for completeness, one sentence max. Link to the esoteric content that depends on it.

Good: `**Zigbee** — Low-power mesh protocol (2.4 GHz, 65K nodes). See [protocols.md](concepts/protocols.md) for HA-specific coordinator firmware quirks.`

Bad: Three paragraphs explaining what Zigbee is and how mesh networking works.

## Hydration Priority Matrix

| Content Type | EK Likelihood | Hydration Priority | Treatment |
|-------------|--------------|-------------------|-----------|
| Practitioner workflows / "how we actually do it" | Very High | 🔴 Highest | Full extraction, propositions, lead summaries |
| Failure modes / gotchas / edge cases | Very High | 🔴 Highest | Detailed with examples |
| Configuration specifics / undocumented settings | High | 🟠 High | Full extraction |
| Version-specific bugs / compatibility | High | 🟠 High | Full extraction with refresh metadata |
| Architecture decisions / "why this way" | High | 🟠 High | Full extraction |
| UI/API walkthrough details | Medium | 🟡 Medium | Probe first, then decide |
| Standard procedures (documented SOPs) | Medium | 🟡 Medium | Probe first — may be GK |
| Concept definitions / technology overviews | Low | 🟢 Low | One-line scaffolding only |
| History / background / industry context | Low | 🟢 Low | Skip unless unique angle |

## Pack-Type Specific Guidance

### Person Packs
Almost entirely EK by nature — private stories, beliefs, voice patterns, relationships exist nowhere in model weights. **Skip blind probing** for `verbatim/`, `mind/`, `presentation/`, `relationships/`. Probe only `facts/` for public figures (biographical data may be in training data).

### Product Packs
Highest GK contamination risk — documentation, architecture overviews, and tech primers are often in training data. **Probe all documentation-sourced content.** Skip probing for expert walkthroughs and code-analysis findings. Focus hydration on: troubleshooting, undocumented behavior, configuration gotchas, and practitioner workflows.

### Process Packs
Mixed: official SOPs may be in training data, but practitioner experience, failure modes, timing, and regional variations are esoteric. **Probe** `fundamentals/` and formal descriptions. **Skip probing** `gotchas/`, `exceptions/`, and practitioner-contributed content.

## Population Methods

### 1. Documentation Mining
Read docs → extract facts → EK triage → file. Good starting point but lowest EK density. Use mainly for scaffolding.

### 2. Expert Walkthrough
Interview a domain expert. Record screen + audio. The expert narrates while demonstrating. Highest-quality source for tribal knowledge, decision rationale, and "why we do it this way."

### 3. Code/Artifact Analysis
Read source code, configs, schemas. Extract actual behavior vs. documented behavior. Especially valuable for undocumented features, default values, and edge case handling.

### 4. Feedback Mining
Mine support tickets, forum threads, GitHub issues, app reviews. Extract: common pain points, workarounds, version-specific bugs, real user vocabulary (for glossary). Highest-EK source for open-source products.

### 5. Video Transcription
Transcribe tutorials, demos, conference talks. Extract practitioner knowledge embedded in narration. Tag with timestamps for provenance.

### 6. Observation / Testing
Use the product/process yourself. Document what you discover that isn't in any other source. Especially valuable for UX flows, error messages, and edge cases.

## Retrieval Layer Generation

After populating content, generate retrieval optimization layers:

1. **`_index.md`** per content directory — table of contents for agent navigation
2. **`summaries/`** — section-level summaries for broad query matching (RAPTOR pattern)
3. **`propositions/`** — atomic factual statements for precise retrieval
4. **`glossary.md`** — maps user language to technical terms (Tier 1, always loaded)
5. **Lead summaries** — 1-3 sentence blockquote at top of high-traffic files

These layers work together — don't skip any. Split files + summaries + propositions consistently outperform any single change.

## Source Provenance

Every content file should track its sources in YAML frontmatter:

```yaml
---
sources:
  - type: video
    title: "Product Overview Walkthrough"
    ref: "03:12-04:05"
  - type: documentation
    url: "https://docs.example.com/feature-x"
    date: "2026-01-15"
---
```

Types: `video`, `documentation`, `interview`, `support`, `conversation`.

## Coverage Map

Every pack needs `sources/_coverage.md` — an honest accounting of what was researched:

```markdown
# Research Coverage — {Pack Name}

## Source Inventory
| Source | Status | Value | Notes |
|--------|--------|-------|-------|
| r/{subreddit} | ✅ Mined | High | Top 50 threads reviewed |
| {YouTube channel} | 🟡 Sampled | High | 3 of ~40 videos |
| {forum} | ⬜ Identified | Unknown | Not yet accessed |

## Known Gaps
- {Specific area that's thin or missing}

## Priority Sources for Next Pass
1. {Highest-value unmined source}
```

Status key: ✅ Mined | 🟡 Sampled | ⬜ Identified | ❌ Checked, low value
