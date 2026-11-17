# Testing And Release

Use the smallest test that proves the adapter contract, then add one live or
HTTP-level smoke when behavior crosses process boundaries.

## Test Layers

| Layer | What to prove |
|---|---|
| Unit | option resolution, server construction, env vars, skill path collection |
| Dispatcher | main-affinity calls run on the host dispatcher and return envelopes |
| Skill lifecycle | `search_skills` -> `load_skill` -> typed tool -> `unload_skill` |
| REST/MCP | direct `/mcp` or `/v1/*` search, then the returned `next_step` |
| Gateway | multi-instance routing, policy, compact responses, debug traces |
| Live DCC | one host smoke that creates/queries/cleans up real scene state |
| Packaging | wheel or plugin archive installs into the target host runtime |
| Install SOP | `plan -> execute -> verify -> status -> uninstall`, including rollback |

## Protocol Compatibility Gates

Protocol selection and wire types belong to Core. Follow the
[Core protocol router](https://github.com/dcc-mcp/dcc-mcp-core/blob/main/docs/adr/033-mcp-http-protocol-router.md)
for the exact revision under test; adapters should not duplicate its envelopes
or enable an opt-in protocol solely because a newer model or SDK exists.

| Boundary | Required evidence when changing protocol support |
|---|---|
| Feature flags | Test feature-on and feature-off builds; keep legacy initialize/list/call working. Advertise only implemented handlers, providers, and notification channels. |
| Official client | Pin the SDK and lockfile. Exercise auto negotiation and explicit version selection with discovery, a nonempty tool list, and a deterministic call. Record SDK/source differences instead of silently skipping cases. |
| Wire contracts | Cover malformed metadata/headers, request identity, argument shape, and body limits before execution; distinguish ingress errors from in-band tool failures. |
| Artifact | Verify the PR head, CI artifact hash, and installed native module origin. Then repeat on the published wheel/sidecar with the actual feature set; source tests are not release evidence. |
| Execution | The same declared sync/async tool must preserve result/job semantics through REST and MCP. A timeout hint is not a substitute for `execution: async`. |

Successful protocol tests do not prove full conformance or host correctness.
For response-correlation issues, also test a slow call followed by uniquely
marked fast calls on the same real host/session, tracing IDs through every hop.
Echoing the current request ID around a stale payload is not a fix. After a
timeout, query the existing job; never replay a mutation just to flush a queue.
Keep real-host, PR-artifact, and published-release acceptance separate.

## Install SOP Gate

Adapter lifecycle commands must follow
[`adapter-install-sop.md`](../../../docs/guide/adapter-install-sop.md). Import
`load_install_sop_schema()` and `INSTALL_EXIT_CODES` from
`dcc_mcp_core.deployment` so machine-readable results and process exit codes
stay compatible across adapters.

The shared Core front door preserves `install --json` as a plan and emits a
post-execution Install SOP v1 result for `install --execute --json`. Treat the
execution result as evidence: assert stable per-step states, rollback outcomes,
exit/stage/error codes, executable `next_steps`, nullable receipt state, and
verification state. Do not infer success from the earlier plan or expose raw
paths, subprocess output, exceptions, or secrets in either output stream.

Until live-host verification is implemented for the shared executor, a local
artifact verification step may be `ok` while `verify.directly_usable` remains
false with `LIVE_DCC_VERIFICATION_REQUIRED`. Keep that boundary in adapter
tests instead of treating package installation as live DCC readiness.
Any planner step that still requires operator or live-host work, such as
`register-dcc`, must be `deferred` rather than `ok`; a zero exit code does not
turn that manual boundary into completed registration.

Exercise the complete `plan -> execute -> verify -> status -> uninstall`
round trip in CI. The gate must also prove that failed replacement restores the
previous usable install, stale receipt paths are diagnosed precisely, and
bootstrap failures remain visible. A mock may prove the contract when the real
DCC cannot run in CI; retain the documented live-host validation gap.

## Validation Commands

Prefer repository-native commands. For Python projects, prefer `vx uv` when it
is available in the environment, then fall back to direct Python only when the
wrapper is unavailable or hides behavior you need to inspect.

Typical gates:

```bash
python -m ruff check src tests
python -m ruff format --check src tests
python -m pytest
```

For Rust/PyO3 core changes, run the workspace's `just` or `cargo` gates that
match the touched crates.

For gateway discovery performance, use deterministic tests or Criterion as the
regression gate. If a regression needs local diagnosis, build
`dcc-mcp-server` with `--no-default-features --features gateway-daemon,tracy`
and follow the [local Tracy workflow](https://github.com/dcc-mcp/dcc-mcp-core/blob/main/docs/guide/observability.md#6-local-tracy-profiling).
Do not wrap async work across `.await` in a Tracy zone; correlate those phases
with the existing request IDs and OTLP spans instead.

For `dcc-mcp-core` toolchain or dependency refreshes, prefer vx-managed Cargo so
local runs match CI:

```bash
vx cargo update
vx cargo tree -d
vx cargo build --workspace --all-targets --timings
```

## Live-DCC Smoke Shape

Every adapter should eventually provide one documented smoke:

1. Start the DCC host in the supported mode.
2. Start or load the adapter.
3. Discover one skill.
4. Load it.
5. Call one safe typed tool.
6. Verify host-visible state.
7. Stop the adapter and ensure registry rows are gone.

If CI cannot run the real DCC, keep the mock HTTP test in CI and document the
manual live smoke command in the adapter repository.

## PR Notes

PR descriptions should include:

- short summary of runtime or skill behavior changed;
- validation commands, without machine-specific paths;
- any live-DCC gap that remains;
- exact-head terminal CI and any protocol feature, SDK, or artifact evidence;
- the matching public Skill PR when Core changes authoring or testing contracts,
  or a concise reason no Skill update is needed;
- linked core issues for deferred shared APIs.
