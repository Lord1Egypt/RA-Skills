# Templates — plans and contracts to show the user

Fill these in the user's language. Keep them specific to the repository (real module names, real commands); a generic plan is not reviewable. Leave out sections that do not apply rather than writing "N/A" everywhere.

## Refactor plan

```markdown
## Refactor plan: <title>
Goal: <why this refactor, which future change it makes easier>
Contract (must not change): <public API, outputs, side effects, formats>
Current shape: <2–4 lines or a small diagram>
Target shape: <2–4 lines or a small diagram>
Blast radius: <modules/files, number of call sites, external consumers, hidden coupling found>
Safety net: <existing tests + coverage of touched code; characterization tests to add first>

Steps (each one green and revertible):
1. <expand / add shim / add tests> — verify: <command>
2. <move / migrate callers batch 1> — verify: <command>
3. ...
N. <remove shims / old paths> — verify: <command>

Risks and mitigations: <risk → mitigation>
Rollback: <how to undo the riskiest step>
Out of scope: <deliberately not touched; follow-ups>
```

## Rewrite plan

```markdown
## Rewrite plan: <component>
Why rewrite instead of refactor: <reason(s) from the go/no-go list>
Behavior inventory: <entry points, formats, errors, side effects, config, quirks — or link to the list>
Oracle: <characterization/golden suite against the old implementation; location; input classes>
Seam: <interface / flag / router / proxy where old and new both run>
Slices (in order): <slice → acceptance check>
Approved behavior changes: <change + demonstrating input + who approved>   (none by default)
Parity evidence: <differential harness, corpus size, how differences are triaged>
Cutover: <switch mechanism, order, what is watched>
Rollback window and deletion: <tag/flag, how long, what gets deleted afterwards>
```

## Port plan + parity contract

```markdown
## Port plan: <component> (<source> → <target>)
End state: <A replacement | B permanent bindings | C temporary bindings>
Unit of parity: <function | CLI invocation | HTTP response | file>
Must match: <…>          Allowed to differ: <…>
Fixtures: <location, how generated from the source, input classes incl. error paths>
Module order (leaf first): <m1 → m2 → …>
Key mappings: <numbers, strings, errors, nullability, concurrency, each dependency → replacement>
Not ported: <item → reason>
Known source bugs preserved: <bug → pinning fixture>
Verification: <target test/lint/format commands; differential command; report format "N inputs / M diffs">
Cutover and cleanup: <switch, deletion of source or scaffolding>
```

## Progress note for long efforts

When work spans several sessions, end each one at a green state and leave a short note (in the plan file or the report):

```markdown
Done: <steps completed, with verification results>
State: <builds/tests green? shims alive?>
Next: <next step and its verification command>
Open questions: <decisions waiting on the user>
```
