# user-preference

User preference specification. This sub-specification governs how the skill interprets and persists `persistent preference`.

---

## Purpose and scope

This document governs long-term user preference, not temporary conversation context.

`persistent preference` means stable user tendencies that should shape future behavior across sessions, such as long-term style, color, fit, or occasion preferences.

This document does not govern `fact state`, item-scoped notes, or ordinary same-turn session handling. It also does not define recommendation logic itself. It only defines what may become durable user preference and what must remain session-only.

---

## Preference data surface

Persistent preferences are stored in `user/preference.json`.

If the file does not exist or is effectively empty, the agent should treat preference as uninitialized rather than as missing capability. Recommendation may still proceed normally, while future preference signals are interpreted under the rules below.

Persistent preference may include areas such as:
- style affinities,
- style aversions,
- preferred or avoided colors,
- fit preferences,
- occasion habits,
- and other durable user tendencies.

The durable profile should remain semantically coherent. It should not become a dump of every preference-like phrase the user has ever said.

---

## What qualifies as persistent preference

A signal qualifies for `persistent preference` only when it is sufficiently long-term in scope.

The relevant question is not whether the signal is useful right now. The relevant question is whether it is durable enough to shape future sessions without distorting the user's profile.

A signal is a good candidate for durable preference when it is one or more of the following:
- an explicit long-term instruction such as "remember this" or "from now on",
- a stable tendency that is stated clearly enough to generalize,
- a repeated pattern that is meaningfully consistent across situations,
- or a cross-situation habit that is useful beyond the current turn.

A signal is not a durable preference candidate merely because it sounds preference-like.

---

## What remains session-only

Many useful signals should remain in `session state`.

By default, the following should be handled as session-only rather than durable preference:
- one-turn styling constraints,
- temporary mood or occasion framing,
- current-weather or current-event adjustments,
- weakly implied likes or dislikes,
- and preference-like language whose scope is unclear between "for now" and "in general".

Examples include:
- "Not too formal today."
- "I want something lighter this time."
- "Today I want a more relaxed look."

These signals may affect the same-turn response immediately, but they are not persistent by default.

Being useful for the current reply does not make a signal persistable.

---

## High-confidence persistence threshold

A preference signal may be durably persisted only when long-term scope is sufficiently clear.

This usually means the signal is either:
- explicitly framed as a durable instruction,
- or clearly stable enough that treating it as a long-term preference would be reasonable and low-risk.

In addition, the signal should:
- be specific enough to record meaningfully,
- not be better modeled as item-specific feedback,
- not be better modeled as temporary session context,
- and not be materially contradicted by nearby context.

This sub-specification intentionally does not reduce the threshold to a rigid scoring table. The agent may exercise judgment, but the judgment must remain conservative about durable scope.

---

## Silent persistence vs confirmation

Not every durable preference update requires a separate confirmation step.

A durable preference update may remain silent when:
- the user's long-term intent is clear,
- the meaning is low-ambiguity,
- and the write is not unusually risky or broad in future impact.

However, confirmation is required when a durable preference write is too uncertain for lasting storage.

This includes cases such as:
- unclear scope between current-session intent and long-term preference,
- low-confidence preference inference that could materially shape future recommendations,
- ambiguous meaning about what should actually be remembered,
- or a broad durable update that would significantly redirect future behavior without enough evidence.

If the signal is useful now but not safe to persist durably, the agent should keep it in `session state` instead of forcing a durable write.

---

## Relationship to item notes and fact state

`persistent preference` must remain distinct from both `item notes` and `fact state`.

The agent must not:
- convert an item-specific observation into a global preference without sufficient basis,
- rewrite wardrobe facts as if they were preference,
- or promote temporary session context into durable preference merely because it affected the current response.

Examples:
- "That blazer feels too tight" is usually item-scoped feedback, not automatically a global fit preference.
- "I don't want anything too formal today" is usually session-only, not automatically a durable occasion habit.
- "Please remember that I prefer loose fits in general" is a durable preference candidate.

---

## Same-turn effect on responses

A preference-like signal may affect the current response before it qualifies for durable persistence.

The agent may immediately use new same-turn context in recommendation or reply framing while still deciding that the signal belongs only in `session state`.

This distinction is important:
- same-turn usefulness is one threshold,
- durable persistence is a higher threshold.

The agent should not persist simply because it already used the signal in the current reply.

---

## Conflict handling and profile consistency

Durable preference should stay coherent over time.

When a newer durable signal clearly supersedes an older durable preference, the durable profile should be updated in a meaning-consistent way rather than by accumulating contradictory fragments.

When the newer signal is weak, local, or ambiguous, the agent should avoid thrashing the durable profile. In such cases it is usually better to keep the signal session-only.

The agent should prefer:
- newer explicit long-term instructions over older weak inferences,
- narrower interpretations when durable scope is uncertain,
- and semantically normalized updates over repetitive append-style duplication.

`persistent preference` is not append-only in the same way that `item notes` are. Durable preference may be updated, replaced, or normalized when that is the most faithful representation of the user's stable tendency.

---

## Dedup and automation backfill consistency

Automation backfill may help capture a missed durable preference candidate, but it must follow the same persistence boundary as immediate handling.

Backfill may fill a missed durable preference write only when:
- the signal actually qualifies for durable preference,
- the write was not already completed in-turn,
- and the durable profile does not already contain an equivalent preference update.

Backfill must not:
- duplicate a durable preference that was already stored,
- overwrite a clearer or newer explicit durable instruction,
- promote session-only context into durable preference,
- or broaden an item-scoped signal into a general preference without sufficient basis.

Equivalent durable preference updates should be deduplicated at the meaning level, not only by exact string match.

---

## Current-version automation note

The current version does not rely on hooks-based automatic backfill.

Preference signals should be handled within the active interaction rather than delegated to end-of-session or idle-time automation.

If automation is introduced later, it must follow the main specification's rules for capability detection, authorization, lifecycle-level coordination records, and write consistency.

---

## Dependency on the main spec

This sub-specification depends on the main specification for:
- the shared state model,
- the abstract write classes,
- the global confirmation boundary,
- and compound-intent arbitration.

This document refines those rules for long-term user preference only. It must not weaken the shared persistence or confirmation model.
