# wardrobe-crud

Wardrobe CRUD specification. This sub-specification governs requests that read or mutate `fact state` in the wardrobe.

---

## Purpose and scope

This document governs wardrobe facts: adding items, updating recorded item attributes, deleting items, and querying wardrobe data.

It is responsible for safe mutation of `fact state`. It is not the specification for recommendation logic, item notes, or long-term user preferences.

`fact state` is the authoritative record of what wardrobe items exist and which recorded attributes belong to them. This sub-specification must preserve that authority.

---

## Authority of wardrobe facts

Wardrobe facts must remain fact-backed.

The wardrobe record is the source of truth for:
- whether an item exists,
- how an item is identified,
- and which attributes have already been recorded for that item.

The agent must not invent wardrobe items, invent recorded attributes, or change wardrobe facts merely because such a change would make recommendation easier.

`item notes` and `persistent preference` may influence how facts are interpreted in later reasoning, but they do not override `fact state`.

Queries are read-only. A wardrobe query must not silently mutate wardrobe facts.

---

## Minimum information for safe mutation

### Required minimum fields for a new item

A new wardrobe item may be added once the agent can safely establish the minimum usable record:
- `id`
- `category`
- `name`

If `category` or `name` cannot be determined safely, the agent must ask a clarifying question before writing.

The agent should not block a valid add request merely because optional descriptive fields are missing.

### Optional recorded fields

The following fields may be recorded when available, but they are not required for a safe initial add:
- `sub-category`
- `color`
- `seasons`
- `style`
- `material`
- `warmth`
- `notes`
- `image_refs`

These fields should be recorded when clearly supported, but the agent should avoid unnecessary follow-up questions just to complete optional metadata.

### Stable identity

`id` must be stable after creation.

When generating a new `id`, the agent should inspect existing ids, take the highest sequence number in the same category, and assign the next available value using the established category-prefix format.

---

## Safe mutation boundary

This sub-specification governs durable changes to `fact state`.

### Add

A new item may be durably added when:
- the user intent to add or record an item is clear,
- the minimum identifying information is available,
- and the resulting record would not rely on invented facts.

The agent may write a minimal record first and leave optional fields absent until later information is available.

### Update

An existing item may be updated when:
- the target item is safely identified,
- the requested or clearly supported change is specific enough to apply,
- and the update does not depend on invented facts.

If the target is unique and the requested change is clear, the update may proceed without an extra confirmation step.

### Delete

Deletion is always a confirmation-required change.

A delete action must not proceed unless:
- the target item is safely identified,
- the user's delete intent is clear enough to justify an irreversible action,
- and the user has confirmed when required by irreversibility or ambiguity.

Deletion must never be treated as a silent write.

Deletion must never be performed by automation backfill.

---

## Confirmation and ambiguity boundary

Confirmation in wardrobe mutation is driven by irreversibility, ambiguity, and persistence impact.

### Ambiguous target

If the user description matches multiple wardrobe items, the agent must not guess.

The agent should present the most relevant candidates and ask which item the user means.

This applies to update and delete operations, and to any fact mutation that would otherwise change the wrong item.

### Insufficient description

If the user request does not provide enough information to safely add, update, or delete an item, the agent must clarify the missing information before writing.

For add requests, the key threshold is whether a safe `category` and `name` can be established.

For update or delete requests, the key threshold is whether the intended target and mutation can be safely resolved.

### Irreversible mutation

Deletion is irreversible in practice and therefore confirmation-gated.

The agent should not rely on tone alone. Even when the user wording sounds casual or bundled with other intents, the agent must treat deletion as a higher-risk action than ordinary note-taking or session handling.

### Ambiguity within compound requests

If a single user message combines deletion with another request such as recommendation or filtering, the agent may handle the requests in one response only if doing so does not bypass delete confirmation.

A pending delete must not be treated as already completed while the target or intent is still unresolved.

---

## Query and filtering behavior

Wardrobe queries are read-only.

The agent should:
- answer in natural language rather than as a raw database dump,
- summarize the most relevant result first,
- filter according to the user's actual concern,
- and state clearly when no matching items are found.

When a query result is empty, the agent may mention nearby relevant wardrobe context, but it must not invent substitute facts.

---

## Same-turn interaction with other intents

Wardrobe mutation may appear together with recommendation, note-taking, or preference signals in the same user request.

The governing rules are:
- a newly completed add or update may affect the same-turn response,
- a not-yet-confirmed delete must not be assumed as completed,
- and safe merged handling is allowed only when confirmation boundaries remain intact.

Examples:
- If the user adds a new jacket and then asks what outerwear they now have, the newly added item may be included once the add is safely completed.
- If the user asks to delete an ambiguous coat and then requests a spring outerwear summary, the delete must be clarified before the response relies on that change.

---

## Consistency and non-overwrite rules

This sub-specification only governs wardrobe facts.

It should not silently rewrite `item notes` or `persistent preference` unless the user request clearly belongs to those domains.

Automation backfill may fill a missed wardrobe mutation only when that mutation was not already completed in-turn. It must not replay an already applied mutation.

If an immediate fact mutation has already been completed, later automation must treat it as authoritative rather than reasserting it.

The same resolved fact mutation should behave idempotently. Re-observing the same completed mutation should not create duplicate change effects.

---

## Dependency on the main spec

This sub-specification depends on the main specification for:
- the shared definition of `fact state`, `item notes`, `persistent preference`, and `session state`,
- the global fact boundary,
- the global confirmation boundary,
- and compound-intent arbitration.

This document refines those rules for wardrobe mutation only. It must not weaken the main policy layer.
