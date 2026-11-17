# Specification Notation

**Use the [reading version](spec-reading.md) by default** for product discussion and acceptance. Expand the notation below when implementation or precision requires it. Both forms express one specification, not independently maintained requirements.

Write concepts in `CONCEPT.md` and synchronizations in `SYNCS.md`. Describe behavior in natural language with named arguments, conditions, and results; mark undecided details as open.

## CONCEPT

```text
concept Name [Type]

purpose
  <why this functionality is needed>

principle
  <a representative scenario showing how behavior fulfills the purpose>

state
  a set of Items with
    <relations to other individuals or simple values>

actions
  action (input: Input): (result: Result)
    requires <conditions for the action to occur>
    ensures <constraints relating prior and subsequent state, inputs, and results>

  _query (input: Input): (result: Result)
    returns <bindings satisfying the query>
```

**Type parameters** represent individuals with identity, without importing the structure of other concepts.

**State consists of relations.** `a set of Items with ...` organizes relations by individual type; it does not define classes or composite objects. Define initial conditions and invariants before actions; exclude illegal states through types and relational constraints where possible.

**Actions use preconditions and postconditions.** Name inputs and results; omit absent results. `requires` permits occurrence; `ensures` constrains prior and subsequent state and results: **occurrence ⇒ precondition and postcondition hold**. The converse does not follow: a precondition neither guarantees execution nor prescribes a refusal response.

**Queries are read-only and return sets of bindings.** List queries within `actions`, with an initial underscore. Zero, one, or many bindings depend on the query definition.

**The operational principle explains fulfillment of purpose.** It is a representative scenario, not a replacement for the action specifications.

## SYNCS

Identify participating concept instances and type bindings before defining individual synchronizations.

```text
sync RuleName
when Source.action (item)
where
  Target._find (item): (target)
then
  Target.apply (target)
```

**Name each rule.** A name identifies a causal rule for explanation and provenance.

**`when` matches action occurrences.** This skill's execution encoding matches completion records, not invocation requests. Bind arguments by name; partial matching is allowed. Queries do not trigger rules.

**`where` queries and binds.** Read public state, test conditions, and bind variables needed downstream. The same variable denotes the same value.

**`then` initiates subsequent actions.** Arguments come from trigger patterns, query bindings, or explicit constants. Execute for each binding produced by `where`; no bindings means no subsequent action.

**Keep coordination outside concepts.** Rules use declared actions and public state, without calls between concepts. A request may occur without its requested action following.

## Execution semantics

**Actions are atomic.** An action has no observable duration in the model; model activities that span time with start and end actions.

**Synchronizations are causal rules.** An action occurrence leads to subsequent actions under the specified conditions, without an implicit transaction or rollback across the chain. Express required order through action occurrences, not textual position.

Put business conditions directly in actions or synchronizations. Record concurrency, repetition, timing, and recovery requirements as needed; see [execution and recovery](execution.md) for engineering requirements.

## Tool checks

`concept-lint` and the diagram tool read the [tool encoding](tool-encoding.md). This is an explicit encoding of the specification. Conversion preserves names, arguments, conditions, results, and open issues without inventing requirements. The native notation in this document is outside the current parsers' supported input; do not report it as checked.
