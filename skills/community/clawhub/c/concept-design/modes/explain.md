# Explain

1. Trace specifications, entries, state, actions, callers, queries, tests, and failure paths.
2. Select only the content needed from [views and evidence](../references/spec-reading.md#views-and-evidence).
3. Deliver Markdown explaining behavior, with diagrams where needed and current file, symbol, and line references.
4. Check against code and the [specification notation](../references/spec-notation.md); without implementation, explain only the design.

Generate concept and synchronization diagrams through the [map workflow](../references/diagram-contract.md#usage).
MUST NOT manually fill relationships the generator could not parse.
Teaching order MUST NOT be presented as evidence of execution order, transactions, or runtime correctness.
