# Report Expression Gate

Use this gate after evidence, methodology, mechanism, and decision checks have passed. It removes template-like report prose without weakening traceability, uncertainty, or formal structure.

## Signals

1. `Empty importance claims`
   - The report calls something significant, structural, transformative, or worth watching without naming the changed object, mechanism, evidence, or consequence.
2. `Consulting-language stacks`
   - Jargon and polished abstractions replace a concrete actor, constraint, causal step, or decision implication.
3. `Formulaic pivots`
   - Repeated binary reframes, negative setup, or identical three-part paragraphs simulate argument without advancing it.
4. `Unsynthesized navigation`
   - Section previews, transitions, and source summaries repeat headings or citations but do not help the reader locate evidence or reasoning.
5. `Low-information conclusions`
   - A sentence can be removed without changing the finding, confidence, limitation, reversal condition, or next action.
6. `Section-level non-progression`
   - Adjacent paragraphs or sections repeat the same claim and citations without adding evidence, mechanism, dissent, boundary, consequence, or decision value.

## Claim and speaker position

Before revising prose, preserve the claim's evidence status and the writer's position:

- confirmed fact, reported claim, user signal, inference, and gap must remain distinguishable
- a synthesis must not be rewritten as a witnessed fact or first-person experience
- the report may explain what follows from evidence, but must keep the inference path and confidence visible
- quotations, evidence IDs, formal-status labels, source provenance, and reversal conditions are protected fields

The evidence ledger and other structured research artifacts are truth sources. Do not apply free-form prose cleanup to them. If a report sentence changes a load-bearing claim, update the owning claim/evidence mapping and rerun the relevant lint instead of editing only the rendered paragraph.

## Research-specific exemptions

Keep a form when it improves rigor or retrieval:

- confidence qualifiers, uncertainty, scope limits, and evidence gaps
- claim-level citations, evidence IDs, formal-status labels, and source provenance
- necessary domain or legal terminology
- passive voice when the actor is unknown, disputed, institutionally distributed, or less important than the formal action
- navigation sentences, comparison tables, three-part scenarios, and structured lists that make evidence auditable
- concise executive judgments supported by the report

Do not force conversational `you`, remove hedging globally, or replace formal precision with punchy prose.

## Decision rule

A phrase or structure is a revision target only when it adds no evidence, mechanism, boundary, orientation, or decision value and has no formal-report justification.

Apply revision in this order:

1. protect evidence state, citations, formal status, uncertainty, dissent, and required output structure
2. verify claim-to-evidence and inference boundaries
3. remove repeated sections or restore genuine progression
4. repair jargon stacks, formulaic pivots, and low-information navigation
5. cold-read the executive judgment, limitations, reversal conditions, and next action

Never use global punctuation, sentence-form, or banned-word rules for reports. Colons, dashes, passive voice, questions, lists, and technical terminology remain available when they improve precision or auditability.

For review requests, return:

- `template_trace`
- `why_it_weakens_the_report`
- `research_exemption`
- `minimal_revision`
- `evidence_or_method_gap_exposed`

If expression cleanup reveals that a strong claim has no evidence or mechanism, route back to the owning evidence or mechanism gate instead of polishing the claim.
