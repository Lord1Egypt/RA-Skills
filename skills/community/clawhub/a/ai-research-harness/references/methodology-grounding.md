# Methodology Grounding for Research Design

> Added in v1.3.0 — Prevents "invented from thin air" designs by enforcing theoretical accountability.

## The Problem

AI research agents can produce plausible schemas, scoring systems, and experiment designs very quickly. The output *looks* scientific — structured, detailed, internally consistent. But without explicit theoretical grounding, these designs are:

1. **Ungeneralizable** — no one can predict whether they'll work in other domains
2. **Indefensible** — reviewers will ask "why this design?" and you'll have no answer beyond "it seemed reasonable"
3. **Unimprovable** — you can't tell what's wrong when it fails, because you don't know what assumptions it rests on

The antidote: **every non-trivial design decision must trace to at least one published precedent or an explicitly stated hypothesis**.

## Three Layers of Grounding

### Layer 1: Schema Design (Knowledge Representation)

When designing a knowledge schema (card format, field structure, asset taxonomy):

| Question | What to look for |
|----------|-----------------|
| Why these categories? | Ontology Design Patterns (Gangemi & Presutti, 2009); knowledge engineering taxonomies; domain-specific classification standards (e.g., EBV for biodiversity) |
| Why these fields? | Information retrieval theory: which fields actually enable downstream tasks? Compare with existing schemas (Knowledge Cards ICLR 2024, PROV-O for provenance) |
| Why this granularity? | Cognitive load theory; minimal sufficient representation principle; ablation studies on field necessity |
| How to validate completeness? | Coverage analysis against domain tasks; expert Delphi review; comparison with established benchmarks |

**Minimum grounding**: For each schema category/type, cite at least one work that uses a similar structure AND explain why your deviation (if any) is justified.

### Layer 2: Scoring & Evaluation Design

When designing a scoring rubric or evaluation metric:

| Question | What to look for |
|----------|-----------------|
| Why these dimensions? | Construct validity theory (Cronbach & Meehl, 1954); multi-trait multi-method matrix; domain-specific evaluation frameworks |
| Why these weights? | Analytic Hierarchy Process (Saaty, 1987) or similar weight justification; sensitivity analysis showing stability |
| How to validate the rubric? | Inter-rater reliability (Cohen's κ); comparison with established benchmarks (PlanBench, TravelPlanner, AgentBench); pilot scoring with calibration |
| Are dimensions independent? | Discriminant validity; correlation analysis between dimensions; avoid double-counting |

**Minimum grounding**: For each scoring dimension, cite at least one evaluation study that uses a similar construct AND explain what construct validity evidence you have or plan to collect.

### Layer 3: Experiment Design (Causal Inference)

When designing controlled experiments:

| Question | What to look for |
|----------|-----------------|
| What is the treatment? | Precisely define what changes between groups; use Rubin's potential outcomes framework |
| What is the outcome? | Primary endpoint must be pre-registered; distinguish proxy outcomes from true outcomes |
| What are confounders? | List known confounders and how they're controlled; acknowledge unmeasured confounders |
| How many subjects? | Power analysis (a priori); if n is small, report effect sizes with confidence intervals rather than p-values |
| Is attribution clean? | Adjacent groups differ by exactly one variable; no confounded treatments |

**Minimum grounding**: State the causal model explicitly (treatment → outcome, with confounders and mediators). Reference at least one experiment in the same or adjacent domain that uses a comparable design.

## Design Justification Document Template

Before implementing any non-trivial design (schema, scoring system, experiment protocol), write a brief justification:

```markdown
# Design Justification: [Design Name]

## 1. What is being designed
One-paragraph description of the design artifact.

## 2. Precedent Analysis
| Design Decision | Published Precedent | Our Deviation | Justification |
|----------------|--------------------|----|------------|
| [decision 1] | [cite paper/system] | [same / different because...] | [why] |

## 3. Theoretical Basis
- Theory/framework: [name]
- Key reference: [cite]
- How it applies: [explain]

## 4. Assumptions (if no precedent exists)
- Assumption 1: [state clearly]
- How to test: [experiment or analysis]

## 5. Validation Plan
- How will we know this design works?
- What constitutes evidence of failure?

## 6. Reviewer-Proofing
- Anticipated reviewer question: "Why this design?"
- Answer: [grounded response]
```

## Methodology Review Gate

**Trigger**: Any design that is "novel" (no direct precedent in published work) must pass this gate before entering experiment execution.

**Gate criteria** (ALL must be met):
1. ✅ Design Justification Document written
2. ✅ At least 2 published works cited in Precedent Analysis OR explicit assumption declaration
3. ✅ Validation plan stated
4. ✅ Human review for designs affecting protected surfaces (schema, rubrics, experiment protocol)

**What counts as a "published precedent"**:
- Peer-reviewed papers (any venue)
- Well-cited technical reports (e.g., arXiv with 50+ citations)
- Established standards (e.g., W3C PROV, FAIR principles)
- Widely-adopted systems (e.g., Hugging Face model cards, OpenAI evals framework)

**What does NOT count**:
- "Common practice" without citation
- AI-generated suggestions without source verification
- Your own previous unpublished designs

## Self-Evolution Integration

When a methodology gap is discovered (e.g., reviewer questions, experiment failure traceable to design):

1. **Log** the gap as a learning entry with category `methodology_gap`
2. **Trigger** a targeted literature search to fill the gap
3. **Update** the relevant Design Justification Document
4. **Propagate** the new grounding to the research-harness skill if broadly applicable

This creates a feedback loop: research execution exposes methodology gaps → gaps trigger learning → learning strengthens future design discipline.

## Key References

- Cronbach, L. J., & Meehl, P. E. (1954). Construct validity in psychological tests. *Psychological Bulletin*.
- Gangemi, A., & Presutti, V. (2009). Ontology design patterns. In *Handbook on Ontologies*.
- Saaty, T. L. (1987). The analytic hierarchy process. *Mathematical Modeling*.
- Rubin, D. B. (2005). Causal inference using potential outcomes. *Journal of the American Statistical Association*.
- Wilkinson, M. D., et al. (2016). The FAIR guiding principles for scientific data management. *Scientific Data*.
- Shuster, K., et al. (2024). Knowledge Cards. *ICLR 2024*.
- Liu, X., et al. (2024). PlanBench benchmark. *TMLR*.
