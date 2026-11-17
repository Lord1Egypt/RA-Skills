# Inheritance Refactorings

These cards transform the supplied standard catalog into concise operational guidance for frontend agents. Standard IDs/names are preserved; examples and framework adaptations are original.

## RF-PULL-UP-METHOD — Pull Up Method

### Intent
Move equivalent subclass behavior to a superclass when it is truly shared.

### Typical Signals
- Sibling subclasses contain the same behavior or behavior that can be generalized without type checks.

### Avoid When
- Do not pull up code that only looks similar but depends on subtype-specific semantics.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Compare implementations and make differences explicit.
2. Align signatures/fields needed by the shared method.
3. Move one shared implementation to the superclass.
4. Remove duplicates and verify substitutability.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-DUPLICATED-CODE`

### Composes Well With
- `RF-PUSH-DOWN-METHOD` when its preconditions independently hold.

### JavaScript Notes
- Preserve prototype behavior, constructor order, `instanceof`, method binding, and super calls in legacy OO code.

### TypeScript Notes
- Track structural typing, discriminated unions, abstract contracts, visibility, and public subtype APIs.

### React Notes
- React components should normally use composition, hooks, render props, or delegates rather than class inheritance.

### Vue Notes
- Vue components should normally use composition, composables, slots, and delegation rather than inheritance.

### Frontend-Craft Adaptation
- These techniques primarily serve genuine legacy OO JS/TS, domain models, SDKs, and editor engines; translate intent to composition when frontend architecture is composition-first.

### Example Transformation
Before: two legacy editor subclasses implement identical `isDirty()`. After: the base editor owns it if both contracts are truly the same.

## RF-PULL-UP-FIELD — Pull Up Field

### Intent
Move duplicated subclass state to a superclass when every relevant subtype owns the same concept.

### Typical Signals
- Sibling subclasses declare the same field with the same meaning.

### Avoid When
- Do not pull up fields that merely share a name but have different invariants or lifecycles.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Confirm semantic equivalence and initialization.
2. Add the field to the superclass.
3. Redirect subclass initialization/access.
4. Remove duplicate fields.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- `RF-PUSH-DOWN-FIELD` when its preconditions independently hold.

### JavaScript Notes
- Preserve prototype behavior, constructor order, `instanceof`, method binding, and super calls in legacy OO code.

### TypeScript Notes
- Track structural typing, discriminated unions, abstract contracts, visibility, and public subtype APIs.

### React Notes
- React components should normally use composition, hooks, render props, or delegates rather than class inheritance.

### Vue Notes
- Vue components should normally use composition, composables, slots, and delegation rather than inheritance.

### Frontend-Craft Adaptation
- These techniques primarily serve genuine legacy OO JS/TS, domain models, SDKs, and editor engines; translate intent to composition when frontend architecture is composition-first.

### Example Transformation
Before: several legacy transport subclasses keep the same `endpoint` state. After: the common base owns it if semantics match.

## RF-PULL-UP-CONSTRUCTOR-BODY — Pull Up Constructor Body

### Intent
Move common subclass initialization into the superclass while leaving variant initialization in subclasses.

### Typical Signals
- Subclass constructors repeat the same base-field setup.

### Avoid When
- Avoid moving initialization that depends on subtype-only state before it is ready.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Align common constructor parameters.
2. Move one common initialization step to `super`/base initialization.
3. Keep subtype-specific steps after the base is valid.
4. Verify construction order and overridden-method hazards.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve prototype behavior, constructor order, `instanceof`, method binding, and super calls in legacy OO code.

### TypeScript Notes
- Track structural typing, discriminated unions, abstract contracts, visibility, and public subtype APIs.

### React Notes
- React components should normally use composition, hooks, render props, or delegates rather than class inheritance.

### Vue Notes
- Vue components should normally use composition, composables, slots, and delegation rather than inheritance.

### Frontend-Craft Adaptation
- These techniques primarily serve genuine legacy OO JS/TS, domain models, SDKs, and editor engines; translate intent to composition when frontend architecture is composition-first.

### Example Transformation
Before: two legacy provider subclasses both initialize id/name before provider-specific config. After: base construction handles common identity.

## RF-PUSH-DOWN-METHOD — Push Down Method

### Intent
Move behavior from a superclass to the subclass(es) that actually need it.

### Typical Signals
- A superclass method is meaningful only for a subset of subtypes.

### Avoid When
- Do not push down merely because some subclasses do not call a valid shared method.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the true owning subtype set.
2. Move/copy the method to those subtypes.
3. Update base contract if necessary.
4. Verify callers no longer rely on the broad superclass API.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-REFUSED-BEQUEST`

### Composes Well With
- `RF-PULL-UP-METHOD` when its preconditions independently hold.

### JavaScript Notes
- Preserve prototype behavior, constructor order, `instanceof`, method binding, and super calls in legacy OO code.

### TypeScript Notes
- Track structural typing, discriminated unions, abstract contracts, visibility, and public subtype APIs.

### React Notes
- React components should normally use composition, hooks, render props, or delegates rather than class inheritance.

### Vue Notes
- Vue components should normally use composition, composables, slots, and delegation rather than inheritance.

### Frontend-Craft Adaptation
- These techniques primarily serve genuine legacy OO JS/TS, domain models, SDKs, and editor engines; translate intent to composition when frontend architecture is composition-first.

### Example Transformation
Before: a base editor exposes `exportToPdf()` but only document editors support it. After: move it to the appropriate subtype or capability delegate.

## RF-PUSH-DOWN-FIELD — Push Down Field

### Intent
Move state from a superclass to only the subclasses that require it.

### Typical Signals
- A base field is unused or invalid for most subtypes.

### Avoid When
- Do not narrow a field that is part of a valid shared contract even if some subtypes rarely use it.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Map field reads/writes by subtype.
2. Add the field to the real owner subtype.
3. Move initialization/access.
4. Remove the base field and verify construction/serialization.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-REFUSED-BEQUEST`

### Composes Well With
- `RF-PULL-UP-FIELD` when its preconditions independently hold.

### JavaScript Notes
- Preserve prototype behavior, constructor order, `instanceof`, method binding, and super calls in legacy OO code.

### TypeScript Notes
- Track structural typing, discriminated unions, abstract contracts, visibility, and public subtype APIs.

### React Notes
- React components should normally use composition, hooks, render props, or delegates rather than class inheritance.

### Vue Notes
- Vue components should normally use composition, composables, slots, and delegation rather than inheritance.

### Frontend-Craft Adaptation
- These techniques primarily serve genuine legacy OO JS/TS, domain models, SDKs, and editor engines; translate intent to composition when frontend architecture is composition-first.

### Example Transformation
Before: base transport stores `imapFolder` though only IMAP transport uses it. After: the IMAP subtype owns that field.

## RF-REPLACE-TYPE-CODE-WITH-SUBCLASSES — Replace Type Code with Subclasses

### Intent
Represent stable variant-specific behavior with subtype-like alternatives instead of repeated type-code branching.

### Typical Signals
- A type code controls substantial behavior and new variants repeatedly change the same branch sets.

### Avoid When
- In modern frontend code, do not force inheritance; discriminated unions, strategy maps, component registries, or delegates may be the better subtype mechanism.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify the stable type discriminator and variant boundaries.
2. Introduce one variant representation at a time.
3. Move type-specific behavior behind variant dispatch.
4. Remove repeated type-code checks only after exhaustive handling is proven.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-PRIMITIVE-OBSESSION`
- `SMELL-LARGE-CLASS`

### Composes Well With
- Replace Conditional with Polymorphism when its preconditions independently hold.
- `RF-REMOVE-SUBCLASS` when its preconditions independently hold.

### JavaScript Notes
- Preserve prototype behavior, constructor order, `instanceof`, method binding, and super calls in legacy OO code.

### TypeScript Notes
- Track structural typing, discriminated unions, abstract contracts, visibility, and public subtype APIs.

### React Notes
- React components should normally use composition, hooks, render props, or delegates rather than class inheritance.

### Vue Notes
- Vue components should normally use composition, composables, slots, and delegation rather than inheritance.

### Frontend-Craft Adaptation
- These techniques primarily serve genuine legacy OO JS/TS, domain models, SDKs, and editor engines; translate intent to composition when frontend architecture is composition-first.

### Example Transformation
Before: editor mode strings drive repeated switches. After: use a discriminated union + strategy registry, or subclasses only in a genuine OO domain model.

## RF-REMOVE-SUBCLASS — Remove Subclass

### Intent
Remove subclasses whose variation no longer warrants separate types, preserving the distinction as data or simpler behavior when needed.

### Typical Signals
- Subclasses differ only trivially or a former behavior distinction has disappeared.

### Avoid When
- Keep subclasses when substitutable behavior remains materially different and the hierarchy is useful.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Move unique behavior/state to the superclass or an explicit field/strategy.
2. Migrate construction to the unified type.
3. Update callers that inspect subtype identity.
4. Remove subclass declarations after behavior is covered.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- No single code smell required; select from concrete structural evidence.

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve prototype behavior, constructor order, `instanceof`, method binding, and super calls in legacy OO code.

### TypeScript Notes
- Track structural typing, discriminated unions, abstract contracts, visibility, and public subtype APIs.

### React Notes
- React components should normally use composition, hooks, render props, or delegates rather than class inheritance.

### Vue Notes
- Vue components should normally use composition, composables, slots, and delegation rather than inheritance.

### Frontend-Craft Adaptation
- These techniques primarily serve genuine legacy OO JS/TS, domain models, SDKs, and editor engines; translate intent to composition when frontend architecture is composition-first.

### Example Transformation
Before: two legacy account subclasses differ only by a display label. After: one account type stores the label/type value when no variant behavior remains.

## RF-EXTRACT-SUPERCLASS — Extract Superclass

### Intent
Factor genuinely shared data/behavior from classes into a common abstraction.

### Typical Signals
- Two or more classes independently implement the same concept and substitutability is useful.

### Avoid When
- Do not create inheritance solely to deduplicate a few lines; composition may be clearer.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Identify shared responsibilities and compatible contracts.
2. Introduce the superclass/abstract contract.
3. Move one shared member at a time.
4. Verify subtype behavior and external substitution.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-LARGE-CLASS`
- `SMELL-ALTERNATIVE-CLASSES-DIFFERENT-INTERFACES`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve prototype behavior, constructor order, `instanceof`, method binding, and super calls in legacy OO code.

### TypeScript Notes
- Track structural typing, discriminated unions, abstract contracts, visibility, and public subtype APIs.

### React Notes
- React components should normally use composition, hooks, render props, or delegates rather than class inheritance.

### Vue Notes
- Vue components should normally use composition, composables, slots, and delegation rather than inheritance.

### Frontend-Craft Adaptation
- These techniques primarily serve genuine legacy OO JS/TS, domain models, SDKs, and editor engines; translate intent to composition when frontend architecture is composition-first.

### Example Transformation
Before: two legacy parser classes share identity and diagnostics. After: extract a base only if callers benefit from the common contract; otherwise prefer a shared module.

## RF-COLLAPSE-HIERARCHY — Collapse Hierarchy

### Intent
Merge a superclass/subclass pair when the distinction no longer carries meaningful behavior or substitution value.

### Typical Signals
- A hierarchy level is empty, nearly empty, or adds only indirection.

### Avoid When
- Do not collapse a public subtype boundary without checking external consumers and serialization/type contracts.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Choose the surviving type.
2. Move fields/methods across the boundary.
3. Update construction and type checks.
4. Remove the redundant class after verification.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-LAZY-ELEMENT`
- `SMELL-SPECULATIVE-GENERALITY`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve prototype behavior, constructor order, `instanceof`, method binding, and super calls in legacy OO code.

### TypeScript Notes
- Track structural typing, discriminated unions, abstract contracts, visibility, and public subtype APIs.

### React Notes
- React components should normally use composition, hooks, render props, or delegates rather than class inheritance.

### Vue Notes
- Vue components should normally use composition, composables, slots, and delegation rather than inheritance.

### Frontend-Craft Adaptation
- These techniques primarily serve genuine legacy OO JS/TS, domain models, SDKs, and editor engines; translate intent to composition when frontend architecture is composition-first.

### Example Transformation
Before: an old `SpecialMailbox` subclass has no unique behavior after earlier cleanup. After: merge it into `Mailbox` if no public subtype contract remains.

## RF-REPLACE-SUBCLASS-WITH-DELEGATE — Replace Subclass with Delegate

### Intent
Move one axis of variation from inheritance into a delegate so an object can combine behaviors more flexibly.

### Typical Signals
- Subclasses exist for a variation that conflicts with other inheritance needs or multiplies combinations.

### Avoid When
- Avoid delegation when the hierarchy is simple, stable, and accurately models substitutability.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Create a delegate/strategy for the varying behavior.
2. Have the base object forward one behavior to it.
3. Migrate subtype-specific state/behavior.
4. Remove subclasses when no unique responsibility remains.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-MIDDLE-MAN`
- `SMELL-INSIDER-TRADING`
- `SMELL-REFUSED-BEQUEST`

### Composes Well With
- `RF-REPLACE-SUPERCLASS-WITH-DELEGATE` when its preconditions independently hold.

### JavaScript Notes
- Preserve prototype behavior, constructor order, `instanceof`, method binding, and super calls in legacy OO code.

### TypeScript Notes
- Track structural typing, discriminated unions, abstract contracts, visibility, and public subtype APIs.

### React Notes
- React components should normally use composition, hooks, render props, or delegates rather than class inheritance.

### Vue Notes
- Vue components should normally use composition, composables, slots, and delegation rather than inheritance.

### Frontend-Craft Adaptation
- These techniques primarily serve genuine legacy OO JS/TS, domain models, SDKs, and editor engines; translate intent to composition when frontend architecture is composition-first.

### Example Transformation
Before: message renderer subclasses differ only by formatting strategy. After: renderer delegates to a format strategy/component map where composition is clearer.

## RF-REPLACE-SUPERCLASS-WITH-DELEGATE — Replace Superclass with Delegate

### Intent
Replace an inaccurate inheritance relationship with delegation to the reused capability.

### Typical Signals
- A subclass inherits a broad API only to reuse implementation and is not truly substitutable for the superclass.

### Avoid When
- Keep inheritance when the subtype contract is semantically valid and clients depend on substitution.

### Preconditions
- Current observable behavior and affected callers are understood.
- The target scope is inside a declared diff budget and can be verified after this one primary transformation.

### Mechanics
1. Create a field holding the former superclass capability.
2. Forward only the operations the object actually needs.
3. Remove `extends` and inherited assumptions.
4. Verify public type compatibility and composition behavior.

### Behavior-Preservation Checkpoints
- Compare inputs, outputs, exceptions, side effects, ordering, and public contracts before/after the step.
- For frontend code, also check UI state, events, focus, network behavior, lifecycle/state transitions, and relevant identity semantics.

### Related Code Smells
- `SMELL-MIDDLE-MAN`
- `SMELL-INSIDER-TRADING`
- `SMELL-REFUSED-BEQUEST`

### Composes Well With
- Combine only with a separately justified next transformation; no fixed sequence is required.

### JavaScript Notes
- Preserve prototype behavior, constructor order, `instanceof`, method binding, and super calls in legacy OO code.

### TypeScript Notes
- Track structural typing, discriminated unions, abstract contracts, visibility, and public subtype APIs.

### React Notes
- React components should normally use composition, hooks, render props, or delegates rather than class inheritance.

### Vue Notes
- Vue components should normally use composition, composables, slots, and delegation rather than inheritance.

### Frontend-Craft Adaptation
- These techniques primarily serve genuine legacy OO JS/TS, domain models, SDKs, and editor engines; translate intent to composition when frontend architecture is composition-first.

### Example Transformation
Before: an editor extends a collection class merely to reuse storage methods. After: the editor owns a collection delegate and exposes only editor-relevant operations.
