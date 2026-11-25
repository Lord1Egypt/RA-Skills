# Runtime contract source reference

Use this reference when diagnosing reporter output, validation failures or CLI errors. These are source-verified semantics, not terminal help captures. Existing command/flag examples and historical help provenance remain separate.

Immutable source: [Checkly CLI commit 2b32bb6e0dd4377ca901f3091dd7a7710bcb0b13](https://github.com/checkly/checkly-cli/tree/2b32bb6e0dd4377ca901f3091dd7a7710bcb0b13). Paths below are relative to `packages/cli/src/` at that commit.

| Contract | Source and regression coverage |
|---|---|
| `github` / `json` completed-check counters and retried-attempt lines go to stderr. At most one file reporter supplies progress; a `list`, `dot` or `ci` reporter suppresses it. Startup progress is not duplicated by the file reporters. Existing stdout summaries and report formats are preserved. | `reporters/abstract-progress.ts`, `reporters/reporter.ts`, `reporters/__tests__/progress.spec.ts` |
| JSON is written to `./checkly-json-report.json`, or `CHECKLY_REPORTER_JSON_OUTPUT`; GitHub Markdown goes to `./checkly-github-report.md`, or `CHECKLY_REPORTER_GITHUB_OUTPUT`. Redirecting stdout does not obtain the JSON report. | `reporters/json.ts`, `reporters/github.ts` |
| GitHub table cells escape `|` and replace CR/LF with spaces for names, types and filenames, including unfinished checks. | `reporters/github.ts`, `reporters/__tests__/github-md-builder.spec.ts` |
| A Slack App channel with destinations fails validation when `Session.account.integrations` reports `SLACK` disconnected. Already deployed channels are included. Missing integration state, a connected app or no destinations skips this specific check. | `constructs/slack-app-alert-channel.ts`, `constructs/__tests__/slack-app-alert-channel.spec.ts` |
| Retired `me-south-1` is removed from the location type and rejected in check/monitor/group locations, shared defaults and configured run locations. Explicit `--location` on `test`, `pw-test` and `trigger` gives exit 2; configured invalid locations give exit 1. `pw-test --create-check` checks before writing. Generated imports filter it out. | `config.ts`, `constructs/check.ts`, `constructs/check-group-v1.ts`, `helpers/test-helper.ts`, `commands/pw-test.ts`, `commands/trigger.ts`, `constructs/check-codegen.ts`, `constructs/check-group-codegen.ts`, `helpers/__tests__/retired-regions.spec.ts` |
| Bundling skips declaration-level `import type`, `export type { X } from` and `export type * from`; inline `import { type X } from` remains followed because a `verbatimModuleSyntax` compilation may preserve side effects. | `services/check-parser/parser.ts`, `services/check-parser/__tests__/check-parser.spec.ts` |
| `rca run` reports disabled Rocky AI with account-settings guidance, exit 1 and JSON `code: "ERR_ROCKY_AI_DISABLED"`. The code identifies that API condition, not every 403. | `commands/rca/run.ts`, `rest/errors.ts`, `commands/__tests__/rca-run.spec.ts` |
| `test`, `pw-test` and `trigger` result-stream connection failures include a readable explanation and underlying error details, including aggregate per-address failures. | `services/socket-client.ts`, `services/abstract-check-runner.ts`, `services/__tests__/socket-client.spec.ts` |

## Crash reporting boundaries

Set `CHECKLY_NO_ERROR_REPORTING=1` or `DO_NOT_TRACK=1` before invocation to disable reporting. A configured release sends at most one detected CLI bug per run. The classifier selects `TypeError`, `ReferenceError` and `RangeError` originating in CLI-owned code, including wrapped causes; it excludes ordinary user/API/network errors, user check code and dependencies. This is a classification rule, not a promise that all possible CLI bugs are reported.

The event contains selected error names, messages and stack frames, CLI release/command/mode and OS/runtime/architecture. It does not attach the full environment, command arguments or arbitrary error-object properties. Scrubbing targets recognizable Checkly user/service API keys, Basic/Bearer credentials, URL credentials and known directory paths. It cannot promise removal of every arbitrary secret embedded in error text. Builds without the release reporting configuration, and development builds, do not send reports.

Sources: `services/error-reporting/{classify,event,report,scrub}.ts`, `commands/baseCommand.ts` and the `services/error-reporting/__tests__/` regression suite.

## Limits and generated payloads

Default degraded / maximum response times in milliseconds are API 5000 / 20000, URL and TCP 3000 / 5000, DNS 500 / 1000, gRPC 10000 / 20000, SSL 3000 / 10000, and traceroute 500 / 1000. ICMP packet-loss defaults are 10 / 20 percent. These defaults are sent explicitly and match what the backend already applied; they are not client-side ceilings. Explicit zero values are preserved.

Ordering diagnostics are type-specific: API, URL, TCP and DNS compare response times only when both are explicit. gRPC and SSL additionally compare an explicit degraded value against an omitted maximum (20000 / 10000 ms), but do not compare an omitted degraded against an explicit maximum. Traceroute compares both effective defaults (500 / 1000 ms). It measures final-hop average round-trip latency; a zero maximum disables failure on latency and equal limits leave no degraded state. ICMP compares effective packet-loss thresholds: degraded above an omitted maximum of 20, or maximum below an omitted degraded value of 10, fails validation. Set both thresholds to an ordered pair. A missing property diagnostic or synthesized payload is not proof of total project validity or live backend acceptance.

Sources: `constructs/{api-check,url-monitor,tcp-monitor,dns-monitor,grpc-monitor,ssl-monitor,traceroute-monitor,icmp-monitor}.ts`, `constructs/internal/common-diagnostics.ts`, `constructs/__tests__/{default-limits,traceroute-monitor}.spec.ts`. Payload shape-change cleanup in `constructs/check.ts` does not add another setting or alter these defaults.
