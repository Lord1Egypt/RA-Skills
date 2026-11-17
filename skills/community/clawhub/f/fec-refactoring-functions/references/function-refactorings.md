# Function Refactorings

These cards transform the supplied standard catalog into concise operational guidance for frontend agents. Standard IDs/names are preserved; examples and framework adaptations are original.

## RF-EXTRACT-FUNCTION — Extract Function

### Intent
Move a coherent fragment into a well-named function so the caller reads in terms of intent.

### Typical Signals
- A block has a distinct purpose that can be named; comments divide a function into concepts.

### Avoid When
- Do not extract when the new function would merely hide a trivial expression without adding a useful name.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the coherent statements and their inputs/outputs.
2. Create a function named for purpose rather than implementation.
3. Move the statements and replace them with the call.
4. Run narrow verification before any further extraction.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-DUPLICATED-CODE`
- `SMELL-LONG-FUNCTION`
- `SMELL-MUTABLE-DATA`
- `SMELL-DIVERGENT-CHANGE`
- `SMELL-FEATURE-ENVY`
- `SMELL-MESSAGE-CHAINS`
- `SMELL-DATA-CLASS`
- `SMELL-COMMENTS`

### Composes Well With
- Move Function when its preconditions independently hold.
- Replace Temp with Query when its preconditions independently hold.

### JavaScript Notes
- Preserve JavaScript evaluation order, closures, `this`, default parameters, rest/spread, and side effects.

### TypeScript Notes
- Use typed parameter objects and keep inference/public signatures stable; do not silence errors with casts.

### React Notes
- For React, extracted helpers must not violate Hook rules or capture stale values; keep event/effect ordering stable.

### Vue Notes
- For Vue, preserve `ref`/`reactive` unwrapping, computed dependencies, and composable lifecycle scope.

### Frontend-Craft Adaptation
- Prefer helpers, handlers, modules, hooks/composables, or services when they express the same intent more naturally than classes.

### Example Transformation
Before: a submit handler validates recipients, normalizes payload, then sends. After: extract `validateRecipients()` while preserving the same errors and order.

## RF-INLINE-FUNCTION — Inline Function

### Intent
Remove a function boundary whose body is clearer than its name or whose indirection blocks better restructuring.

### Typical Signals
- A function only delegates or its name adds no semantic value.

### Avoid When
- Keep a small function when its name is the useful abstraction, a test seam, or a stable public contract.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Check all callers and whether the function is overridden/exported.
2. Replace one caller with the body and verify.
3. Repeat for remaining safe callers.
4. Remove the declaration only after all references are resolved.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-SHOTGUN-SURGERY`
- `SMELL-LAZY-ELEMENT`
- `SMELL-SPECULATIVE-GENERALITY`
- `SMELL-MIDDLE-MAN`

### Composes Well With
- `RF-EXTRACT-FUNCTION` when its preconditions independently hold.

### JavaScript Notes
- Preserve JavaScript evaluation order, closures, `this`, default parameters, rest/spread, and side effects.

### TypeScript Notes
- Use typed parameter objects and keep inference/public signatures stable; do not silence errors with casts.

### React Notes
- For React, extracted helpers must not violate Hook rules or capture stale values; keep event/effect ordering stable.

### Vue Notes
- For Vue, preserve `ref`/`reactive` unwrapping, computed dependencies, and composable lifecycle scope.

### Frontend-Craft Adaptation
- Prefer helpers, handlers, modules, hooks/composables, or services when they express the same intent more naturally than classes.

### Example Transformation
Before: `isEmptyName(v)` only returns `!v.trim()`. After: inline the expression where that makes the surrounding guard clearer.

## RF-EXTRACT-VARIABLE — Extract Variable

### Intent
Name an important subexpression so a complex calculation or condition exposes its concepts.

### Typical Signals
- A long expression contains meaningful parts that readers must mentally decode.

### Avoid When
- Avoid names that merely restate syntax or force readers to bounce between lines.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Select a stable subexpression.
2. Introduce a `const` with an intent-revealing name.
3. Replace matching occurrences where evaluation semantics stay the same.
4. Verify evaluation count and short-circuit behavior.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- `RF-INLINE-VARIABLE` when its preconditions independently hold.

### JavaScript Notes
- Preserve JavaScript evaluation order, closures, `this`, default parameters, rest/spread, and side effects.

### TypeScript Notes
- Use typed parameter objects and keep inference/public signatures stable; do not silence errors with casts.

### React Notes
- For React, extracted helpers must not violate Hook rules or capture stale values; keep event/effect ordering stable.

### Vue Notes
- For Vue, preserve `ref`/`reactive` unwrapping, computed dependencies, and composable lifecycle scope.

### Frontend-Craft Adaptation
- Prefer helpers, handlers, modules, hooks/composables, or services when they express the same intent more naturally than classes.

### Example Transformation
Before: a JSX condition repeats `user.permissions.includes("mail.send")`. After: introduce `canSendMail` and render from that name.

## RF-INLINE-VARIABLE — Inline Variable

### Intent
Remove a temporary variable that obscures a simple expression or blocks another refactoring.

### Typical Signals
- A variable is assigned once and its name adds less clarity than the expression.

### Avoid When
- Do not inline when it duplicates expensive/effectful evaluation or removes a useful domain name.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Confirm the initializer is stable and side-effect semantics are unchanged.
2. Replace reads with the initializer.
3. Remove the declaration.
4. Verify evaluation count and type inference.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- `RF-EXTRACT-VARIABLE` when its preconditions independently hold.

### JavaScript Notes
- Preserve JavaScript evaluation order, closures, `this`, default parameters, rest/spread, and side effects.

### TypeScript Notes
- Use typed parameter objects and keep inference/public signatures stable; do not silence errors with casts.

### React Notes
- For React, extracted helpers must not violate Hook rules or capture stale values; keep event/effect ordering stable.

### Vue Notes
- For Vue, preserve `ref`/`reactive` unwrapping, computed dependencies, and composable lifecycle scope.

### Frontend-Craft Adaptation
- Prefer helpers, handlers, modules, hooks/composables, or services when they express the same intent more naturally than classes.

### Example Transformation
Before: `const result = draft.subject.trim(); return result;`. After: return `draft.subject.trim()` directly.

## RF-CHANGE-FUNCTION-DECLARATION — Change Function Declaration

### Intent
Make a function name or parameter contract better express how callers should use it.

### Typical Signals
- A name is misleading, parameters are missing/unused, or callers need a clearer contract.

### Avoid When
- Do not casually change exported/public signatures, framework callback contracts, or externally consumed APIs.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Map all callers and public boundaries.
2. Introduce the new name/signature, using a compatibility shim when needed.
3. Migrate callers in small verified steps.
4. Remove the old form only when compatibility requirements allow.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-MYSTERIOUS-NAME`
- `SMELL-SPECULATIVE-GENERALITY`
- `SMELL-ALTERNATIVE-CLASSES-DIFFERENT-INTERFACES`
- `SMELL-COMMENTS`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve JavaScript evaluation order, closures, `this`, default parameters, rest/spread, and side effects.

### TypeScript Notes
- Use typed parameter objects and keep inference/public signatures stable; do not silence errors with casts.

### React Notes
- For React, extracted helpers must not violate Hook rules or capture stale values; keep event/effect ordering stable.

### Vue Notes
- For Vue, preserve `ref`/`reactive` unwrapping, computed dependencies, and composable lifecycle scope.

### Frontend-Craft Adaptation
- Prefer helpers, handlers, modules, hooks/composables, or services when they express the same intent more naturally than classes.

### Example Transformation
Before: private `send(data, true)` becomes `sendUrgently(data)` or a clearer signature; public APIs keep a compatibility path when required.

## RF-ENCAPSULATE-VARIABLE — Encapsulate Variable

### Intent
Route access to a variable through an explicit boundary so reads and writes can be controlled.

### Typical Signals
- A shared variable can be mutated from many locations or representation changes are difficult.

### Avoid When
- Do not add ceremonial getters around genuinely local constants.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Create a controlled read/write API around the variable.
2. Migrate one access path at a time.
3. Restrict direct access after callers are migrated.
4. Then change representation or ownership behind the seam if useful.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-GLOBAL-DATA`
- `SMELL-MUTABLE-DATA`

### Composes Well With
- `RF-RENAME-VARIABLE` when its preconditions independently hold.
- Move Function when its preconditions independently hold.

### JavaScript Notes
- Preserve JavaScript evaluation order, closures, `this`, default parameters, rest/spread, and side effects.

### TypeScript Notes
- Use typed parameter objects and keep inference/public signatures stable; do not silence errors with casts.

### React Notes
- For React, extracted helpers must not violate Hook rules or capture stale values; keep event/effect ordering stable.

### Vue Notes
- For Vue, preserve `ref`/`reactive` unwrapping, computed dependencies, and composable lifecycle scope.

### Frontend-Craft Adaptation
- Prefer helpers, handlers, modules, hooks/composables, or services when they express the same intent more naturally than classes.

### Example Transformation
Before: modules assign `currentTenant` directly. After: expose `getCurrentTenant()` / `setCurrentTenant()` or a store action boundary.

## RF-RENAME-VARIABLE — Rename Variable

### Intent
Give a variable a name that communicates its role and domain meaning.

### Typical Signals
- Readers must infer meaning from context; the name is generic, stale, or misleading.

### Avoid When
- Do not churn stable domain vocabulary without evidence of confusion.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Choose the domain-accurate name.
2. Rename the declaration and all statically verified references.
3. Check string-based/dynamic references where relevant.
4. Run type/lint/tests for the affected scope.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-MYSTERIOUS-NAME`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve JavaScript evaluation order, closures, `this`, default parameters, rest/spread, and side effects.

### TypeScript Notes
- Use typed parameter objects and keep inference/public signatures stable; do not silence errors with casts.

### React Notes
- For React, extracted helpers must not violate Hook rules or capture stale values; keep event/effect ordering stable.

### Vue Notes
- For Vue, preserve `ref`/`reactive` unwrapping, computed dependencies, and composable lifecycle scope.

### Frontend-Craft Adaptation
- Prefer helpers, handlers, modules, hooks/composables, or services when they express the same intent more naturally than classes.

### Example Transformation
Before: `let d` in a date-range calculation becomes `billingPeriodEnd` when that is the actual meaning.

## RF-INTRODUCE-PARAMETER-OBJECT — Introduce Parameter Object

### Intent
Group parameters that form one concept into a named object contract.

### Typical Signals
- Several values repeatedly travel together or their relationships are hidden by positional arguments.

### Avoid When
- Avoid a bag-of-options object when values are unrelated or the object only makes a one-off call less explicit.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the stable parameter cluster.
2. Define an object/options shape with meaningful field names.
3. Add the object parameter and migrate callers.
4. Move behavior into the object only when invariants or domain behavior justify it.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-LONG-FUNCTION`
- `SMELL-LONG-PARAMETER-LIST`
- `SMELL-DATA-CLUMPS`
- `SMELL-PRIMITIVE-OBSESSION`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve JavaScript evaluation order, closures, `this`, default parameters, rest/spread, and side effects.

### TypeScript Notes
- Use typed parameter objects and keep inference/public signatures stable; do not silence errors with casts.

### React Notes
- For React, extracted helpers must not violate Hook rules or capture stale values; keep event/effect ordering stable.

### Vue Notes
- For Vue, preserve `ref`/`reactive` unwrapping, computed dependencies, and composable lifecycle scope.

### Frontend-Craft Adaptation
- Prefer helpers, handlers, modules, hooks/composables, or services when they express the same intent more naturally than classes.

### Example Transformation
Before: `loadMessages(folderId, page, size, sort)` becomes `loadMessages({ folderId, page, size, sort })` with a typed request shape.

## RF-COMBINE-FUNCTIONS-INTO-CLASS — Combine Functions into Class

### Intent
Place functions that operate on shared data behind one cohesive context so their relationship is explicit.

### Typical Signals
- Several functions repeatedly accept the same data and calculate related results.

### Avoid When
- Do not force a class when a module, closure, hook, composable, or service provides the clearer frontend abstraction.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the shared data/context and related functions.
2. Create the smallest cohesive owner for that context.
3. Move one function at a time while preserving outputs.
4. Choose class/module/hook/composable/service based on existing architecture.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-LONG-PARAMETER-LIST`
- `SMELL-MUTABLE-DATA`
- `SMELL-SHOTGUN-SURGERY`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve JavaScript evaluation order, closures, `this`, default parameters, rest/spread, and side effects.

### TypeScript Notes
- Use typed parameter objects and keep inference/public signatures stable; do not silence errors with casts.

### React Notes
- For React, extracted helpers must not violate Hook rules or capture stale values; keep event/effect ordering stable.

### Vue Notes
- For Vue, preserve `ref`/`reactive` unwrapping, computed dependencies, and composable lifecycle scope.

### Frontend-Craft Adaptation
- Prefer helpers, handlers, modules, hooks/composables, or services when they express the same intent more naturally than classes.

### Example Transformation
Before: several pricing helpers all take the same quote. After: expose a cohesive pricing module or `useQuotePricing()` rather than mechanically introducing a class.

## RF-COMBINE-FUNCTIONS-INTO-TRANSFORM — Combine Functions into Transform

### Intent
Collect related derived calculations into a transform that returns the enriched result together.

### Typical Signals
- Many functions derive values from the same immutable input and callers need several of them.

### Avoid When
- Avoid when derivations are effectful, expensive but rarely used, or require independent lifecycle timing.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Define the input and derived output fields.
2. Create a pure transform that copies/enriches rather than mutating the input.
3. Move one calculation at a time into the transform.
4. Verify derived values and object identity expectations.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-MUTABLE-DATA`
- `SMELL-SHOTGUN-SURGERY`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve JavaScript evaluation order, closures, `this`, default parameters, rest/spread, and side effects.

### TypeScript Notes
- Use typed parameter objects and keep inference/public signatures stable; do not silence errors with casts.

### React Notes
- For React, extracted helpers must not violate Hook rules or capture stale values; keep event/effect ordering stable.

### Vue Notes
- For Vue, preserve `ref`/`reactive` unwrapping, computed dependencies, and composable lifecycle scope.

### Frontend-Craft Adaptation
- Prefer helpers, handlers, modules, hooks/composables, or services when they express the same intent more naturally than classes.

### Example Transformation
Before: multiple selectors derive displayName, initials, and domain from one contact DTO. After: `toContactViewModel(dto)` returns the enriched view model.

## RF-SPLIT-PHASE — Split Phase

### Intent
Separate sequential concerns so each phase has a clear input/output boundary.

### Typical Signals
- One routine performs conceptually distinct stages whose intermediate data can be named.

### Avoid When
- Avoid splitting tightly interleaved work when the intermediate contract would be more complex than the original.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the phase boundary and intermediate data.
2. Extract the later phase first behind an explicit input.
3. Extract/normalize the earlier phase.
4. Verify phase ordering, errors, and side effects.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-DIVERGENT-CHANGE`
- `SMELL-SHOTGUN-SURGERY`
- `SMELL-DATA-CLASS`

### Composes Well With
- `RF-EXTRACT-FUNCTION` when its preconditions independently hold.
- Move Function when its preconditions independently hold.

### JavaScript Notes
- Preserve JavaScript evaluation order, closures, `this`, default parameters, rest/spread, and side effects.

### TypeScript Notes
- Use typed parameter objects and keep inference/public signatures stable; do not silence errors with casts.

### React Notes
- For React, extracted helpers must not violate Hook rules or capture stale values; keep event/effect ordering stable.

### Vue Notes
- For Vue, preserve `ref`/`reactive` unwrapping, computed dependencies, and composable lifecycle scope.

### Frontend-Craft Adaptation
- Prefer helpers, handlers, modules, hooks/composables, or services when they express the same intent more naturally than classes.

### Example Transformation
Before: one submit function parses, normalizes, validates, and sends. After: `parse → normalize → validate → submit`, preserving error order.
