# Write the PRD and specifications

Organize the confirmed model into the following deliverables.

## Overall PRD

Describe user needs, application purpose, scope, and scenarios. Index the concept and synchronization specifications. Record product dependencies, viable subsets, and exclusions as needed.

## Concept specifications

Explain why each concept exists and how it works: purpose, operational principle, state, and actions. Define each concept independently of other concepts; its operational principle connects behavior to value.

## Synchronization specifications

Identify concept instances and type bindings. Express coordination as “when—query/if—then”: match action occurrences, query state or check conditions, then initiate subsequent actions.

## Acceptance

Express needs as observable results, with assumptions and triggers linked to the relevant concepts or synchronizations. Check local behavior and application behavior separately, retaining required failure and timing bounds.

Preserve sources, reasons, and confirmation status. Keep undecided matters open and acceptance requirements separate from executed test evidence.

## Writing and ownership

Use the [reading version](../references/spec-reading.md) by default, expanding the [specification notation](../references/spec-notation.md) to resolve ambiguity. Add [execution constraints](../references/execution.md#execution-constraints) when runtime requirements apply.

Define each model element once. Organize concept and synchronization specifications by [engineering ownership](../references/architecture.md#specification-ownership), with all specifications indexed in the overall PRD. Preserve confirmed locations, human notes, and decision records; check references, types, and signatures, and update affected diagrams.
