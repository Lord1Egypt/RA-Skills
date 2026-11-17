# Conditional Logic Refactorings

These cards transform the supplied standard catalog into concise operational guidance for frontend agents. Standard IDs/names are preserved; examples and framework adaptations are original.

## RF-DECOMPOSE-CONDITIONAL — Decompose Conditional

### Intent
Extract a complex condition and its branches into named operations that explain why each path exists.

### Typical Signals
- A conditional mixes domain predicates with substantial branch calculations.

### Avoid When
- Do not scatter tiny helpers when the condition is already simple and self-explanatory.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Extract/name the predicate.
2. Extract the then branch if it has a distinct purpose.
3. Extract the else branch if useful.
4. Verify short-circuiting, side effects, and branch results.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-LONG-FUNCTION`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve short-circuiting, exception timing, side-effect order, and default/fallthrough behavior.

### TypeScript Notes
- Use discriminated unions and `never` exhaustiveness when they clarify variants; assertions are not a substitute for runtime validation.

### React Notes
- Guard clauses must not skip loading cleanup or effect teardown; strategy/component registries often fit variant rendering better than classes.

### Vue Notes
- Preserve `finally`, pending/error state, watcher/effect behavior, and component branch lifecycle.

### Frontend-Craft Adaptation
- “Polymorphism” includes strategies, discriminated-union dispatch, handler/component registries, and delegation; use class hierarchies only when natural.

### Example Transformation
Before: a compose permission `if` embeds tenant/date/quota checks and actions. After: use `canSendNow()` plus named branch functions.

## RF-CONSOLIDATE-CONDITIONAL-EXPRESSION — Consolidate Conditional Expression

### Intent
Combine separate checks that produce the same outcome into one named condition.

### Typical Signals
- Several adjacent conditions return/assign the same result for one conceptual reason.

### Avoid When
- Keep conditions separate when they represent different outcomes, logging, or error reasons users must distinguish.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Confirm branches truly have the same effect.
2. Combine predicates without changing short-circuit order.
3. Extract a named predicate when it clarifies purpose.
4. Verify side effects and error distinctions.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve short-circuiting, exception timing, side-effect order, and default/fallthrough behavior.

### TypeScript Notes
- Use discriminated unions and `never` exhaustiveness when they clarify variants; assertions are not a substitute for runtime validation.

### React Notes
- Guard clauses must not skip loading cleanup or effect teardown; strategy/component registries often fit variant rendering better than classes.

### Vue Notes
- Preserve `finally`, pending/error state, watcher/effect behavior, and component branch lifecycle.

### Frontend-Craft Adaptation
- “Polymorphism” includes strategies, discriminated-union dispatch, handler/component registries, and delegation; use class hierarchies only when natural.

### Example Transformation
Before: three separate guards all disable Send for the same “draft not sendable” outcome. After: combine only if individual user-facing reasons are not lost.

## RF-REPLACE-NESTED-CONDITIONAL-WITH-GUARD-CLAUSES — Replace Nested Conditional with Guard Clauses

### Intent
Flatten exceptional or early-exit cases so the main path is visible.

### Typical Signals
- Nested `if/else` primarily checks invalid/special cases before normal work.

### Avoid When
- Do not return early before required cleanup, `finally`, loading-state reset, or transaction completion.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify cases that can return/throw early.
2. Convert the outermost special case to a guard.
3. Repeat one nesting level at a time.
4. Verify cleanup, loading state, and finally semantics.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve short-circuiting, exception timing, side-effect order, and default/fallthrough behavior.

### TypeScript Notes
- Use discriminated unions and `never` exhaustiveness when they clarify variants; assertions are not a substitute for runtime validation.

### React Notes
- Guard clauses must not skip loading cleanup or effect teardown; strategy/component registries often fit variant rendering better than classes.

### Vue Notes
- Preserve `finally`, pending/error state, watcher/effect behavior, and component branch lifecycle.

### Frontend-Craft Adaptation
- “Polymorphism” includes strategies, discriminated-union dispatch, handler/component registries, and delegation; use class hierarchies only when natural.

### Example Transformation
Before: a submit handler nests auth → draft → recipients → send. After: guard invalid states early while preserving `finally { setLoading(false) }`.

## RF-REPLACE-CONDITIONAL-WITH-POLYMORPHISM — Replace Conditional with Polymorphism

### Intent
Move repeated variant-specific behavior behind a dispatch boundary so each variant owns its behavior.

### Typical Signals
- The same type/status discriminator drives behavior in several locations.

### Avoid When
- Do not replace a single clear conditional with a class hierarchy; frontend dispatch may be simpler as a strategy map or discriminated union.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the stable discriminator and variant behaviors.
2. Choose an idiomatic dispatch form: strategy map, discriminated union, handler/component registry, delegation, or class hierarchy.
3. Move one behavior into the dispatch boundary.
4. Verify exhaustiveness and default/error behavior.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-LONG-FUNCTION`
- `SMELL-PRIMITIVE-OBSESSION`
- `SMELL-REPEATED-SWITCHES`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve short-circuiting, exception timing, side-effect order, and default/fallthrough behavior.

### TypeScript Notes
- Use discriminated unions and `never` exhaustiveness when they clarify variants; assertions are not a substitute for runtime validation.

### React Notes
- Guard clauses must not skip loading cleanup or effect teardown; strategy/component registries often fit variant rendering better than classes.

### Vue Notes
- Preserve `finally`, pending/error state, watcher/effect behavior, and component branch lifecycle.

### Frontend-Craft Adaptation
- “Polymorphism” includes strategies, discriminated-union dispatch, handler/component registries, and delegation; use class hierarchies only when natural.

### Example Transformation
Before: message type switches appear in rendering and actions. After: a typed handler/component registry dispatches by discriminant; no subclass hierarchy is required.

## RF-INTRODUCE-SPECIAL-CASE — Introduce Special Case

### Intent
Represent a recurring exceptional value with an object/value that supplies common behavior, reducing repeated checks.

### Typical Signals
- Many callers repeat the same null/unknown/sentinel handling.

### Avoid When
- Avoid when special-case behavior varies by caller or hiding absence would obscure an error.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. List repeated checks and common behavior.
2. Create the special-case representation.
3. Return it from one boundary and migrate consumers.
4. Remove duplicated checks only after behavior is equivalent.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-TEMPORARY-FIELD`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve short-circuiting, exception timing, side-effect order, and default/fallthrough behavior.

### TypeScript Notes
- Use discriminated unions and `never` exhaustiveness when they clarify variants; assertions are not a substitute for runtime validation.

### React Notes
- Guard clauses must not skip loading cleanup or effect teardown; strategy/component registries often fit variant rendering better than classes.

### Vue Notes
- Preserve `finally`, pending/error state, watcher/effect behavior, and component branch lifecycle.

### Frontend-Craft Adaptation
- “Polymorphism” includes strategies, discriminated-union dispatch, handler/component registries, and delegation; use class hierarchies only when natural.

### Example Transformation
Before: every recipient display checks `contact == null`. After: a stable `UnknownContact`/fallback view model supplies the shared display behavior.

## RF-INTRODUCE-ASSERTION — Introduce Assertion

### Intent
Make an internal invariant executable where violating it indicates a programming error.

### Typical Signals
- Code relies on a condition that is assumed but not expressed.

### Avoid When
- Assertions do not replace user-input validation, network error handling, permissions, or recoverable business errors.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. State the invariant precisely.
2. Place the assertion at the boundary where the assumption must hold.
3. Ensure production/runtime assertion policy is understood.
4. Keep normal validation for expected invalid inputs.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-COMMENTS`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve short-circuiting, exception timing, side-effect order, and default/fallthrough behavior.

### TypeScript Notes
- Use discriminated unions and `never` exhaustiveness when they clarify variants; assertions are not a substitute for runtime validation.

### React Notes
- Guard clauses must not skip loading cleanup or effect teardown; strategy/component registries often fit variant rendering better than classes.

### Vue Notes
- Preserve `finally`, pending/error state, watcher/effect behavior, and component branch lifecycle.

### Frontend-Craft Adaptation
- “Polymorphism” includes strategies, discriminated-union dispatch, handler/component registries, and delegation; use class hierarchies only when natural.

### Example Transformation
Before: an internal normalized draft silently assumes at least one recipient. After: assert that invariant after validated construction, not at raw user input.
