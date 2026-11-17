# API Refactorings

These cards transform the supplied standard catalog into concise operational guidance for frontend agents. Standard IDs/names are preserved; examples and framework adaptations are original.

## RF-SEPARATE-QUERY-FROM-MODIFIER — Separate Query from Modifier

### Intent
Separate a function that returns information from the operation that changes state.

### Typical Signals
- A caller cannot ask for a value without also triggering mutation/effects.

### Avoid When
- Keep an atomic combined operation when separating it would introduce race conditions or break transactional semantics.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the returned value and mutation.
2. Extract a pure/read-only query for the value.
3. Keep mutation in a command/action.
4. Migrate callers based on whether they need read, write, or both.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-MUTABLE-DATA`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve arity-sensitive callbacks, `this`, default values, thrown errors, and side-effect timing.

### TypeScript Notes
- Treat exported function signatures, generics, overloads, DTOs, and public types as compatibility contracts.

### React Notes
- Props/callback signatures, hooks, loaders/actions, router contracts, and context APIs may be public boundaries.

### Vue Notes
- Props/emits, composable returns, Pinia actions, route contracts, and injection keys may be public boundaries.

### Frontend-Craft Adaptation
- Prefer explicit, testable dependencies. Command objects earn their cost only when state/lifecycle such as undo, queue, retry, or audit justifies them.

### Example Transformation
Before: `getUnreadCountAndMarkSeen()` both reads and mutates. After: expose `getUnreadCount()` and `markSeen()` while preserving workflows that intentionally call both.

## RF-PARAMETERIZE-FUNCTION — Parameterize Function

### Intent
Replace several near-duplicate functions with one function parameterized by the varying value.

### Typical Signals
- Functions differ only by a literal, threshold, mode, or other explicit data.

### Avoid When
- Avoid when the variants represent distinct business concepts whose names are valuable or behavior will diverge.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Compare implementations and isolate the varying value.
2. Add a parameter for that variation.
3. Migrate one old function/caller at a time.
4. Inline/remove wrappers only when names no longer add domain value.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve arity-sensitive callbacks, `this`, default values, thrown errors, and side-effect timing.

### TypeScript Notes
- Treat exported function signatures, generics, overloads, DTOs, and public types as compatibility contracts.

### React Notes
- Props/callback signatures, hooks, loaders/actions, router contracts, and context APIs may be public boundaries.

### Vue Notes
- Props/emits, composable returns, Pinia actions, route contracts, and injection keys may be public boundaries.

### Frontend-Craft Adaptation
- Prefer explicit, testable dependencies. Command objects earn their cost only when state/lifecycle such as undo, queue, retry, or audit justifies them.

### Example Transformation
Before: `loadFirstPage()` and `loadNextPage()` differ only by page index. After: `loadPage(page)` if their policies are truly identical.

## RF-REMOVE-FLAG-ARGUMENT — Remove Flag Argument

### Intent
Replace an argument that selects different behavior with explicit operations or a clearer dispatch API.

### Typical Signals
- A boolean/enum flag tells a function which branch of behavior to execute.

### Avoid When
- Do not remove ordinary data booleans that are part of the domain value rather than a control instruction.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify behavior-selecting flags and affected call sites.
2. Create explicit functions/entry points for meaningful behaviors.
3. Migrate callers from magic boolean/enum values.
4. Remove the flag branch after all callers are clear.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-LONG-PARAMETER-LIST`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve arity-sensitive callbacks, `this`, default values, thrown errors, and side-effect timing.

### TypeScript Notes
- Treat exported function signatures, generics, overloads, DTOs, and public types as compatibility contracts.

### React Notes
- Props/callback signatures, hooks, loaders/actions, router contracts, and context APIs may be public boundaries.

### Vue Notes
- Props/emits, composable returns, Pinia actions, route contracts, and injection keys may be public boundaries.

### Frontend-Craft Adaptation
- Prefer explicit, testable dependencies. Command objects earn their cost only when state/lifecycle such as undo, queue, retry, or audit justifies them.

### Example Transformation
Before: `send(draft, true)` means schedule. After: `scheduleSend(draft)` and `sendNow(draft)` expose intent.

## RF-PRESERVE-WHOLE-OBJECT — Preserve Whole Object

### Intent
Pass the source object when a function needs several of its fields instead of unpacking them into a long parameter list.

### Typical Signals
- Callers extract multiple values from one object solely to pass them together.

### Avoid When
- Avoid when passing the whole object would create an undesirable dependency on a broad mutable/public structure.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify values originating from one object.
2. Change the callee to accept the object while keeping calculation unchanged.
3. Migrate callers.
4. Narrow to an interface/view if the whole object exposes too much.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-LONG-FUNCTION`
- `SMELL-LONG-PARAMETER-LIST`
- `SMELL-DATA-CLUMPS`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve arity-sensitive callbacks, `this`, default values, thrown errors, and side-effect timing.

### TypeScript Notes
- Treat exported function signatures, generics, overloads, DTOs, and public types as compatibility contracts.

### React Notes
- Props/callback signatures, hooks, loaders/actions, router contracts, and context APIs may be public boundaries.

### Vue Notes
- Props/emits, composable returns, Pinia actions, route contracts, and injection keys may be public boundaries.

### Frontend-Craft Adaptation
- Prefer explicit, testable dependencies. Command objects earn their cost only when state/lifecycle such as undo, queue, retry, or audit justifies them.

### Example Transformation
Before: `withinRange(room.temp.low, room.temp.high, plan)` becomes `withinRange(room.temp, plan)` with a typed narrow range contract.

## RF-REPLACE-PARAMETER-WITH-QUERY — Replace Parameter with Query

### Intent
Remove a parameter when the callee can obtain the same value from an appropriate stable source.

### Typical Signals
- Callers repeatedly compute/pass a value that the callee already can derive.

### Avoid When
- Avoid when the query introduces hidden dependency, impurity, nondeterminism, or makes testing harder.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the stable query source.
2. Read the value inside the function.
3. Migrate callers and remove the redundant parameter.
4. Verify dependency visibility and testability.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-LONG-PARAMETER-LIST`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve arity-sensitive callbacks, `this`, default values, thrown errors, and side-effect timing.

### TypeScript Notes
- Treat exported function signatures, generics, overloads, DTOs, and public types as compatibility contracts.

### React Notes
- Props/callback signatures, hooks, loaders/actions, router contracts, and context APIs may be public boundaries.

### Vue Notes
- Props/emits, composable returns, Pinia actions, route contracts, and injection keys may be public boundaries.

### Frontend-Craft Adaptation
- Prefer explicit, testable dependencies. Command objects earn their cost only when state/lifecycle such as undo, queue, retry, or audit justifies them.

### Example Transformation
Before: every caller passes `tenant.locale` into a tenant-owned formatter. After: the formatter queries its explicit tenant context when that dependency is appropriate.

## RF-REPLACE-QUERY-WITH-PARAMETER — Replace Query with Parameter

### Intent
Make a hidden dependency explicit by passing the needed value into a function.

### Typical Signals
- A function queries global/context state that reduces purity, reuse, determinism, or testability.

### Avoid When
- Avoid exploding parameter lists or passing values that are truly intrinsic to the receiver’s responsibility.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the hidden query/dependency.
2. Add a parameter for the needed value or narrow interface.
3. Move the query to callers at the right boundary.
4. Verify callers and avoid duplicating inconsistent query logic.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve arity-sensitive callbacks, `this`, default values, thrown errors, and side-effect timing.

### TypeScript Notes
- Treat exported function signatures, generics, overloads, DTOs, and public types as compatibility contracts.

### React Notes
- Props/callback signatures, hooks, loaders/actions, router contracts, and context APIs may be public boundaries.

### Vue Notes
- Props/emits, composable returns, Pinia actions, route contracts, and injection keys may be public boundaries.

### Frontend-Craft Adaptation
- Prefer explicit, testable dependencies. Command objects earn their cost only when state/lifecycle such as undo, queue, retry, or audit justifies them.

### Example Transformation
Before: a pure formatter reads global timezone. After: pass the resolved timezone from application context so tests and SSR remain deterministic.

## RF-REMOVE-SETTING-METHOD — Remove Setting Method

### Intent
Remove mutation APIs for state that should not change after construction/initialization.

### Typical Signals
- A setter exists but valid usage never changes the value after creation.

### Avoid When
- Do not remove required edit workflows or framework-controlled setters without replacing the legitimate mutation path.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Find all writes and establish the intended invariant.
2. Move required initialization into construction/factory input.
3. Migrate or reject post-construction writes.
4. Remove the setter after callers no longer need it.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-MUTABLE-DATA`
- `SMELL-DATA-CLASS`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve arity-sensitive callbacks, `this`, default values, thrown errors, and side-effect timing.

### TypeScript Notes
- Treat exported function signatures, generics, overloads, DTOs, and public types as compatibility contracts.

### React Notes
- Props/callback signatures, hooks, loaders/actions, router contracts, and context APIs may be public boundaries.

### Vue Notes
- Props/emits, composable returns, Pinia actions, route contracts, and injection keys may be public boundaries.

### Frontend-Craft Adaptation
- Prefer explicit, testable dependencies. Command objects earn their cost only when state/lifecycle such as undo, queue, retry, or audit justifies them.

### Example Transformation
Before: an immutable account ID exposes `setAccountId`. After: require it at creation and expose only a getter/read-only field.

## RF-REPLACE-CONSTRUCTOR-WITH-FACTORY-FUNCTION — Replace Constructor with Factory Function

### Intent
Use a named factory when construction syntax cannot express selection, normalization, caching, or intent clearly.

### Typical Signals
- Creation needs a meaningful name, subtype/strategy choice, normalization, or controlled instance reuse.

### Avoid When
- Avoid adding a factory when `new` is already clear and no creation policy exists.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Create a factory that initially delegates to the constructor.
2. Migrate call sites incrementally.
3. Move creation policy behind the factory only as needed.
4. Restrict direct construction only when the abstraction benefits.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve arity-sensitive callbacks, `this`, default values, thrown errors, and side-effect timing.

### TypeScript Notes
- Treat exported function signatures, generics, overloads, DTOs, and public types as compatibility contracts.

### React Notes
- Props/callback signatures, hooks, loaders/actions, router contracts, and context APIs may be public boundaries.

### Vue Notes
- Props/emits, composable returns, Pinia actions, route contracts, and injection keys may be public boundaries.

### Frontend-Craft Adaptation
- Prefer explicit, testable dependencies. Command objects earn their cost only when state/lifecycle such as undo, queue, retry, or audit justifies them.

### Example Transformation
Before: `new Client(config, "readonly")` becomes `createReadonlyClient(config)` when the factory captures real creation policy.

## RF-REPLACE-FUNCTION-WITH-COMMAND — Replace Function with Command

### Intent
Represent a complex operation as an object/context when it benefits from state, lifecycle, undo, queueing, retry, audit, or staged calculation.

### Typical Signals
- A function carries many temporaries or needs a reusable execution context.

### Avoid When
- Do not introduce Command objects for simple pure calculations; classes are not inherently superior to functions.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Create a command/context that captures inputs.
2. Move the function body into an execute/calculate operation.
3. Extract internal steps/state only when they clarify the lifecycle.
4. Migrate callers and preserve result/error semantics.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-LONG-FUNCTION`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve arity-sensitive callbacks, `this`, default values, thrown errors, and side-effect timing.

### TypeScript Notes
- Treat exported function signatures, generics, overloads, DTOs, and public types as compatibility contracts.

### React Notes
- Props/callback signatures, hooks, loaders/actions, router contracts, and context APIs may be public boundaries.

### Vue Notes
- Props/emits, composable returns, Pinia actions, route contracts, and injection keys may be public boundaries.

### Frontend-Craft Adaptation
- Prefer explicit, testable dependencies. Command objects earn their cost only when state/lifecycle such as undo, queue, retry, or audit justifies them.

### Example Transformation
Before: a complex upload function manages retry, progress, cancellation, and audit state. After: an UploadCommand/session object owns that lifecycle.

## RF-REPLACE-COMMAND-WITH-FUNCTION — Replace Command with Function

### Intent
Collapse a command object to a function when its state/lifecycle no longer justifies the extra abstraction.

### Typical Signals
- A command has one execute method, trivial fields, and no meaningful lifecycle or reuse.

### Avoid When
- Keep commands that genuinely support state, undo, queueing, retry, auditing, or complex staged work.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Inline command helpers until the operation is simple.
2. Convert captured fields to function parameters.
3. Replace construction + execute with a function call.
4. Remove the command after callers migrate.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve arity-sensitive callbacks, `this`, default values, thrown errors, and side-effect timing.

### TypeScript Notes
- Treat exported function signatures, generics, overloads, DTOs, and public types as compatibility contracts.

### React Notes
- Props/callback signatures, hooks, loaders/actions, router contracts, and context APIs may be public boundaries.

### Vue Notes
- Props/emits, composable returns, Pinia actions, route contracts, and injection keys may be public boundaries.

### Frontend-Craft Adaptation
- Prefer explicit, testable dependencies. Command objects earn their cost only when state/lifecycle such as undo, queue, retry, or audit justifies them.

### Example Transformation
Before: a one-shot `TitleFormatterCommand` only stores one string then returns a formatted title. After: use `formatTitle(value)`.
