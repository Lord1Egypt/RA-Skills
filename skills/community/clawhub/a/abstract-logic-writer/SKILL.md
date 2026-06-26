---
name: abstract-logic-writer
description: write, critique, score, compare, and revise english academic abstracts for ai, systems, and computer science papers using computable symbolic rules, lightweight ontologies, and sentence-level discourse constraints. use when the task involves drafting an abstract from notes, repairing sentence-to-sentence logic, checking verb-noun compatibility such as growth versus development, scoring two abstract fragments with a formal rule-based metric, bootstrapping or downloading a domain ontology, removing generic ai phrasing such as em dashes or unlike, or generating deliberately flawed negative examples for teaching and comparison.
---

# Abstract Logic Writer

## Overview

Use symbolic discourse constraints and a lightweight ontology to draft or critique English academic abstracts. Treat abstract writing as a constrained mapping from propositions to an ordered sentence sequence, not as free-form style imitation.

## Core workflow

1. Build a proposition set `P = {background, status, motivation, challenge, idea, technique, evidence}` from the user's notes.
2. Choose the shortest valid role chain whose image still contains `motivation`, `challenge`, and `idea`. The default 4-5 sentence chain is `M -> C -> I -> T -> E`, with optional `background` or `status` prepended.
3. For each sentence, write a micro-structure `general -> specification -> consequence/purpose`. Do not place a narrow detail before its governing concept.
4. Load `references/computable-rules.md` as the primary specification. Load `references/lexeme-typing.md` and `assets/lexeme_types.json` when verb-noun fit is uncertain.
5. If the domain terminology is sparse or unstable, load `references/ontology-bootstrap.md` and optionally run:
   `python scripts/ontology_bootstrap.py --domain "..." --terms "term a,term b" --outdir ./ontology_out`
6. Before finalizing, run:
   `python scripts/abstract_lint.py draft.txt`
   for rule diagnostics, and run
   `python scripts/abstract_score.py draft.txt`
   or
   `python scripts/abstract_score.py before.txt --compare after.txt`
   when a formal score or pairwise comparison is needed.

## Drafting discipline

- Assign each sentence exactly one primary discourse role.
- Never output a sentence that only labels a condition without causal or purposive load. Reject patterns like `X is a challenge.` unless the sentence continues with cause, consequence, or operational relevance.
- When introducing a new concept `x`, attach motivation, purpose, or consequence within the same sentence or an adjacent sentence.
- When explaining a mechanism, state what it enables, stabilizes, reduces, or preserves.
- Prefer typed predicate selection over idiomatic guesswork. Example: `traffic grows`, `demand increases`, `applications develop`, `systems evolve`, `accuracy improves`, `continuity is maintained`.
- Avoid common AI-sounding markers. Do not use the em dash or `Unlike` unless the user explicitly asks to preserve source wording.
- Do not end with a generic recap sentence. The last sentence must carry evidence, operational implication, or measured outcome.

## Output modes

### 1. Draft from notes

Return:
1. an optional symbolic plan when the source notes are underspecified,
2. the final abstract,
3. concise lint notes only when there are nontrivial tradeoffs.

### 2. Critique or rewrite an existing abstract

Return:
1. a violation list keyed to the symbolic predicates in `references/computable-rules.md`,
2. a repaired abstract,
3. the smallest possible set of lexical substitutions when the main issue is verb-noun mismatch.

### 3. Produce negative examples

Use `references/negative-examples.md`.
Generate intentionally flawed rewrites that violate one or more named predicates such as `summary_only`, `selection_mismatch`, `scope_inversion`, or `forbidden_marker`.
Label each negative example with the violated rules. Do not present it as recommended style.

## Resource map

- `README.md`: GitHub-facing quick start and repository guide.
- `references/computable-rules.md`: formal sentence and discourse constraints.
- `references/lexeme-typing.md`: upper ontology for noun classes and verb selection.
- `references/ontology-bootstrap.md`: domain ontology construction and download workflow.
- `references/negative-examples.md`: contrastive negative examples and rule tags.
- `references/source-abstract-corpus.md`: raw domain corpus supplied by the user.
- `scripts/abstract_lint.py`: heuristic checker for role order, banned markers, and selection mismatches.
- `scripts/abstract_score.py`: formulaic scorer and comparator for one or two abstract fragments.
- `scripts/ontology_bootstrap.py`: generate a seed ontology or download a public ontology file.
- `assets/discourse_rules.json`: machine-readable role order, forbidden patterns, and score weights.
- `assets/lexeme_types.json`: machine-readable lexeme typing rules.
- `examples/`: before-and-after fragments for quick scoring demos.
- `evals/`: sample scoring outputs for repository documentation.

## Working defaults

When the user does not provide all paper details, infer the missing low-risk connective tissue from the available propositions and state the assumptions briefly. Keep the prose compact, domain-accurate, and hierarchy-aware. Prioritize logical fit over rhetorical flourish.
