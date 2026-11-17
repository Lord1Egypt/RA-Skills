# Code Smell Catalog

This catalog distills the supplied Chapter 3 taxonomy into evidence-oriented frontend diagnostics. Standard names and IDs are stable; explanations are project-native summaries.

## SMELL-MYSTERIOUS-NAME — Mysterious Name

### Diagnostic Meaning
A name does not reveal the element’s purpose or usage.

### Strong Signals
- names require tracing implementation before intent is clear.
- renames are repeatedly discussed because current vocabulary is unstable.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- abbreviations are mandated domain terms understood by the team.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-CHANGE-FUNCTION-DECLARATION`
- `RF-RENAME-VARIABLE`
- `RF-RENAME-FIELD`

### Related Smells
- `SMELL-SPECULATIVE-GENERALITY`
- `SMELL-ALTERNATIVE-CLASSES-DIFFERENT-INTERFACES`
- `SMELL-COMMENTS`

### Frontend Manifestations
Functions, hooks, stores, props, events, and DTO fields whose names hide business intent.

## SMELL-DUPLICATED-CODE — Duplicated Code

### Diagnostic Meaning
The same or near-identical structure appears in multiple places and must evolve together.

### Strong Signals
- equivalent expressions or branches appear in multiple functions.
- a change requires editing several copies of the same rule.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- similar-looking code has materially different business reasons to change.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-EXTRACT-FUNCTION`
- `RF-SLIDE-STATEMENTS`
- `RF-PULL-UP-METHOD`

### Related Smells
- `SMELL-LONG-FUNCTION`
- `SMELL-MUTABLE-DATA`
- `SMELL-DIVERGENT-CHANGE`

### Frontend Manifestations
Repeated handlers, validators, formatters, selectors, or component branches that encode one rule.

## SMELL-LONG-FUNCTION — Long Function

### Diagnostic Meaning
A function mixes enough intentions that its purpose is difficult to see without reading implementation detail.

### Strong Signals
- comments divide the body into conceptual sections.
- validation, data shaping, effects, and state updates are interleaved.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- LOC alone does not prove the smell; a cohesive algorithm may legitimately be long.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-EXTRACT-FUNCTION`
- `RF-REPLACE-TEMP-WITH-QUERY`
- `RF-INTRODUCE-PARAMETER-OBJECT`
- `RF-PRESERVE-WHOLE-OBJECT`
- `RF-REPLACE-FUNCTION-WITH-COMMAND`
- `RF-DECOMPOSE-CONDITIONAL`
- `RF-REPLACE-CONDITIONAL-WITH-POLYMORPHISM`
- `RF-SPLIT-LOOP`

### Related Smells
- `SMELL-DUPLICATED-CODE`
- `SMELL-LONG-PARAMETER-LIST`
- `SMELL-MUTABLE-DATA`

### Frontend Manifestations
Large event handlers, submit flows, hooks/composables, effects, loaders, and data adapters with multiple responsibilities.

## SMELL-LONG-PARAMETER-LIST — Long Parameter List

### Diagnostic Meaning
A function receives many separate values whose relationships or origins are hard to understand.

### Strong Signals
- several parameters are always passed together.
- callers unpack many fields from one object only to pass them separately.
- a flag parameter selects behavior.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- many independent values are genuinely required at a narrow boundary and an object would hide rather than clarify them.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-REPLACE-PARAMETER-WITH-QUERY`
- `RF-PRESERVE-WHOLE-OBJECT`
- `RF-INTRODUCE-PARAMETER-OBJECT`
- `RF-REMOVE-FLAG-ARGUMENT`
- `RF-COMBINE-FUNCTIONS-INTO-CLASS`

### Related Smells
- `SMELL-LONG-FUNCTION`
- `SMELL-MUTABLE-DATA`
- `SMELL-SHOTGUN-SURGERY`

### Frontend Manifestations
Hooks, helpers, services, callbacks, and component utilities with recurring options or context fragments.

## SMELL-GLOBAL-DATA — Global Data

### Diagnostic Meaning
Widely reachable data can be read or modified without a controlled access boundary.

### Strong Signals
- mutation can originate from unrelated modules.
- the source of a state change is difficult to trace.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- immutable configuration fixed after startup has lower risk, though encapsulation can still clarify ownership.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-ENCAPSULATE-VARIABLE`

### Related Smells
- `SMELL-MUTABLE-DATA`

### Frontend Manifestations
Module singletons, window globals, mutable config objects, ad-hoc caches, or shared stores with unrestricted mutation.

## SMELL-MUTABLE-DATA — Mutable Data

### Diagnostic Meaning
State changes are difficult to reason about because values can be altered from multiple places or reused for different meanings.

### Strong Signals
- the same variable is reassigned for distinct purposes.
- queries also mutate state.
- derived values are stored and manually synchronized.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- controlled local mutation inside a clear algorithm is not automatically problematic.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-ENCAPSULATE-VARIABLE`
- `RF-SPLIT-VARIABLE`
- `RF-SLIDE-STATEMENTS`
- `RF-EXTRACT-FUNCTION`
- `RF-SEPARATE-QUERY-FROM-MODIFIER`
- `RF-REMOVE-SETTING-METHOD`
- `RF-REPLACE-DERIVED-VARIABLE-WITH-QUERY`
- `RF-COMBINE-FUNCTIONS-INTO-CLASS`
- `RF-COMBINE-FUNCTIONS-INTO-TRANSFORM`
- `RF-CHANGE-REFERENCE-TO-VALUE`

### Related Smells
- `SMELL-DUPLICATED-CODE`
- `SMELL-LONG-FUNCTION`
- `SMELL-LONG-PARAMETER-LIST`

### Frontend Manifestations
Shared React/Vue state, mutable module caches, form models, and derived state that can drift from its source.

## SMELL-DIVERGENT-CHANGE — Divergent Change

### Diagnostic Meaning
One module changes for several unrelated reasons or contexts.

### Strong Signals
- different feature requests repeatedly touch disjoint regions of the same module.
- one component owns unrelated data access, business rules, presentation, and integration concerns.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- a small cohesive module may legitimately respond to several closely related changes.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-SPLIT-PHASE`
- `RF-MOVE-FUNCTION`
- `RF-EXTRACT-FUNCTION`
- `RF-EXTRACT-CLASS`

### Related Smells
- `SMELL-DUPLICATED-CODE`
- `SMELL-LONG-FUNCTION`
- `SMELL-MUTABLE-DATA`

### Frontend Manifestations
God components or services that mix transport, domain policy, formatting, and UI concerns.

## SMELL-SHOTGUN-SURGERY — Shotgun Surgery

### Diagnostic Meaning
One conceptual change requires many small edits scattered across the codebase.

### Strong Signals
- one business rule is duplicated across components, hooks, stores, and services.
- adding a variant requires editing many registries or conditionals.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- cross-cutting requirements such as telemetry may intentionally span boundaries when centralized infrastructure is not appropriate.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-MOVE-FUNCTION`
- `RF-MOVE-FIELD`
- `RF-COMBINE-FUNCTIONS-INTO-CLASS`
- `RF-COMBINE-FUNCTIONS-INTO-TRANSFORM`
- `RF-SPLIT-PHASE`
- `RF-INLINE-FUNCTION`
- `RF-INLINE-CLASS`

### Related Smells
- `SMELL-LONG-PARAMETER-LIST`
- `SMELL-MUTABLE-DATA`
- `SMELL-DIVERGENT-CHANGE`

### Frontend Manifestations
A feature change scattered across UI, selectors, API adapters, route config, and duplicated helpers.

## SMELL-FEATURE-ENVY — Feature Envy

### Diagnostic Meaning
A function interacts more strongly with another module’s data or behavior than with its own.

### Strong Signals
- most values used by a calculation come from another owner.
- a helper repeatedly navigates another module’s internals.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- orchestration functions legitimately coordinate several owners and should not be moved wholesale.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-MOVE-FUNCTION`
- `RF-EXTRACT-FUNCTION`

### Related Smells
- `SMELL-DUPLICATED-CODE`
- `SMELL-LONG-FUNCTION`
- `SMELL-MUTABLE-DATA`

### Frontend Manifestations
Selectors or helpers placed near a component but dominated by store/domain data owned elsewhere.

## SMELL-DATA-CLUMPS — Data Clumps

### Diagnostic Meaning
The same group of data items repeatedly travels together across fields or parameters.

### Strong Signals
- removing one value makes the remaining group lose meaning.
- the same field cluster appears in multiple signatures.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- a temporary one-off transport shape may not justify a domain abstraction.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-EXTRACT-CLASS`
- `RF-INTRODUCE-PARAMETER-OBJECT`
- `RF-PRESERVE-WHOLE-OBJECT`

### Related Smells
- `SMELL-LONG-FUNCTION`
- `SMELL-LONG-PARAMETER-LIST`
- `SMELL-DIVERGENT-CHANGE`

### Frontend Manifestations
Repeated date-range, pagination, address, upload, or request option groups in props and APIs.

## SMELL-PRIMITIVE-OBSESSION — Primitive Obsession

### Diagnostic Meaning
Domain concepts with rules or invariants are represented only as generic strings, numbers, or booleans.

### Strong Signals
- validation/formatting for the same primitive repeats in several places.
- conditional logic interprets magic strings or numbers.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- a primitive with no domain behavior or invariant does not need a wrapper.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-REPLACE-PRIMITIVE-WITH-OBJECT`
- `RF-REPLACE-TYPE-CODE-WITH-SUBCLASSES`
- `RF-REPLACE-CONDITIONAL-WITH-POLYMORPHISM`
- `RF-EXTRACT-CLASS`
- `RF-INTRODUCE-PARAMETER-OBJECT`

### Related Smells
- `SMELL-LONG-FUNCTION`
- `SMELL-LONG-PARAMETER-LIST`
- `SMELL-DIVERGENT-CHANGE`

### Frontend Manifestations
Money, email addresses, IDs, ranges, units, statuses, and mode strings with repeated parsing or validation.

## SMELL-REPEATED-SWITCHES — Repeated Switches

### Diagnostic Meaning
The same type/variant distinction is repeated in several conditionals and must stay synchronized.

### Strong Signals
- adding one variant requires modifying several switches/if chains.
- branch-specific behavior is distributed by the same discriminator.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- One switch does not prove Repeated Switches; a centralized exhaustive dispatcher can be appropriate.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-REPLACE-CONDITIONAL-WITH-POLYMORPHISM`

### Related Smells
- `SMELL-LONG-FUNCTION`
- `SMELL-PRIMITIVE-OBSESSION`

### Frontend Manifestations
Repeated status/type dispatch across render logic, validation, serialization, and actions.

## SMELL-LOOPS — Loops

### Diagnostic Meaning
An imperative loop hides a simple transformation pipeline that could communicate intent more directly.

### Strong Signals
- the loop is mainly filter/map/collect style transformation.
- multiple bookkeeping variables obscure the element-level operation.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- performance-critical, early-exit, stateful, or async loops may be clearer as loops.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-REPLACE-LOOP-WITH-PIPELINE`

### Related Smells
- Diagnose neighboring smells independently; do not infer them from this smell alone.

### Frontend Manifestations
Array normalization or view-model construction that is easier to express as filter/map/reduce style operations.

## SMELL-LAZY-ELEMENT — Lazy Element

### Diagnostic Meaning
An abstraction no longer earns its indirection because it adds little meaning, behavior, or change isolation.

### Strong Signals
- a wrapper merely mirrors another function or module.
- an extracted class has collapsed to trivial delegation.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- a tiny named function can still be valuable when its name expresses intent or provides a stable seam.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-INLINE-FUNCTION`
- `RF-INLINE-CLASS`
- `RF-COLLAPSE-HIERARCHY`

### Related Smells
- `SMELL-SHOTGUN-SURGERY`
- `SMELL-SPECULATIVE-GENERALITY`
- `SMELL-MIDDLE-MAN`

### Frontend Manifestations
Pass-through hooks, wrappers, components, services, or classes that no longer own meaningful policy.

## SMELL-SPECULATIVE-GENERALITY — Speculative Generality

### Diagnostic Meaning
Unused abstractions or extension points exist mainly for hypothetical future needs.

### Strong Signals
- unused hooks, parameters, subclasses, or extension interfaces increase navigation cost.
- an abstraction exists only for tests or imagined variants.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- known near-term compatibility requirements with evidence can justify an extension point.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-COLLAPSE-HIERARCHY`
- `RF-INLINE-FUNCTION`
- `RF-INLINE-CLASS`
- `RF-CHANGE-FUNCTION-DECLARATION`
- `RF-REMOVE-DEAD-CODE`

### Related Smells
- `SMELL-MYSTERIOUS-NAME`
- `SMELL-SHOTGUN-SURGERY`
- `SMELL-LAZY-ELEMENT`

### Frontend Manifestations
Generic component APIs, unused slots/callbacks, premature plugin systems, or future-proof flags with no consumers.

## SMELL-TEMPORARY-FIELD — Temporary Field

### Diagnostic Meaning
A field is meaningful only during a special phase or condition, leaving the object partly invalid at other times.

### Strong Signals
- several fields are populated and read only within one workflow.
- many null checks exist because fields are absent outside a special case.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- optional fields in a deliberately modeled partial/async state are not automatically a smell.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-EXTRACT-CLASS`
- `RF-MOVE-FUNCTION`
- `RF-INTRODUCE-SPECIAL-CASE`

### Related Smells
- `SMELL-DIVERGENT-CHANGE`
- `SMELL-SHOTGUN-SURGERY`
- `SMELL-FEATURE-ENVY`

### Frontend Manifestations
Component/service state containing transient workflow-only values that belong to a dedicated model or phase.

## SMELL-MESSAGE-CHAINS — Message Chains

### Diagnostic Meaning
Clients depend on a navigation path through several objects to reach the data or behavior they need.

### Strong Signals
- many callers repeat nested property/accessor navigation.
- a relationship change forces callers to update traversal paths.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- A function/array pipeline is not automatically Message Chains; fluent APIs can be intentionally cohesive.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-HIDE-DELEGATE`
- `RF-EXTRACT-FUNCTION`
- `RF-MOVE-FUNCTION`

### Related Smells
- `SMELL-DUPLICATED-CODE`
- `SMELL-LONG-FUNCTION`
- `SMELL-MUTABLE-DATA`

### Frontend Manifestations
Deep DTO/store access such as session.user.organization.policy scattered through UI code.

## SMELL-MIDDLE-MAN — Middle Man

### Diagnostic Meaning
An abstraction delegates most of its interface without adding meaningful policy or protection.

### Strong Signals
- a wrapper exposes many one-line pass-through methods.
- callers must traverse an extra layer that adds no stable boundary.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- React/Vue declarative composition is not automatically Middle Man; wrappers can own accessibility, styling, or compatibility policy.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-REMOVE-MIDDLE-MAN`
- `RF-INLINE-FUNCTION`
- `RF-REPLACE-SUPERCLASS-WITH-DELEGATE`
- `RF-REPLACE-SUBCLASS-WITH-DELEGATE`

### Related Smells
- `SMELL-SHOTGUN-SURGERY`
- `SMELL-LAZY-ELEMENT`
- `SMELL-SPECULATIVE-GENERALITY`

### Frontend Manifestations
Proxy services, hooks, or wrapper components whose only job is forwarding to another owner.

## SMELL-INSIDER-TRADING — Insider Trading

### Diagnostic Meaning
Modules exchange too much internal data or knowledge, weakening their boundaries.

### Strong Signals
- two modules repeatedly reach into each other’s internals.
- private representation details leak across boundaries.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- explicit narrow collaboration is normal when responsibilities genuinely span modules.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-MOVE-FUNCTION`
- `RF-MOVE-FIELD`
- `RF-HIDE-DELEGATE`
- `RF-REPLACE-SUBCLASS-WITH-DELEGATE`
- `RF-REPLACE-SUPERCLASS-WITH-DELEGATE`

### Related Smells
- `SMELL-DIVERGENT-CHANGE`
- `SMELL-SHOTGUN-SURGERY`
- `SMELL-FEATURE-ENVY`

### Frontend Manifestations
Components, stores, and services coupled through internal fields rather than deliberate contracts.

## SMELL-LARGE-CLASS — Large Class

### Diagnostic Meaning
A class or equivalent module owns too many fields and responsibilities, encouraging duplication and unrelated change.

### Strong Signals
- clusters of fields and methods form distinct concepts.
- different subsets of state are used by different operations.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- LOC alone does not prove Large Class; cohesive data structures or generated adapters may be large.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-EXTRACT-CLASS`
- `RF-EXTRACT-SUPERCLASS`
- `RF-REPLACE-TYPE-CODE-WITH-SUBCLASSES`

### Related Smells
- `SMELL-DIVERGENT-CHANGE`
- `SMELL-DATA-CLUMPS`
- `SMELL-PRIMITIVE-OBSESSION`

### Frontend Manifestations
Oversized stores, services, class components, controllers, or modules with several independent responsibility clusters.

## SMELL-ALTERNATIVE-CLASSES-DIFFERENT-INTERFACES — Alternative Classes with Different Interfaces

### Diagnostic Meaning
Two interchangeable concepts provide similar behavior through incompatible interfaces.

### Strong Signals
- callers require adapters or conditionals just to switch implementations.
- equivalent operations have inconsistent names/signatures.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- different interfaces are appropriate when the concepts are not actually substitutable.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-CHANGE-FUNCTION-DECLARATION`
- `RF-MOVE-FUNCTION`
- `RF-EXTRACT-SUPERCLASS`

### Related Smells
- `SMELL-MYSTERIOUS-NAME`
- `SMELL-DIVERGENT-CHANGE`
- `SMELL-SHOTGUN-SURGERY`

### Frontend Manifestations
Alternative API clients, storage adapters, editors, or providers that should satisfy one frontend contract.

## SMELL-DATA-CLASS — Data Class

### Diagnostic Meaning
A data holder is manipulated in detail by other modules while behavior that belongs with the data lives elsewhere.

### Strong Signals
- clients repeatedly read/write fields and perform the same calculations.
- mutable fields expose invariants that callers must maintain.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- Immutable DTOs, API responses, and intermediate transform records may legitimately remain data-only.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-ENCAPSULATE-RECORD`
- `RF-REMOVE-SETTING-METHOD`
- `RF-MOVE-FUNCTION`
- `RF-EXTRACT-FUNCTION`
- `RF-SPLIT-PHASE`

### Related Smells
- `SMELL-DUPLICATED-CODE`
- `SMELL-LONG-FUNCTION`
- `SMELL-MUTABLE-DATA`

### Frontend Manifestations
Mutable form/domain models whose rules live in consumers; immutable transfer/view-model records are common exceptions.

## SMELL-REFUSED-BEQUEST — Refused Bequest

### Diagnostic Meaning
A subtype inherits data or behavior that does not fit its real substitutability or responsibility.

### Strong Signals
- subclasses override inherited behavior to disable it.
- consumers cannot safely treat subtype as the parent contract.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- a subtype need not use every parent helper; unused inherited members alone do not prove the smell.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-PUSH-DOWN-METHOD`
- `RF-PUSH-DOWN-FIELD`
- `RF-REPLACE-SUBCLASS-WITH-DELEGATE`
- `RF-REPLACE-SUPERCLASS-WITH-DELEGATE`

### Related Smells
- `SMELL-MIDDLE-MAN`
- `SMELL-INSIDER-TRADING`

### Frontend Manifestations
Legacy class hierarchies in SDKs, editors, models, or class components where inheritance encodes the wrong relationship.

## SMELL-COMMENTS — Comments

### Diagnostic Meaning
Comments are used to explain confusing structure that code could express more directly; comments themselves are not defects.

### Strong Signals
- a long comment explains a block’s purpose because the block has no meaningful abstraction.
- comments describe preconditions that code never checks.

### Weak Signals
- a reader needs repeated navigation to understand the intent.
- changes around the area have historically been error-prone.

### False Positives
- Comments are not defects by themselves; rationale, constraints, and non-obvious decisions can be valuable.

### Required Evidence
- Cite concrete files/symbols and show the repeated dependency, change pattern, or structural burden; metrics alone are insufficient.

### Likely Impact
- Increased comprehension cost, change coupling, or regression risk when the affected structure evolves.

### Candidate Refactorings
- `RF-EXTRACT-FUNCTION`
- `RF-CHANGE-FUNCTION-DECLARATION`
- `RF-INTRODUCE-ASSERTION`

### Related Smells
- `SMELL-MYSTERIOUS-NAME`
- `SMELL-DUPLICATED-CODE`
- `SMELL-LONG-FUNCTION`

### Frontend Manifestations
Comments around dense handlers or conditionals can reveal missing names, extracted functions, or explicit invariants.
