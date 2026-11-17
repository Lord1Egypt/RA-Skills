# Saved details and secure forms

Use the current connected Memory schemas. Discover value-free metadata with
`get_memory_footprint` before filling a payment or non-payment form, without
requiring a checkout session. `list_memory_items` with templates included can
find an available template even when no item exists. Widen a narrow search
before concluding that a matching person, account or field is absent.

Match entity/person, semantic role, field meaning and script/transliteration,
not just a similar label. Me owns the user's Personal profile, Passport and
Address; Passenger and Traveler describe use roles. Preserve an existing
custom title. Prefer a clear task-compatible match and its current reuse
policy. Ask once by name for material ambiguity or consent, not for values
that discovery already establishes are available. Chat context does not skip
discovery. For transfers, resolve address, network and asset together.

Materialize only exact selected item revisions and field IDs through
`materialize_memory_items` or the current `resolve_browser_form_values`
workflow. Metadata CRUD is value-free; request/status reads do not release
protected data. Memory consent authorizes only that use, not payment or
submission. Retain selected entities, item revisions and the typed collection
through a multi-field/batch continuation; replay the unchanged resolver as
directed rather than dropping previously resolved fields or starting siblings.

Missing protected fields use the request-owned secure web form or service
editor returned by the owning workflow. `collectionGroups.target` proposes
Save; it does not read values. Custom forms cover unsupported fields only,
not a replacement for the existing typed collection. Incomplete saved items
are valid. Use task-provided details only where no usable saved match exists,
and offer Save where useful.

## Explicit Save and updates

For explicitly supplied ordinary or protected values, call `save_memory_item`
directly, preserving the user's values and a useful description. Select the
person/organization from context or create the appropriate new entity; use Me
for self or unusable identity hints. Use Personal profile or Organization
profile for default profile titles and retain custom titles. Do not invent
placeholder values, require a collection session or ask for the same values
again. Retry the same client request identity and unchanged input after an
ambiguous result; a new key is for a genuinely distinct Save intent.

Clipboard input exposes plaintext: require a field-specific choice and allow
direct input. Never fetch clipboard contents speculatively. If direct Save
is unavailable, report the blocked save; preserve installation and sign-in.
For updates/deletions, identify the exact owned item and expected revision
through the current metadata APIs. `correct_memory_field` follows its own
service-issued correction decision; do not invent a different-details choice.

Use authorized values through the host's documented targeted input only for
the intended form/task. Public recipient fields may also be used for the
exact requested transfer. For explicitly requested protected recall, show a
value only when the approved purpose explicitly authorizes revealing it in
this chat; form-use consent does not grant that permission. Otherwise do not
expose values in chat, files, logs, unrelated
forms, screenshots exported to others or external messages. A complete batch
must resume its same request/resolver after the recorded decision, including
when another channel supplied the winning answer. On denial, do not release
the denied values; continue only the parts that remain authorized.

An expired fulfilled release is not a denial. Refresh the footprint, verify
the same active form and resolve again with a new clientRequestId as the
service directs. Current policy decides whether another review is needed.
Preserve the task, merchant and payment operation; do not recollect every
field, replay an expired artifact or use a new identity to bypass a denial.
