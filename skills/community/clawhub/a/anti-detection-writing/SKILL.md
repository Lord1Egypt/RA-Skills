---
name: anti-detection-writing
description: Polish AI-written replies, emails, articles, and documentation for smoother flow and better human readability. Preserve meaning and factual accuracy; when requested, test revisions with GPTZero or another detector and work toward lower AI-detection scores.
---

# Anti-detection writing

Make AI-written prose easier and more natural to read while preserving its meaning. Improve flow, specificity, and tone for the intended audience. When detector testing is requested, work toward lower scores through useful edits and measure the outcome; never trade accuracy or readability for a score. Detector results do not establish human authorship or permission to publish.

## Establish the purpose and facts

1. Save the original text. Identify its reader, purpose, format, and requested tone or length from the supplied context. For a discussion reply, also read the question and existing replies. For public participation, respect the destination's rules, explicit objections to AI-assisted work, and disclosure requirements.
2. Treat supplied facts as the starting point for a self-contained edit. Verify substantive factual corrections against relevant sources; for technical advice, inspect official documentation or implementation and record the version when it matters. Distinguish source inspection, local tests, and deployment verification. Flag unsupported claims instead of adding invented evidence.
3. Inventory the substantive claims, commands, code, conditions, uncertainty, and reported symptoms. For each claim record whether it is preserved, corrected, or removed, and why. Identify what the reader needs to understand, decide, or do.

## Write and review

- Rebuild the text around the reader's purpose rather than retaining the original sentence order. Put the main point where the format calls for it, connect each sentence to the next, and keep the detail needed to understand or act on it.
- For a procedure or causal explanation, map each action to its component, prerequisite, and limiting condition. Arrange the answer in that dependency order. Place a prerequisite before the action that needs it and keep an exception beside the claim it limits. Replace an ambiguous pronoun with the existing component name; preserve unknown actors as unknown. Leave already clear passages intact.
- Prefer concrete nouns and verbs. Remove generic reassurance, repeated summaries, rhetorical contrasts, and irrelevant background. Use lists only where they make steps or comparisons easier to follow.
- Preserve operational qualifications and exact code unless evidence supports a correction. Record deliberate scope cuts; do not call an answer fully claim-preserving when useful details were removed.
- Match the requested register and use an authentic writing sample for tone when supplied. Vary sentence length when it improves pacing; do not force informality or strip useful structure. Never invent personal experience, tests, certainty, identity, quotations, typos, or invisible characters to make text appear human-written.
- A short, exact asker quotation can identify the concern being answered. Include it only when it helps the reader. Verify context and attribution; do not pad or rotate quotations to hunt for a detector score.
- Compare the finished answer directly with the claim inventory. Check who acts, negation, cause and effect, scope, certainty, numbers, units, and prerequisites. Match protected code, commands, identifiers, URLs, and exact quotations byte-for-byte unless a verified correction is recorded. Account for every cut or correction and remove unsupported additions. This writer self-check does not replace separate review.
- When a separate reviewer is requested or available, give them the reader's purpose, relevant context and sources, baseline, final text, and claim inventory without detector scores. Request a verdict on correctness, relevance, readability, tone, and necessary qualifications, tied to the final file's SHA-256. Resolve factual objections even if an incorrect version has a lower score. If no separate reviewer is available, say so; a self-check is not independent review.

## Measure only when requested

Read [measurement instructions](references/measurement.md) before live scanning and [evidence limits](references/evidence.md) before interpreting results. Use the user's requested service, mode, and supported browser tools. This skill supplies no browser controls and does not authorize subscriptions, paid scans, public posting, or new account access.

For a comparison, select cases and candidates before seeing scores. Record fresh baseline and candidate scans using the same service, mode, and displayed model. Retain failures and unchanged results. Compare a fixed body with a relevant quotation separately from prose rewriting; track content and length changes. Distinguish first-pass trials from adaptive iterations.

Confirm the effective editor text, completed scan, fresh-result indicator, model, all classification confidences, timestamp, and warnings. Save exact inputs and private visible evidence. A stale displayed number is not a result for changed text. Never omit code or pad a short answer to satisfy a detector.

The optional checker in `scripts/validate_receipt.py` checks strict plain-text receipt consistency. Its [receipt format](references/receipt-format.md) rejects unrecorded editor changes; it does not support rendered-Markdown transformations or authenticate the service. A valid receipt can record 100% AI. Apply a numeric threshold only when the user explicitly requests one.

## Publish and report

Honor existing user authorization; do not invent authorization or ask again for an already authorized action. For a public reply, refresh the discussion before posting and reassess if context changed. Match the final body to the reviewed version and, when required, its scan and requested threshold. Update the owned answer when editing, then independently read back its author, exact body, and URL. Do not post a duplicate or claim an answer was accepted without checking.

Report the actual quality findings, scores and warnings when measured, and edit or keep decisions. Missing required review or measurement leaves a candidate unpublished. A detector threshold applies only if requested. A successful local receipt check never authorizes publication.

For a showcase, include only quality-passing candidates with a measured decrease against a saved before-text using comparable completed scans. Link exact inputs, identify the intervention and tested version, and keep the full comparison denominator visible. Put unchanged, worse, rejected, unpaired, and unmeasured outcomes in a separate limitations section while retaining all records. A quotation effect is not a rewriting effect, and an untested skill revision is not an established improvement. If a case does not improve, document when the approach may not help or test a specific new edit within a bounded experiment.
