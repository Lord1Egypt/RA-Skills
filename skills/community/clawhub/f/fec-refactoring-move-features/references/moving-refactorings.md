# Moving Feature Refactorings

These cards transform the supplied standard catalog into concise operational guidance for frontend agents. Standard IDs/names are preserved; examples and framework adaptations are original.

## RF-MOVE-FUNCTION — Move Function

### Intent
Move behavior to the module that owns most of the data it uses or the responsibility it represents.

### Typical Signals
- A function depends more on another module’s data than its current home.

### Avoid When
- Do not move orchestration merely because it calls several collaborators; coordination may be its responsibility.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify data ownership and change responsibility.
2. Create/copy the function at the destination with a narrow interface.
3. Delegate from the old location while migrating callers.
4. Remove the old location only when dependencies and public contracts permit.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-DIVERGENT-CHANGE`
- `SMELL-SHOTGUN-SURGERY`
- `SMELL-FEATURE-ENVY`
- `SMELL-TEMPORARY-FIELD`
- `SMELL-MESSAGE-CHAINS`
- `SMELL-INSIDER-TRADING`
- `SMELL-ALTERNATIVE-CLASSES-DIFFERENT-INTERFACES`
- `SMELL-DATA-CLASS`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Module initialization order, circular imports, closures, and dynamic imports can make a textual move behavior-changing.

### TypeScript Notes
- Preserve exported types, path aliases, package boundaries, and type-only/runtime import distinctions.

### React Notes
- Check Hook rules, Server/Client boundaries, lazy components, Suspense, router behavior, and event ordering when moving code.

### Vue Notes
- Check composable lifecycle, Pinia ownership, async setup, route guards, and auto-import conventions.

### Frontend-Craft Adaptation
- Place behavior with the data/change responsibility it serves, not merely in a “utilities” folder; prove dead code with the specialized cleanup lane.

### Example Transformation
Before: a component-local mailbox quota calculation mostly reads account policy data. After: move it to the account policy module and keep UI code declarative.

## RF-MOVE-FIELD — Move Field

### Intent
Move data to the object/module that conceptually owns it and changes with it.

### Typical Signals
- A field is read/updated mainly by another owner or repeatedly travels with another data cluster.

### Avoid When
- Avoid moving a public serialized field without a compatibility plan.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the real owner and all reads/writes.
2. Add storage/access at the destination.
3. Redirect reads and writes incrementally.
4. Remove old storage after state synchronization is no longer required.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-SHOTGUN-SURGERY`
- `SMELL-INSIDER-TRADING`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Module initialization order, circular imports, closures, and dynamic imports can make a textual move behavior-changing.

### TypeScript Notes
- Preserve exported types, path aliases, package boundaries, and type-only/runtime import distinctions.

### React Notes
- Check Hook rules, Server/Client boundaries, lazy components, Suspense, router behavior, and event ordering when moving code.

### Vue Notes
- Check composable lifecycle, Pinia ownership, async setup, route guards, and auto-import conventions.

### Frontend-Craft Adaptation
- Place behavior with the data/change responsibility it serves, not merely in a “utilities” folder; prove dead code with the specialized cleanup lane.

### Example Transformation
Before: a view controller owns `quotaLimit` though policy service controls it. After: policy owns the field and UI reads through the policy boundary.

## RF-MOVE-STATEMENTS-INTO-FUNCTION — Move Statements into Function

### Intent
Move statements that always accompany a function call into that function so the shared operation is complete.

### Typical Signals
- The same setup/teardown statement appears around many calls and belongs to the called operation.

### Avoid When
- Do not move caller-specific policy into a generic function.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Find repeated adjacent statements around the call.
2. Move one shared statement into the callee.
3. Verify callers and ordering.
4. Repeat only for behavior truly common to all callers.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Module initialization order, circular imports, closures, and dynamic imports can make a textual move behavior-changing.

### TypeScript Notes
- Preserve exported types, path aliases, package boundaries, and type-only/runtime import distinctions.

### React Notes
- Check Hook rules, Server/Client boundaries, lazy components, Suspense, router behavior, and event ordering when moving code.

### Vue Notes
- Check composable lifecycle, Pinia ownership, async setup, route guards, and auto-import conventions.

### Frontend-Craft Adaptation
- Place behavior with the data/change responsibility it serves, not merely in a “utilities” folder; prove dead code with the specialized cleanup lane.

### Example Transformation
Before: every caller formats a draft ID immediately before `saveDraft`. After: `saveDraft` owns canonical ID formatting if it is always required.

## RF-MOVE-STATEMENTS-TO-CALLERS — Move Statements to Callers

### Intent
Move behavior out of a function when only some callers need it or its policy varies by context.

### Typical Signals
- A formerly common step is now caller-specific.

### Avoid When
- Avoid duplicating logic when the behavior is still a stable invariant of every caller.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the statement whose policy varies.
2. Expose or split the callee so callers can perform the varying step.
3. Move the statement to one caller at a time.
4. Verify ordering and shared invariants.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Module initialization order, circular imports, closures, and dynamic imports can make a textual move behavior-changing.

### TypeScript Notes
- Preserve exported types, path aliases, package boundaries, and type-only/runtime import distinctions.

### React Notes
- Check Hook rules, Server/Client boundaries, lazy components, Suspense, router behavior, and event ordering when moving code.

### Vue Notes
- Check composable lifecycle, Pinia ownership, async setup, route guards, and auto-import conventions.

### Frontend-Craft Adaptation
- Place behavior with the data/change responsibility it serves, not merely in a “utilities” folder; prove dead code with the specialized cleanup lane.

### Example Transformation
Before: `loadMessages` always shows a toast, but background refresh must not. After: callers decide whether to notify after loading.

## RF-REPLACE-INLINE-CODE-WITH-FUNCTION-CALL — Replace Inline Code with Function Call

### Intent
Use an existing function instead of duplicating equivalent inline logic.

### Typical Signals
- Inline logic already has a trustworthy named implementation elsewhere.

### Avoid When
- Do not replace merely similar logic when semantics or edge cases differ.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Prove equivalence between inline code and the existing function.
2. Replace one occurrence with the call.
3. Verify result, error, and evaluation semantics.
4. Remove any now-unused local helpers.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Module initialization order, circular imports, closures, and dynamic imports can make a textual move behavior-changing.

### TypeScript Notes
- Preserve exported types, path aliases, package boundaries, and type-only/runtime import distinctions.

### React Notes
- Check Hook rules, Server/Client boundaries, lazy components, Suspense, router behavior, and event ordering when moving code.

### Vue Notes
- Check composable lifecycle, Pinia ownership, async setup, route guards, and auto-import conventions.

### Frontend-Craft Adaptation
- Place behavior with the data/change responsibility it serves, not merely in a “utilities” folder; prove dead code with the specialized cleanup lane.

### Example Transformation
Before: an inline loop checks whether a folder is special. After: call the existing `isSpecialFolder(id)` helper when semantics match exactly.

## RF-SLIDE-STATEMENTS — Slide Statements

### Intent
Reorder statements so related code is adjacent and a later extraction or simplification becomes possible.

### Typical Signals
- Statements that belong together are separated by unrelated work.

### Avoid When
- Do not reorder across side effects, awaits, exceptions, subscriptions, or reads/writes whose order is observable.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Map dependencies and side effects between statements.
2. Move the smallest statement across only independent operations.
3. Verify after each move.
4. Stop when the intended cluster is adjacent.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-DUPLICATED-CODE`
- `SMELL-MUTABLE-DATA`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Module initialization order, circular imports, closures, and dynamic imports can make a textual move behavior-changing.

### TypeScript Notes
- Preserve exported types, path aliases, package boundaries, and type-only/runtime import distinctions.

### React Notes
- Check Hook rules, Server/Client boundaries, lazy components, Suspense, router behavior, and event ordering when moving code.

### Vue Notes
- Check composable lifecycle, Pinia ownership, async setup, route guards, and auto-import conventions.

### Frontend-Craft Adaptation
- Place behavior with the data/change responsibility it serves, not merely in a “utilities” folder; prove dead code with the specialized cleanup lane.

### Example Transformation
Before: two normalization statements are separated by an unrelated analytics call. After: move only if analytics timing and data dependencies are unchanged.

## RF-SPLIT-LOOP — Split Loop

### Intent
Separate a loop that performs multiple independent tasks into focused passes.

### Typical Signals
- One loop computes unrelated results with separate accumulators.

### Avoid When
- Avoid when the extra pass is materially expensive or iteration order/side effects couple the tasks.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify independent loop responsibilities.
2. Duplicate the iteration and keep one responsibility in each pass.
3. Verify outputs/order/performance.
4. Then extract or pipeline individual loops if useful.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-LONG-FUNCTION`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Module initialization order, circular imports, closures, and dynamic imports can make a textual move behavior-changing.

### TypeScript Notes
- Preserve exported types, path aliases, package boundaries, and type-only/runtime import distinctions.

### React Notes
- Check Hook rules, Server/Client boundaries, lazy components, Suspense, router behavior, and event ordering when moving code.

### Vue Notes
- Check composable lifecycle, Pinia ownership, async setup, route guards, and auto-import conventions.

### Frontend-Craft Adaptation
- Place behavior with the data/change responsibility it serves, not merely in a “utilities” folder; prove dead code with the specialized cleanup lane.

### Example Transformation
Before: one loop both counts unread messages and builds attachment names. After: split into two focused passes when collection size and order permit.

## RF-REPLACE-LOOP-WITH-PIPELINE — Replace Loop with Pipeline

### Intent
Express a collection transformation as a sequence of named filter/map/reduce-style operations.

### Typical Signals
- An imperative loop mostly filters, maps, or accumulates data and bookkeeping hides intent.

### Avoid When
- Keep loops for early exits, complex mutation, tight performance constraints, or async sequencing when clearer.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the element-level transformation stages.
2. Replace one stage with an equivalent collection operation.
3. Preserve ordering and callback semantics.
4. Verify empty inputs, errors, and performance-sensitive paths.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-LOOPS`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Module initialization order, circular imports, closures, and dynamic imports can make a textual move behavior-changing.

### TypeScript Notes
- Preserve exported types, path aliases, package boundaries, and type-only/runtime import distinctions.

### React Notes
- Check Hook rules, Server/Client boundaries, lazy components, Suspense, router behavior, and event ordering when moving code.

### Vue Notes
- Check composable lifecycle, Pinia ownership, async setup, route guards, and auto-import conventions.

### Frontend-Craft Adaptation
- Place behavior with the data/change responsibility it serves, not merely in a “utilities” folder; prove dead code with the specialized cleanup lane.

### Example Transformation
Before: push matching attachment names into an array inside a loop. After: `attachments.filter(isVisible).map(a => a.name)` when behavior matches.

## RF-REMOVE-DEAD-CODE — Remove Dead Code

### Intent
Remove code proven to have no reachable runtime or supported-tooling use.

### Typical Signals
- A function, export, branch, asset, style, route, or dependency has no legitimate references.

### Avoid When
- Do not infer deadness from grep alone when dynamic imports, routes, Storybook, i18n, Tailwind classes, runtime templates, or external consumers may reference it.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Prove unused status across static and dynamic reference channels.
2. Classify risk before deletion.
3. Use the dedicated cleanup workflow for actual removal.
4. Run relevant build/tests after deletion.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-SPECULATIVE-GENERALITY`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Module initialization order, circular imports, closures, and dynamic imports can make a textual move behavior-changing.

### TypeScript Notes
- Preserve exported types, path aliases, package boundaries, and type-only/runtime import distinctions.

### React Notes
- Check Hook rules, Server/Client boundaries, lazy components, Suspense, router behavior, and event ordering when moving code.

### Vue Notes
- Check composable lifecycle, Pinia ownership, async setup, route guards, and auto-import conventions.

### Frontend-Craft Adaptation
- Place behavior with the data/change responsibility it serves, not merely in a “utilities” folder; prove dead code with the specialized cleanup lane.

### Example Transformation
Before: an obsolete component appears unused. After: route actual proof and deletion through `fec-refactor-clean`, including dynamic-reference checks.
