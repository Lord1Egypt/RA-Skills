# Tool Encoding

This document defines the Markdown encoding accepted by the checker and diagram tool. Author concepts and synchronizations using the [specification notation](spec-notation.md). `coverage`, section names, and record syntax are tool fields.

## CONCEPT

The four core sections in tool input MUST appear in this order: `purpose`, `state`, `actions`, `operational principle`.
Each MUST contain a declaration.
Place optional `queries` after the operational principle, then an optional execution-constraints section.
`coverage: complete|partial` declares the specification's coverage. It is local metadata.

```markdown
# concept Name [T]
coverage: partial

## purpose
<one evaluable need>

## state
items: set Item
owner: Item -> T
<local types, cardinality, initial state, invariants>

## actions
act [item: Item; owner: T] => [item: Item]
  requires <success condition>
  ensures <effect, output, unchanged state>
act [item: Item; owner: T] => [error: E]
  requires <refusal condition>
  ensures <error meaning and state consequence>

## operational principle
after <declared actions and results>
then <later action or observation fulfilling purpose>
```

Name action inputs and outputs; use `[]` for no inputs and `=> []` for no result.
Add [execution constraints](execution.md#execution-constraints) only when required.

Optional `## queries` maps public relations to read APIs:

```markdown
## queries
_owners [item: Item] => [owner: T]
  returns owner bindings; no match returns zero rows
```

Declare query signatures, cardinality, and underlying relations.
In SYNCS, `Name/_query: [inputs] => [outputs]` appears only in `where`.

## SYNCS

Includes MUST resolve to concept or external-entry contracts.
Declare aliases, concrete types, and root signatures for requests, timers, or messages.
For diagrams, check supported includes in the [diagram contract](diagram-contract.md#identity-and-resolution).

A `sync` MAY be immediately preceded by `### <business description>`.

```markdown
# app AppName
include Source [Id]
include Target [Id]

### Pass completion results
sync Transfer
when { Source/finish: [] => [item: ?item] }
where { Source: { ?item owner: ?owner } }
then { Target/accept: [item: ?item; owner: ?owner] }
```

| Part | Constraint |
| --- | --- |
| `sync` | Stable, application-unique name for one decision. |
| `when` | Required and nonempty. All completion patterns MUST match in one runtime flow. |
| Patterns | Omissions are wildcards; `[]` is not success. MUST distinguish cases affecting later effects. |
| `where` | Optional. Read, filter, compute, bind rows; omission retains input bindings. |
| `then` | Required and nonempty. MUST call per binding row with all required named inputs and no outputs. |
| `?name` | Within each binding row, the same variable has the same value. Calls use constants or bound values. |

[Synchronization scenarios](spec-examples.md#synchronization-scenarios).

## concept-lint

```sh
python3 <skill-directory>/scripts/concept_lint.py CONCEPT.md SYNCS.md --json
```

The CLI is read-only and uses only the standard library.

- Checks declarations, coverage, unique/nonempty core sections, rule blocks and delimiters.
- In closed `when`/`then` blocks, checks named, nonempty, unique top-level input/output fields; requires outputs in `when` and forbids them in `then`.
- Detects duplicate rule names across files for the same app; different apps may reuse names.
- Ignores comments, string contents and fenced annotations while preserving diagnostic line numbers.
- Leaves nested values, `where`, includes, signatures, types, bindings and execution policies unchecked. Unknown calls, including braced legacy dot-calls, return `not_checked`.

| Exit | Status | Meaning |
| --- | --- | --- |
| 0 | `format_checked` | All inputs passed the listed structural checks. |
| 1 | `format_error` | At least one determined structural error. |
| 2 | `read_error` | Usage, file access, or encoding error. |
| 3 | `not_checked` | Legacy, unknown, incomplete notation, or missing coverage. |

Read errors take precedence over format errors; format errors take precedence over unchecked portions.
Incomplete comments, strings, or fences cannot turn hidden content into an inferred missing section.
Errors in already closed sections/blocks still count.
For a deliberately absent state or action set, write that declaration instead of leaving the section blank.
`format_checked` is not semantic verification.
