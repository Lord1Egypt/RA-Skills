# clothing-notes

Clothing notes specification. This sub-specification governs how the skill records and uses `item notes` for specific wardrobe items.

---

## Purpose and scope

This document governs item-scoped historical notes attached to a specific wardrobe item.

`item notes` are used for observations such as wearing experience, pairing friction, care reminders, usage patterns, and other item-level feedback that may remain useful later.

This document does not govern `fact state`, global user preference, or recommendation logic itself. It defines what belongs in `item notes`, how notes may be appended, and how notes remain distinct from other state layers.

---

## What belongs in item notes

`item notes` may include item-scoped signals such as:
- wearing experience,
- comfort or discomfort,
- pairing limitations,
- care or maintenance reminders,
- item-specific likes or dislikes,
- usage frequency observations,
- and follow-up reminders tied to that item.

Typical examples include:
- "These shoes start rubbing after long walks."
- "That plaid jacket is hard to pair with bottoms."
- "This sweater needs hand washing."
- "That trench coat still needs dry cleaning."

A signal belongs in `item notes` only when it is about a specific item or a safely resolved item target.

If a signal is clearly about the user's general taste across items, it belongs to `persistent preference` instead.

If a signal is useful only for the current turn and does not clearly need item-level persistence, it may remain in `session state`.

---

## Append-only note model

`item notes` are append-only.

New note-worthy information should be added as a new entry rather than by deleting, rewriting, or erasing historical note entries.

Later notes may supersede earlier notes at the interpretation layer, but not by destructive overwrite.

This means:
- the historical record stays additive,
- newer notes may change how recommendation interprets an item,
- but the note log itself should not silently collapse history.

Each note entry should use the established `{ date, text }` structure, aligned with the wardrobe schema.

---

## Target identification boundary

Before appending an item note, the agent must be able to identify the target item safely.

The agent should first use the active conversational context, especially recently discussed items.

If needed, the agent may use available item attributes such as category or color to resolve the target.

If the target is still ambiguous, the agent must ask a clarifying question rather than guessing.

A note must not be appended to the wrong item merely because it seems likely.

---

## Silent append boundary

A note may be silently appended when all of the following are true:
- the target item is safely identified,
- the signal is clearly item-scoped,
- the note is additive rather than destructive,
- and the content is specific enough to remain useful later.

When those conditions are met, the agent may append the note while continuing the main conversation naturally, without forcing an extra confirmation step.

Typical silent-append cases include:
- wearing discomfort,
- pairing friction,
- care reminders,
- repair reminders,
- and stable item-specific usage observations.

Silent append does not mean silent overwrite.

A note append should create a new item-scoped record, not rewrite prior note history.

---

## Ambiguity and confirmation boundary

Not every clothing-related statement should become an item note.

### Target ambiguity

If the agent cannot safely determine which item the user means, it must ask which item they are referring to.

### Scope ambiguity

If it is unclear whether the user is talking about:
- a specific item,
- a general preference,
- or only the current session,
then the agent should avoid prematurely writing an item note with broader-than-justified scope.

When needed, the agent should prefer the narrower interpretation or ask for clarification.

### Destructive or action-implying statements

If the statement implies removal, disposal, deletion, or another irreversible action, the agent must not quietly record it as a note in order to sidestep the confirmation boundary.

For example, statements like "I should get rid of this" or "This can be thrown away" may trigger wardrobe-mutation implications and must not be reduced to harmless note-taking without considering deletion rules.

### Too-vague durable note content

If the statement is too vague to remain useful as item history, the agent should avoid appending a low-value durable note.

A vague statement may still matter for the current turn, but that does not automatically justify durable note persistence.

---

## Same-turn interaction with other intents

Item notes often appear together with recommendation or wardrobe discussion.

The agent may handle these together when safe.

For example:
- a newly appended note may immediately influence same-turn recommendation interpretation,
- but a not-yet-resolved item target must be clarified before an item note is appended,
- and a deletion-like statement must not be converted into a note simply to keep the conversation moving.

Same-turn usefulness and durable note append are related but not identical decisions.

---

## Reading contract for recommendation

Recommendation may consume `item notes` only as interpretive signals.

`item notes` may:
- lower or raise an item's suitability,
- provide cautionary context,
- explain pairing limitations,
- or add maintenance-related reminders.

`item notes` do not redefine wardrobe facts.

This document does not define recommendation ranking, styling discretion, or recommendation composition. It only defines the note layer that recommendation may read.

---

## Dedup and lifecycle consistency

Equivalent item notes should not be appended repeatedly just because the same signal is observed through different paths.

Deduplication should happen at the meaning level, not only at exact string level.

For example, two differently worded statements about the same shoes causing discomfort after long wear should generally be treated as the same note signal unless the later version adds materially new detail.

Automation backfill, if introduced later, may fill a missed item note only when:
- an equivalent note was not already appended,
- the target item can still be resolved safely,
- and the append would still satisfy the same note boundary.

Automation backfill must not:
- duplicate an already appended note,
- overwrite clearer immediate notes,
- promote an item note into `persistent preference`,
- or convert a confirmation-gated mutation into a harmless-looking note entry.

---

## Current-version automation note

The current version does not rely on hooks-based automatic backfill.

Item feedback should be handled during the active interaction rather than deferred to session-end or idle-time automation.

If automation is introduced later, it must follow the main specification's rules for capability detection, authorization, lifecycle-level coordination records, and write consistency.

---

## Dependency on the main spec and wardrobe facts

This sub-specification depends on the main specification for:
- the shared state model,
- the global write classes,
- the global confirmation boundary,
- and compound-intent arbitration.

It also depends on wardrobe facts for safe item identification.

This document refines those rules for item-scoped note handling only. It must not weaken fact-grounding, persistence boundaries, or confirmation requirements.
