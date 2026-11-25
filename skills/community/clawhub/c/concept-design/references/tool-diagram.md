# Concept and Synchronization Diagram, version 1

## Usage

Generate `ARCHITECTURE.md` with Mermaid from local CONCEPT/SYNCS in the [tool encoding](tool-encoding.md). Native notation is unsupported; version 1 excludes PIPELINE, PRD, and source code.

```sh
python3 <skill-directory>/scripts/concept_map.py <root> --output <root>/ARCHITECTURE.md
```

Report output location, scope, exit status, and gaps. Scope options follow; writing and check rules appear below.

## Scan and scope

Scan `**/CONCEPT.md` and `**/SYNCS.md` beneath the root.
Exclude `.git`, `node_modules`, and `.venv`; never follow symlinks.
Apply repeated `--exclude PATTERN` filters and sort relative paths.
Rescan and check the root index every run, including with `--scope`.
Record root-index sources and exclusions; do not use timestamps to skip inputs.

`--scope RELPATH` shows only in-scope concept definitions and rules, plus their direct instance boundaries.
The root-wide index may resolve definitions outside scope.
Mark those targets `outside_scope` without expanding their other rules.
Retain unreferenced in-scope concepts.

## Identity and resolution

Serialize each key as compact JSON with `ensure_ascii=False`, then encode UTF-8.
`hash12` is the first 12 lowercase hexadecimal digits of SHA-256.

```text
c_<hash12(["concept", relativePath, name])>
i_<hash12(["instance", app, instanceName])>
s_<hash12(["sync", app, ruleName])>
```

`relativePath` is root-relative with `/` separators.
A hash collision, conflicting includes in one app, or duplicate rule names in one app is a determined error.
Repeated compatible includes identify the same instance.
Adding other nodes preserves existing IDs; changing a definition path or declared name may change its ID.

Resolve `include Name[T]` by the concept's declared name across the root index.
Exactly one candidate resolves; several are `ambiguous`; none is `missing`.
Version 1 does not support aliases or external-entry roots.
Unsupported or unresolved references MUST retain their source text and a gap.
MUST NOT guess a target or relabel it external.

## Rules and edges

Each sync has one node.
Every `when` pattern is a conjunctive incoming edge.
Every `then` call is an outgoing edge with no implicit order.
Show `where` reads as dashed incoming edges.

Supported `where` forms:

```text
Alias: { ?subject relation: value; ... }
Alias/query: [...] => [...]
bind(...)
```

Top-level state relations and query fields must be named, nonempty, and unique.
Preserve calculations as source text without edges or claims about binding correctness.
Unknown state patterns or nested namespaces are partial; do not invent read edges.
Other forms remain raw text and make the result partial.
Retain repeated calls and different pattern roles separately, with source order, raw text, and source line.

## Markdown and writes

Sort Mermaid nodes by identity key and edges by rule, `when/where/then`, and source ordinal.
IDs MUST use stable ASCII; quote and escape labels.
Unchanged input MUST produce byte-identical source; omit generation times.

The generated region uses exactly one marker pair:

```text
<!-- concept-map:start -->
...
<!-- concept-map:end -->
```

Its English section headings are fixed: `Source status`, `Concept index`, `Synchronization diagram`, `Relations`, `Gaps`.
The concept index includes verbatim purposes, coverage declarations, and specification links.
Instance rows retain definition references, type bindings, and include sources; rule rows retain declaration sources.
Relations retain pattern roles, order, raw text, and source lines.
Gaps identify unresolved or unsupported material.

Without `--output`, print Markdown to stdout.
With `--output`, create a new file or replace only its marked region.
Preserve all text outside that region and skip a byte-identical write.
An existing file with missing, duplicate, or unmatched markers is an error.
MUST NOT overwrite an input specification.
Determined errors prevent writing.
No specifications leave existing output untouched.
Partial results may be written only with explicit partial status.
`--check` requires `--output` and compares without writing.

| Exit | Meaning |
| --- | --- |
| `0` | Generated or current output, without gaps |
| `1` | Determined structure/identity error, or `--check` difference |
| `2` | Usage or I/O error |
| `3` | No specifications, or partial result |

When several conditions apply, priority is `2 > 1 > 3 > 0`.
This is a projection of local specifications, not a purpose-dependency, code-coverage, or runtime-correctness report.
