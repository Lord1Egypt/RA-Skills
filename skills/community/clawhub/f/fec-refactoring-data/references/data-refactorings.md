# Data Refactorings

These cards transform the supplied standard catalog into concise operational guidance for frontend agents. Standard IDs/names are preserved; examples and framework adaptations are original.

## RF-SPLIT-VARIABLE — Split Variable

### Intent
Give distinct assignments distinct variables when one variable currently represents more than one thing.

### Typical Signals
- A local variable is reassigned for unrelated purposes or a parameter is overwritten.

### Avoid When
- Loop counters or deliberate accumulators are not automatically candidates.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify each semantic role of the variable.
2. Introduce a separate variable for the later role.
3. Replace reads belonging to that role.
4. Repeat until each variable has one meaning.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-MUTABLE-DATA`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve equality, identity, mutation timing, serialization, and property access semantics.

### TypeScript Notes
- Model reference/value intent with `readonly`, narrow domain types, and explicit DTO adapters rather than unsafe casts.

### React Notes
- Object identity can affect state updates, memoization, dependency arrays, selectors, and reconciliation.

### Vue Notes
- Proxy/reference identity affects `reactive`, `ref`, `computed`, `watch`, Pinia subscriptions, and template updates.

### Frontend-Craft Adaptation
- Treat state identity as observable frontend behavior; choose value/reference semantics deliberately.

### Example Transformation
Before: `result` first stores normalized input and later stores API output. After: use `normalizedDraft` and `response`.

## RF-RENAME-FIELD — Rename Field

### Intent
Rename a field so the data model uses accurate domain vocabulary.

### Typical Signals
- A field name is ambiguous, misleading, or no longer matches the concept.

### Avoid When
- Treat DTO, persisted storage, URL/query, analytics, and backend field names as contracts unless a compatibility mapping exists.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Map internal and serialized/external uses.
2. Add the new field/accessor or translation at the boundary.
3. Migrate internal reads/writes.
4. Remove old compatibility only when consumers are migrated.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-MYSTERIOUS-NAME`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve equality, identity, mutation timing, serialization, and property access semantics.

### TypeScript Notes
- Model reference/value intent with `readonly`, narrow domain types, and explicit DTO adapters rather than unsafe casts.

### React Notes
- Object identity can affect state updates, memoization, dependency arrays, selectors, and reconciliation.

### Vue Notes
- Proxy/reference identity affects `reactive`, `ref`, `computed`, `watch`, Pinia subscriptions, and template updates.

### Frontend-Craft Adaptation
- Treat state identity as observable frontend behavior; choose value/reference semantics deliberately.

### Example Transformation
Before: internal `mailId` actually means thread ID. After: rename to `threadId` internally while preserving backend DTO mapping if the API still sends `mailId`.

## RF-REPLACE-DERIVED-VARIABLE-WITH-QUERY — Replace Derived Variable with Query

### Intent
Compute derived state from its source instead of manually keeping a stored duplicate synchronized.

### Typical Signals
- A stored field can be deterministically derived and update paths can drift.

### Avoid When
- Avoid naive recomputation when the calculation is expensive; use memoization only if identity/dependency semantics are understood.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Define the derivation as a query/computed value.
2. Replace reads of stored derived state.
3. Remove synchronization writes.
4. Verify recomputation cost, memoization, and reactive dependencies.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-MUTABLE-DATA`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve equality, identity, mutation timing, serialization, and property access semantics.

### TypeScript Notes
- Model reference/value intent with `readonly`, narrow domain types, and explicit DTO adapters rather than unsafe casts.

### React Notes
- Object identity can affect state updates, memoization, dependency arrays, selectors, and reconciliation.

### Vue Notes
- Proxy/reference identity affects `reactive`, `ref`, `computed`, `watch`, Pinia subscriptions, and template updates.

### Frontend-Craft Adaptation
- Treat state identity as observable frontend behavior; choose value/reference semantics deliberately.

### Example Transformation
Before: React state stores both `items` and `totalCount = items.length`. After: derive the count, using memoization only if the real calculation warrants it.

## RF-CHANGE-REFERENCE-TO-VALUE — Change Reference to Value

### Intent
Use immutable value semantics when objects are defined entirely by their data and shared identity is unnecessary.

### Typical Signals
- Equivalent values should compare by content and independent replacement is safer than shared mutation.

### Avoid When
- Avoid when shared identity, lifecycle, caching, subscriptions, or coordinated updates are meaningful.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify identity-dependent behavior.
2. Make the value immutable and define equality/creation semantics.
3. Replace mutation with replacement.
4. Verify React/Vue equality/reactivity and cache behavior.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-MUTABLE-DATA`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve equality, identity, mutation timing, serialization, and property access semantics.

### TypeScript Notes
- Model reference/value intent with `readonly`, narrow domain types, and explicit DTO adapters rather than unsafe casts.

### React Notes
- Object identity can affect state updates, memoization, dependency arrays, selectors, and reconciliation.

### Vue Notes
- Proxy/reference identity affects `reactive`, `ref`, `computed`, `watch`, Pinia subscriptions, and template updates.

### Frontend-Craft Adaptation
- Treat state identity as observable frontend behavior; choose value/reference semantics deliberately.

### Example Transformation
Before: a mutable `DateRange` object is shared and changed in place. After: immutable ranges are replaced as values when no shared identity is required.

## RF-CHANGE-VALUE-TO-REFERENCE — Change Value to Reference

### Intent
Use a canonical shared object when identity and coordinated updates matter more than independent copies.

### Typical Signals
- Multiple copies represent the same entity and must stay synchronized.

### Avoid When
- Avoid introducing a global identity map when values are naturally independent snapshots.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Choose a stable identity key and owner/registry.
2. Resolve values to the canonical reference.
3. Migrate consumers incrementally.
4. Verify update propagation, cache lifetime, and serialization boundaries.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve equality, identity, mutation timing, serialization, and property access semantics.

### TypeScript Notes
- Model reference/value intent with `readonly`, narrow domain types, and explicit DTO adapters rather than unsafe casts.

### React Notes
- Object identity can affect state updates, memoization, dependency arrays, selectors, and reconciliation.

### Vue Notes
- Proxy/reference identity affects `reactive`, `ref`, `computed`, `watch`, Pinia subscriptions, and template updates.

### Frontend-Craft Adaptation
- Treat state identity as observable frontend behavior; choose value/reference semantics deliberately.

### Example Transformation
Before: each message stores a copied sender object. After: sender IDs resolve to canonical contact entities when shared updates must propagate.
