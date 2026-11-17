# Principles, reasons, and examples

Use the applicable dimensions to design, review, or verify a CLI. Checks define acceptance; examples illustrate evidence rather than universal syntax.

## Ten dimensions

Dimensions 1–3 support predictability, 4–7 defense in depth, and 8–10 context efficiency. Each row has two independently scored checks.

| Dimension | Why | Check 1 | Check 2 |
| --- | --- | --- | --- |
| 1. Contract | Duplicated definitions drift; stale handoffs misdirect execution. | Give each subcommand a concrete user task. Keep command structure and names consistent. | Share types across schema, validation, and execution; bind resumable artifacts to version, target, run, and input digest. |
| 2. Input | Flat shortcuts can lose nesting; prompts block headless calls. | Preserve nested types through JSON; equivalent flags produce the same request, with explicit conflict handling. | Accept complete non-interactive input; missing input fails immediately with a valid example. |
| 3. Results | A parser needs stable structure; acceptance is not completion. | Offer a machine-readable format such as JSON. Explicit format selection overrides TTY defaults. Send machine data to stdout and diagnostics to stderr. | Keep errors and exit codes stable. Say what to fix, verify, or unblock next. Distinguish accepted, completed, failed, and unknown outcomes. |
| 4. Validation | Agent inputs are untrusted; plausible structure is not proof of validity. | Enforce field-specific schemas and lint constraints; return actionable structured errors. | Enforce path, control-character, ID, address, redirect, and encoding boundaries without corrupting legitimate text. |
| 5. Authentication | Credentials and permissions can change independently of input validity. | Use credential references and least privilege; exclude secrets from argv, logs, and ordinary configuration. | The server checks current permissions. |
| 6. Mutations | Previewed state may change before execution. | Provide `--dry-run` for destructive operations. Show the target and planned changes. Preview writes neither business data nor persistent recovery state; declare authentication and network behavior. | Recheck target, authorization, and concurrency; provide explicit confirmation for high-impact operations while preserving existing authorization. |
| 7. Recovery | Timeout does not mean failure; uncontrolled repair can repeat effects. | Repeating one intent produces one durable business effect, verified against server guarantees. | Reconcile before safe replay; bound repair attempts/no-progress, invalidate stale reports, and rerun affected gates. |
| 8. Discovery | Embedded manuals go stale; full schema expansion wastes context. | Use `--help` to reveal capabilities from root to leaf: list immediate subcommands and their purposes, explain usage, required arguments, applicable options and defaults, and give runnable examples. | Query current machine-readable method/type schemas; bound reference expansion and verify deployed behavior. |
| 9. Responses | Streaming alone neither bounds output nor preserves meaning. | Support declared field selection; state whether projection is client-side or server-side. | Bound pages and record size, preserve parseable JSON/NDJSON, cursors, completeness, and meaningful nulls. |
| 10. Knowledge | Parameter lists do not teach decisions; irrelevant rules distract. | Descriptions explain object, preconditions, direct effect, and completion boundary. | Skills retain workflows, constraints, and necessary examples; load references, current help/schema, and task artifacts on demand. |

## Human-first and Agent-first

Human convenience is not a defect. Agent-first adds complete, stable, headless paths using the same validation and executor.
The following flags and JSON shapes are illustrative; confirm actual syntax in the target CLI.

| Task | Human-first positive | Agent-first positive | Negative and consequence |
| --- | --- | --- | --- |
| Simple input | `--name invoices` is easy to type. | The same flag works headlessly and maps to a typed request. | Ban all flags merely because the caller is an agent; add needless complexity. |
| Nested input | Shortcuts cover a common single-sheet case. | `{"sheets":[{"title":"Actual"},{"title":"Plan"}]}` preserves both sheets. | Repeated `--sheet-title` overwrites the first sheet; silently merge conflicting flag/JSON values. |
| Output | A table is easy to scan. | Explicit JSON returns stable IDs and states on any terminal. | Parse colored columns or put progress text before JSON; the consumer breaks. |
| Missing input | Explicit interactive mode offers a TTY menu. | Fail with a field path, stable error code, valid call, and nonzero exit. | Wait on closed stdin or guess production; execution hangs or hits the wrong target. |
| Discovery | Focused help shows working usage. | Query only the required method and referenced types. | Copy the whole manual into every prompt; generate stale calls. |
| Pagination | A person pages through a table. | At the page limit retain `next_cursor` and `complete: false`; keep meaningful `null`. | Stream every page, drop cursors, or equate `{"owner":null}` with an absent owner. |

For comparable input paths, compare normalized executor requests rather than their printed messages.
Preserve omission, `null`, `false`, `0`, empty strings, and arrays according to the method contract.
Declare file/stdin syntax, bound input size, and allow one stdin consumer per call.

## Untrusted input hardening

Agent-generated arguments are untrusted: plausible fields and values can still violate the contract. Apply public-API rigor in the shared executor, including CLI and MCP paths.
Check locally decidable constraints before business requests or writes; verify state-dependent constraints against current resources before mutation.

| Boundary | Positive rule and example | Negative |
| --- | --- | --- |
| Paths | Resolve the path and symlinked parents; reject `../../.ssh` or a symlink escape outside the allowed root. | Block only the literal `../` substring and assume the target is contained. |
| Control characters | Reject controls in identifiers; escape terminal controls such as `\u001b[2J` when displaying text. Preserve declared body newlines. | Execute terminal escape sequences or strip every newline from stored text. |
| Resource IDs | Reject `file_17?fields=name` as an ID; pass field selection through its declared parameter. Allow query-bearing URLs in URL/text fields. | Concatenate an ID into a request URL, or apply ID restrictions to all body text. |
| Encoding | Declare raw versus encoded input. Validate in the form the consumer uses and encode once at the transport boundary; test encoded traversal where decoding applies. | Repeatedly decode until something looks valid, double-encode blindly, or ban every `%` regardless of field contract. |
| Unknown fields | A closed object rejects `{"fon_size":12}` with a field error; declared extension maps retain user keys. | Ignore invented fields, silently guess corrections, or close every dynamic map. |
| Types and bounds | An integer field rejects `{"limit":"10"}` unless coercion is declared; a three-item collection rejects `{"index":4}`. Validate enums and per-element limits. | Accept any syntactically valid JSON, clamp values silently, or rely on prompt reminders. |

Put required enums, bounds, and quality thresholds in executable schemas or lint contracts. Apply only declared constraints; instructions alone do not enforce them.
Return a stable code, field path, allowed value/range, and actionable correction with a nonzero exit. Example for a three-item collection:

```json
{"error":{"code":"INDEX_OUT_OF_RANGE","field":"index","expected":{"min":0,"max":2},"suggestion":"Select an index within the reported range"},"effects":"none"}
```

Only report `effects: none` when evidence establishes it; do not echo secrets or unsafe control bytes in diagnostics.
A rejected preflight can be corrected and resubmitted. A timeout after dispatch requires outcome reconciliation, not a validation retry.

## Critical positive and negative checks

Run in an authorized isolated fixture. K1/K2 are server-supported idempotency keys; B1/B2 are different bodies.

| Case | Positive evidence | Negative |
| --- | --- | --- |
| Input preflight | Exercise the hardening cases through each supported surface; locally invalid input produces no business HTTP or writes, while valid text/maps still pass. | Test only rejection, skip valid counterparts, or let MCP bypass CLI validation. |
| Same intent | Submit K1/B1 twice; verify one durable effect and the original ID/receipt when defined. | Generate a new key for every retry. |
| New intent / body conflict | Use K2 for a separately authorized intent; K1/B2 must fail without another effect. Recheck current permissions and business uniqueness. | Reuse K1 for a new operation or accept a changed body under K1. |
| Unknown write | Query outcome first. Replay K1/B1 only within verified server key scope and retention. With no valid key, reconcile resource, receipt, and audit facts; otherwise retain `unknown`. | Treat timeout as failure and start a new write. |
| `--dry-run` | Run a destructive subcommand in preview mode: valid input shows the expected target and planned changes with zero business or recovery state writes. Invalid IDs or inline secrets fail before effects. A local-only preview must also make no business HTTP requests or credential accesses. | Return a plan while writing business data, or initialize authentication or send business requests despite a local-only claim. |
| Secrets / external text | Inject a test secret through stdin/private file; check all formats and both streams. Mask secret fields, retain public IDs/types, and preserve provenance of untrusted text. | Leak a secret in an error, remove the whole token object, or obey instructions in returned content. |
| Async completion | Report HTTP 202 as accepted; query terminal success and verify the requested result. | Report done merely because a job ID exists. |
| Contract change | Recheck current schema and accepted/rejected inputs on the tested artifact/version. | Reuse a score from another binary or assume generated schema proves deployment parity. |

## Resumable workflows

Persist handoffs when restart, inspection, or cross-tool use requires them. A one-step task needs no orchestration framework.
Validate artifact version, target, run, input digest, and allowed transition; write atomically and exclude credentials.

```text
build -> check -> ready -> execute -> verify -> done
           |               |          |
           v               +----------+-> unknown -> reconcile
       needs_fix -> repair -> check
           |
           +-> blocked (budget exhausted or no progress)
```

Positive: changing plan A to plan B invalidates affected reports; rerun the relevant gates and stop at the attempt/time budget or repeated identical failure.
Separate content and contract gates when they require different fixes. Negative: publish despite a failed gate, reuse A's report for B, or loop indefinitely.
A passing report proves only its checks on that input. Files, previews, and client-generated keys provide neither current authorization nor server idempotency.
