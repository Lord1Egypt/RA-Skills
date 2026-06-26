# outfit-recommendation

## Purpose

This sub-spec defines how the agent should produce outfit recommendations and refine prior recommendations using the user’s existing wardrobe state.

This module is not a fixed outfit-construction workflow. It defines the boundaries, state usage rules, and judgment expectations that constrain recommendation behavior while preserving high agent autonomy.

The agent may decide how to organize recommendations, how many viable options to present, how much explanation to include, and how to merge compatible intents in one response, as long as it remains fact-grounded and within the write and confirmation boundaries defined elsewhere.

---

## Recommendation Role

The recommendation module is responsible for:
- proposing wearable outfit combinations from the recorded wardrobe,
- adapting recommendations to the current request and context,
- refining an earlier recommendation when the user asks for changes,
- and naturally incorporating relevant temporary constraints, long-term preferences, and item-level notes.

It should help the agent make good judgment calls. It should not force the interaction into a rigid sequence of mandatory steps.

---

## State Consumption Rules

Recommendation behavior may read all four shared state layers, but each layer serves a different role.

### fact state
`fact state` defines the available wardrobe inventory and recorded item attributes.

Recommendation must use `fact state` to determine what items may actually be proposed. No recommendation may rely on items that are not present in authoritative wardrobe facts.

### session state
`session state` contains the temporary constraints and context that matter for the current interaction, such as:
- current weather-relevant context,
- temporary dislikes or preferences,
- current occasion,
- immediate user constraints,
- and prior recommendation context from the same session.

Recommendation should treat `session state` as the highest-priority layer for current-turn direction, but not as a source of new wardrobe facts.

### persistent preference
`persistent preference` captures stable user tendencies across sessions.

Recommendation should use persistent preference to rank, bias, or frame otherwise valid candidates when doing so helps choose among multiple plausible outfits. Persistent preference should not override explicit current-turn instructions.

### item notes
`item notes` capture item-specific experience, cautions, or contextual observations.

Recommendation should use item notes to adjust confidence, ranking, caveats, or explanation for a specific item. Item notes do not create new wardrobe facts and should not be generalized into user-wide preference unless another module has already persisted that conclusion appropriately.

---

## Interpretation and Priority Rules

Recommendation should apply the shared state model as follows:

1. Use `fact state` to determine the candidate set.
2. Use `session state` to determine what matters for this reply.
3. Use `persistent preference` to rank or bias among valid candidates.
4. Use `item notes` to qualify specific items with caution, support, or context.

The agent must preserve the following conflict rules:

- Explicit current-turn user instructions outrank persistent preference for the current reply.
- `fact state` is authoritative on item existence and recorded wardrobe attributes.
- `item notes` may influence whether an item is a good choice, but may not be treated as proof that the item does or does not exist.
- Newly established same-turn temporary context may affect the current recommendation immediately when doing so is natural and safe.

---

## Recommendation Discretion

The agent retains broad discretion in how it constructs and presents recommendations.

It may:
- present one strong option or several viable options,
- choose a concise or slightly more comparative explanation,
- decide which attributes deserve emphasis,
- and compress reasoning that is obvious from the request and the available wardrobe.

This discretion exists to support natural recommendation quality, not to weaken factual or state boundaries.

---

## Explanation Boundary

Recommendation should explicitly state relevant constraints when they materially affect the answer.

The agent should explicitly say so when:
- the wardrobe cannot fully satisfy the request,
- the proposed outfit is the closest available match rather than a full match,
- a notable item note materially changes the recommendation,
- a temporary current-turn constraint causes a tradeoff,
- or a refinement preserves most of the prior outfit and changes only selected parts.

The agent may omit or compress minor reasoning when:
- the recommendation is straightforward,
- the omitted detail does not affect safety or user understanding,
- and no significant tradeoff needs to be surfaced.

Recommendation explanations should remain practical and grounded. They should not overclaim confidence or precision that the recorded wardrobe state does not support.

---

## Sparse Wardrobe Behavior

When the wardrobe is sparse or cannot fully satisfy the request, recommendation should still try to be useful.

The agent may:
- broaden within nearby style or formality space,
- offer the closest wearable match from available items,
- explain the gap directly,
- and propose a small number of reasonable alternatives if they clarify the tradeoff.

The agent must not:
- invent missing items or categories,
- imply that the wardrobe satisfies a requirement that it only partially satisfies,
- or fabricate detailed style precision that is not supported by the available inventory.

If the missing information or missing distinction would materially change the recommendation, the agent should ask a clarifying question instead of stretching the interpretation too far.

---

## Compound Request Handling

Recommendation may be merged naturally with other compatible intents when doing so does not bypass write or confirmation boundaries.

Examples include:
- recommendation plus a temporary requirement,
- recommendation plus an item note supplied in the same turn,
- recommendation plus a long-term preference signal,
- recommendation plus refinement instructions,
- and recommendation plus newly provided contextual details.

In merged handling:
- same-turn temporary constraints may influence the current recommendation immediately,
- same-turn note or preference signals may be acknowledged and consumed according to their proper state layer,
- but recommendation must not silently redefine how those signals are written, persisted, or confirmed.

If the user request also includes a state-changing action governed by another module, recommendation may proceed in the same response only when doing so is safe and does not bypass any required confirmation.

---

## Refinement Behavior

When the user is refining a prior recommendation, the agent should preserve continuity unless the user asks for a reset or the requested change logically requires broader recomposition.

A refinement request should normally keep the stable parts of the prior outfit and update the most relevant components first.

The agent should make clear what changed when that change is material to the answer.

---

## Hard Boundaries

Recommendation must respect the following hard boundaries:

- It must not invent wardrobe items, owned categories, or unsupported item attributes.
- It must not treat inference as fact.
- It must not silently rewrite `fact state`, `persistent preference`, or `item notes` for convenience.
- It must not claim that a temporary session signal is now a durable preference unless another module has explicitly handled that write.
- It must not bypass confirmation requirements that belong to CRUD, preference persistence, or other state-changing modules.
- It must not convert recommendation convenience into unauthorized state mutation.
- It must not rely on workflow-style mandatory sequencing when a more natural response is possible within policy boundaries.

---

## Output Guidance

Recommendation should usually:
- answer directly with a viable outfit or set of options,
- name the concrete items being recommended,
- include enough rationale to make the recommendation understandable,
- and surface major constraints or tradeoffs when relevant.

The response should stay practical, grounded, and proportionate to the request.

---

## Dependencies

This sub-spec depends on the main skill specification for:
- the four-layer state model,
- the global fact boundary,
- the shared write and confirmation boundary,
- compound-intent arbitration,
- and the general autonomy-within-boundaries principle.

This sub-spec also depends on other sub-specifications for rules it must consume but not redefine:
- weather/tool usage rules,
- item-note writing rules,
- persistent-preference writing rules,
- and wardrobe mutation rules.
