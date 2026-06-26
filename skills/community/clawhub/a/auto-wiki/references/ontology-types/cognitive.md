# Cognitive Ontology: Collection and Synthesis Strategy for Person Research

> Use this strategy when research target is a **person** (their thinking patterns, decision modes, expression styles).
> Adapted from cognitive profiling methodology, only covers wiki accumulation phase, not final persona crystallization.

---

## 1. Six-Dimension Collection Framework

Each dimension corresponds to one ingest, producing one source page.

| Dimension | Search For | Extract | Source Page Output |
|-----------|-----------|---------|-------------------|
| **Writings** | Books, long articles, papers, newsletters | Recurring core claims (>=3 times = true belief); self-coined terms; recommended reading lists (intellectual lineage) | `sources/{date}-writings.md` |
| **Conversations** | Podcasts, long videos, AMAs, deep interviews | Responses when pressed; spontaneous analogies; moments of changing position; questions declined | `sources/{date}-conversations.md` |
| **Expression DNA** | Twitter/X, Weibo, Jike, short posts | High-frequency word patterns; controversial positions; humor style; public debates | `sources/{date}-expression-dna.md` |
| **External Views** | Others' analysis, book reviews, criticism, biographies | Patterns observed externally; criticism and controversy; comparisons with peers | `sources/{date}-external-views.md` |
| **Decision Records** | Major decisions, turning points, controversial actions | Decision context and logic; post-hoc reflections; consistent/inconsistent cases | `sources/{date}-decisions.md` |
| **Timeline** | Complete resume + recent 12 months activity | Key milestones; intellectual turning points; latest status (prevents staleness) | `sources/{date}-timeline.md` |

**Information grading**: Every extraction must label source type—primary (own words) > secondary (others' retelling) > speculation.

**Source priority**: Own writings/long interviews/actual decisions > Social media/Others' evaluation > Second-hand retelling.
Source blacklist: Zhihu, WeChat Official Accounts, Baidu Baike. For Chinese figures, prioritize Bilibili original videos, Xiaoyuzhou podcasts, authoritative media (36Kr/LatePost/Caixin).

---

## 2. Synthesis Rules

After all 6 dimension source pages are ready, execute synthesis, producing entity and concept pages.

### 2.1 Triple Verification (Mental Model vs Decision Heuristic)

List candidate claims from all sources (usually 15-30), verify one by one:

| Verification Dimension | Determination Method | Pass Criteria |
|------------------------|---------------------|---------------|
| **Cross-domain reproducibility** | Same thinking framework appears in >=2 different domains/topics | Writings + Decisions both confirm |
| **Generative power** | Using this model can infer person's stance on unaddressed issues | Can produce reasonable predictions |
| **Exclusivity** | Not all smart people think this way, reflects this person's unique perspective | Has discriminative power |

- Triple pass → Mental model (write to entity page)
- Only 1-2 passes → Downgrade to decision heuristic (write to concept page)
- 0 passes → Not included in wiki

### 2.2 Expression DNA Quantification

From person's long writings/speeches, extract 20 segments, count:

- **Sentence fingerprint**: Average sentence length, question ratio, analogy density (/1000 words), first-person frequency, certainty tone ratio
- **Style tags** (7-axis score): Formal-Vernacular, Abstract-Concrete, Cautious-Assertive, Academic-Popular, Long sentence-Short sentence, Setup-first-Conclusion-first, Data-driven-Narrative-driven
- **Taboo words and verbal tics**: Words never used + high-frequency expressions

Produce a concept page: `concepts/expression-dna.md`.

### 2.3 Conflict Handling

Conflicts are personality traits, not bugs to fix. Handle in three categories:

| Conflict Type | Meaning | Wiki Treatment |
|---------------|---------|----------------|
| **Temporal conflict** | Early said A, later said B (view evolution) | Record evolution trajectory in page, label periods; confidence stays `high` |
| **Domain conflict** | Advocates X at work, Y in life | Record by domain, don't force unity; this is source of depth |
| **Essential tension** | Intrinsic value conflict (e.g., pursues both freedom and discipline) | Create independent concept page `concepts/tension-{name}.md`, label as core tension |

Never do: pick one side and ignore the other, fabricate reconciliation, pretend conflict doesn't exist.

---

## 3. Wiki Page Types

### Entity Pages

**One page per mental model**, not one page per person.

```markdown
---
title: Inversion
type: mental-model
created: 2026-04-06
updated: 2026-04-06
sources: [2026-04-06-writings, 2026-04-06-decisions]
confidence: high
verification:
  cross_domain: true
  generative: true
  exclusive: false
  domains: [investment decisions, risk management, product design]
relations:
  - target: misjudgment_psychology
    type: derived_from
---

## Model Description
Facing "how to succeed", first think "how to ensure failure".

## Source Evidence
- Writings: Mentioned X times in "Poor Charlie's Almanack" ([[2026-04-06-writings]])
- Decisions: Actually applied in Y event ([[2026-04-06-decisions]])

## Application
Given any goal G, first list all paths leading to ~G, eliminate one by one.

## Limitations
Tends toward conservatism, may miss opportunities requiring frontal assault.
```

The person also has an overview entity page (`entities/{person-slug}.md`), linking to all mental models and concept pages.

### Concept Pages

For following content:

| Content | Page Example |
|---------|-------------|
| Decision heuristics (rules not passing triple verification) | `concepts/heuristic-{name}.md` |
| Values and anti-patterns | `concepts/values.md`, `concepts/anti-patterns.md` |
| Expression DNA | `concepts/expression-dna.md` |
| Core tensions | `concepts/tension-{name}.md` |
| Intellectual lineage (influence/influenced relationships) | `concepts/intellectual-lineage.md` |
| Honest boundaries (what this framework cannot do) | `concepts/honest-boundaries.md` |

### Source Pages

One source page per collection dimension (6 total), faithful summary of raw materials, not modified after creation.

---

## 4. Ingest Sequence Suggestion

No strict sequence required, but recommended:

1. **Writings + Timeline** first—establish basic framework and chronological context
2. **Conversations + Decisions** supplement—capture spontaneous thinking and real behavior
3. **Expression DNA + External Views** finalize—quantify style, introduce external calibration

Check after each ingest: Do existing pages need confidence updates, are there new conflicts.

---

## 5. Quality Standards

| Check Item | Pass Criteria |
|------------|---------------|
| Mental model count | 3-7, each with >=2 different domain evidences |
| Limitations per model | Clearly write failure conditions |
| Expression DNA | Complete statistical dimensions (sentence+style+taboo words) |
| Primary source ratio | > 50% |
| Conflict records | >=2 pairs of tensions, don't avoid or reconcile |
| Honest boundaries | >=3 specific limitations, label dimensions with insufficient info |
