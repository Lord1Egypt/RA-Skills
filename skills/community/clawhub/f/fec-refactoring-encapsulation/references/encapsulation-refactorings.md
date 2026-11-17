# Encapsulation Refactorings

These cards transform the supplied standard catalog into concise operational guidance for frontend agents. Standard IDs/names are preserved; examples and framework adaptations are original.

## RF-ENCAPSULATE-RECORD — Encapsulate Record

### Intent
Replace uncontrolled record access with a boundary that owns representation and allowed operations.

### Typical Signals
- A raw record is widely read/written and representation changes leak to callers.

### Avoid When
- Immutable DTOs at a clear transport boundary may not need behavioral wrapping.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Create an accessor/factory/object boundary around the record.
2. Migrate reads first, then controlled writes.
3. Keep external serialization shape explicit if it is a contract.
4. Change internal representation only after access is controlled.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-DATA-CLASS`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Watch object identity, property descriptors, iteration order, mutability, and serialization.

### TypeScript Notes
- Use `readonly`, narrow interfaces, branded/value types only when they model real invariants; keep DTO translations explicit.

### React Notes
- Preserve props/state identity expectations, memoization, context boundaries, and controlled/uncontrolled contracts.

### Vue Notes
- Preserve reactive proxy identity, computed tracking, store actions, props/emits, and serialization boundaries.

### Frontend-Craft Adaptation
- Encapsulation can be a module API, service, hook/composable, store slice, domain object, or value abstraction; class syntax is optional.

### Example Transformation
Before: UI modules mutate a raw preferences object. After: a preferences model/module exposes named reads and updates while preserving serialized JSON.

## RF-ENCAPSULATE-COLLECTION — Encapsulate Collection

### Intent
Prevent callers from mutating a collection through an uncontrolled reference.

### Typical Signals
- A getter exposes a mutable array/set and callers push/splice/delete directly.

### Avoid When
- Avoid copying or wrapping when the collection is intentionally immutable and ownership is already clear.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Hide the mutable collection behind an owner.
2. Return a read-only view or copy as appropriate.
3. Provide explicit add/remove operations.
4. Migrate direct mutations and verify ordering/identity semantics.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Watch object identity, property descriptors, iteration order, mutability, and serialization.

### TypeScript Notes
- Use `readonly`, narrow interfaces, branded/value types only when they model real invariants; keep DTO translations explicit.

### React Notes
- Preserve props/state identity expectations, memoization, context boundaries, and controlled/uncontrolled contracts.

### Vue Notes
- Preserve reactive proxy identity, computed tracking, store actions, props/emits, and serialization boundaries.

### Frontend-Craft Adaptation
- Encapsulation can be a module API, service, hook/composable, store slice, domain object, or value abstraction; class syntax is optional.

### Example Transformation
Before: `store.items.push(x)` from components becomes `store.addItem(x)` while selectors expose read-only items.

## RF-REPLACE-PRIMITIVE-WITH-OBJECT — Replace Primitive with Object

### Intent
Represent a domain value with an abstraction that owns its formatting, validation, or invariants.

### Typical Signals
- The same primitive is repeatedly validated, formatted, or compared by domain-specific rules.

### Avoid When
- A TypeScript alias or wrapper with no behavior/invariant may add ceremony without value.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the domain behavior around the primitive.
2. Create a small value abstraction with compatible conversion.
3. Migrate creation and use sites incrementally.
4. Keep transport serialization explicit at boundaries.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-PRIMITIVE-OBSESSION`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Watch object identity, property descriptors, iteration order, mutability, and serialization.

### TypeScript Notes
- Use `readonly`, narrow interfaces, branded/value types only when they model real invariants; keep DTO translations explicit.

### React Notes
- Preserve props/state identity expectations, memoization, context boundaries, and controlled/uncontrolled contracts.

### Vue Notes
- Preserve reactive proxy identity, computed tracking, store actions, props/emits, and serialization boundaries.

### Frontend-Craft Adaptation
- Encapsulation can be a module API, service, hook/composable, store slice, domain object, or value abstraction; class syntax is optional.

### Example Transformation
Before: email addresses are raw strings with repeated normalization. After: an `EmailAddress` value abstraction owns normalization; API payloads still serialize strings.

## RF-REPLACE-TEMP-WITH-QUERY — Replace Temp with Query

### Intent
Turn a local derived temporary into a query so the calculation can be reused and extraction boundaries shrink.

### Typical Signals
- A temporary repeats a derivable calculation or must be threaded into extracted functions.

### Avoid When
- Avoid when recomputation is expensive, unstable, or effectful unless memoization/caching preserves semantics.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Confirm the initializer is pure/stable enough to query.
2. Extract the calculation into a function/getter.
3. Replace temporary reads with the query.
4. Remove the temporary and verify evaluation count/performance.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-LONG-FUNCTION`

### Composes Well With
- Extract Function when its preconditions independently hold.

### JavaScript Notes
- Watch object identity, property descriptors, iteration order, mutability, and serialization.

### TypeScript Notes
- Use `readonly`, narrow interfaces, branded/value types only when they model real invariants; keep DTO translations explicit.

### React Notes
- Preserve props/state identity expectations, memoization, context boundaries, and controlled/uncontrolled contracts.

### Vue Notes
- Preserve reactive proxy identity, computed tracking, store actions, props/emits, and serialization boundaries.

### Frontend-Craft Adaptation
- Encapsulation can be a module API, service, hook/composable, store slice, domain object, or value abstraction; class syntax is optional.

### Example Transformation
Before: a handler stores `const normalized = normalizeDraft(draft)` only to pass it around. After: a query supplies the derived value where safe.

## RF-EXTRACT-CLASS — Extract Class

### Intent
Split a responsibility cluster with its own data and behavior into a separate owner.

### Typical Signals
- A class/module/component owns fields and methods that form a distinct concept and change for different reasons.

### Avoid When
- Avoid extracting a thin bag of functions that increases indirection without improving ownership.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the cohesive field/behavior cluster.
2. Create the new owner and move data behind it.
3. Move one behavior at a time.
4. Reduce delegation after callers can use the better boundary.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-DIVERGENT-CHANGE`
- `SMELL-DATA-CLUMPS`
- `SMELL-PRIMITIVE-OBSESSION`
- `SMELL-TEMPORARY-FIELD`
- `SMELL-LARGE-CLASS`

### Composes Well With
- Move Function when its preconditions independently hold.
- Move Field when its preconditions independently hold.

### JavaScript Notes
- Watch object identity, property descriptors, iteration order, mutability, and serialization.

### TypeScript Notes
- Use `readonly`, narrow interfaces, branded/value types only when they model real invariants; keep DTO translations explicit.

### React Notes
- Preserve props/state identity expectations, memoization, context boundaries, and controlled/uncontrolled contracts.

### Vue Notes
- Preserve reactive proxy identity, computed tracking, store actions, props/emits, and serialization boundaries.

### Frontend-Craft Adaptation
- Encapsulation can be a module API, service, hook/composable, store slice, domain object, or value abstraction; class syntax is optional.

### Example Transformation
Before: a compose controller also owns recipient parsing rules. After: move those rules to a recipient domain module/service/composable, not necessarily a class.

## RF-INLINE-CLASS — Inline Class

### Intent
Fold a class or object boundary back into its main user when the abstraction no longer carries enough responsibility.

### Typical Signals
- A type mostly delegates or has become trivial after earlier refactoring.

### Avoid When
- Keep the boundary when it protects a public contract, isolates volatility, or has independent lifecycle/state.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Choose the dominant owner.
2. Move one field/behavior back at a time.
3. Redirect callers and verify.
4. Remove the empty abstraction after all references are migrated.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-SHOTGUN-SURGERY`
- `SMELL-LAZY-ELEMENT`
- `SMELL-SPECULATIVE-GENERALITY`

### Composes Well With
- `RF-EXTRACT-CLASS` when its preconditions independently hold.

### JavaScript Notes
- Watch object identity, property descriptors, iteration order, mutability, and serialization.

### TypeScript Notes
- Use `readonly`, narrow interfaces, branded/value types only when they model real invariants; keep DTO translations explicit.

### React Notes
- Preserve props/state identity expectations, memoization, context boundaries, and controlled/uncontrolled contracts.

### Vue Notes
- Preserve reactive proxy identity, computed tracking, store actions, props/emits, and serialization boundaries.

### Frontend-Craft Adaptation
- Encapsulation can be a module API, service, hook/composable, store slice, domain object, or value abstraction; class syntax is optional.

### Example Transformation
Before: a one-method wrapper service only forwards to an API client. After: its only caller uses the client directly if no policy is lost.

## RF-HIDE-DELEGATE — Hide Delegate

### Intent
Shield clients from a navigation relationship by providing the operation at a stable boundary.

### Typical Signals
- Many clients know the same internal path to reach a collaborator.

### Avoid When
- Avoid wrapping every collaborator method; excessive forwarding creates Middle Man.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Choose the navigation detail to hide.
2. Add one intention-revealing operation on the owner.
3. Migrate clients to the new operation.
4. Stop before the owner becomes a pass-through facade.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-MESSAGE-CHAINS`
- `SMELL-INSIDER-TRADING`

### Composes Well With
- `RF-REMOVE-MIDDLE-MAN` when its preconditions independently hold.

### JavaScript Notes
- Watch object identity, property descriptors, iteration order, mutability, and serialization.

### TypeScript Notes
- Use `readonly`, narrow interfaces, branded/value types only when they model real invariants; keep DTO translations explicit.

### React Notes
- Preserve props/state identity expectations, memoization, context boundaries, and controlled/uncontrolled contracts.

### Vue Notes
- Preserve reactive proxy identity, computed tracking, store actions, props/emits, and serialization boundaries.

### Frontend-Craft Adaptation
- Encapsulation can be a module API, service, hook/composable, store slice, domain object, or value abstraction; class syntax is optional.

### Example Transformation
Before: components read `session.user.organization.policy.canSend`. After: expose `session.canSendMail()` or an equivalent selector.

## RF-REMOVE-MIDDLE-MAN — Remove Middle Man

### Intent
Let clients reach the real collaborator when an intermediary adds mostly forwarding noise.

### Typical Signals
- A wrapper delegates a large portion of its API without policy or protection.

### Avoid When
- Do not expose volatile internals merely to save a few forwarding calls.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify forwarding methods that add no value.
2. Give selected callers direct access to the real collaborator.
3. Migrate and verify callers incrementally.
4. Remove obsolete delegations while preserving useful policy methods.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-MIDDLE-MAN`

### Composes Well With
- `RF-HIDE-DELEGATE` when its preconditions independently hold.

### JavaScript Notes
- Watch object identity, property descriptors, iteration order, mutability, and serialization.

### TypeScript Notes
- Use `readonly`, narrow interfaces, branded/value types only when they model real invariants; keep DTO translations explicit.

### React Notes
- Preserve props/state identity expectations, memoization, context boundaries, and controlled/uncontrolled contracts.

### Vue Notes
- Preserve reactive proxy identity, computed tracking, store actions, props/emits, and serialization boundaries.

### Frontend-Craft Adaptation
- Encapsulation can be a module API, service, hook/composable, store slice, domain object, or value abstraction; class syntax is optional.

### Example Transformation
Before: a hook re-exports every store action unchanged. After: consumers use the store API directly while the hook retains only real composition logic.

## RF-SUBSTITUTE-ALGORITHM — Substitute Algorithm

### Intent
Replace an implementation with a clearer or more suitable algorithm while preserving its externally relevant results.

### Typical Signals
- The current algorithm is convoluted or a simpler proven algorithm expresses the requirement better.

### Avoid When
- Avoid when edge cases, stable ordering, error behavior, or performance constraints are not characterized.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Lock inputs, outputs, ordering, errors, and relevant complexity expectations.
2. Implement the replacement in one isolated boundary.
3. Compare against characterization/tests.
4. Remove the old algorithm only after equivalence is established.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Watch object identity, property descriptors, iteration order, mutability, and serialization.

### TypeScript Notes
- Use `readonly`, narrow interfaces, branded/value types only when they model real invariants; keep DTO translations explicit.

### React Notes
- Preserve props/state identity expectations, memoization, context boundaries, and controlled/uncontrolled contracts.

### Vue Notes
- Preserve reactive proxy identity, computed tracking, store actions, props/emits, and serialization boundaries.

### Frontend-Craft Adaptation
- Encapsulation can be a module API, service, hook/composable, store slice, domain object, or value abstraction; class syntax is optional.

### Example Transformation
Before: a manual nested search builds unique recipients. After: a clearer map/set algorithm produces the same order, duplicates policy, and errors.
