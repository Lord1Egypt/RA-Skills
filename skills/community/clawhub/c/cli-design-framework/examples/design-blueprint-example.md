# Design Blueprint Example — `axon`

> A local AI agent runtime that manages agent sessions, tool sandboxes, approval flows, and execution governance.

## 1. Purpose

Provide a local CLI that lets a human operator start, observe, steer, and govern AI agent sessions — including tool-use sandboxing, human-in-the-loop approval, and execution lifecycle — while exposing a structured secondary surface for headless batch execution and programmatic event consumption.

## 2. Classification

- **Primary role:** Runtime
- **Primary user type:** Human-Primary
- **Primary interaction form:** Interactive CLI
- **Statefulness:** Sessionful
- **Risk profile:** High Side-Effect
- **Secondary surfaces:** `axon exec --json` (batch execution), NDJSON event stream, scriptable session control
- **Confidence level:** High

## 2b. Classification reasoning

**Why Runtime, not Capability.**
`axon` manages agent *execution* — it starts sessions, brokers tool calls through a sandbox, mediates approval flows, and governs what a running agent is allowed to do. The core abstraction is a *live execution context*, not a set of CRUD-able resources. A Capability CLI controls objects that exist at rest (issues, images, DNS records); `axon` controls processes that exist *in flight*. The fact that sessions can be listed, inspected, or resumed does not make them "resources" in the Capability sense — `tmux` sessions and `docker` containers are also listable, but tmux and Docker are classified by what they *run*, not by what they *store*. If you designed `axon` as a Capability CLI, you would end up with `axon session create / get / update / delete` — a CRUD shell around an execution engine, which is a category mistake. The command structure should reflect lifecycle verbs (`start`, `attach`, `stop`, `approve`, `deny`) rather than resource-mutation verbs.

**Why Interactive CLI, not TUI.**
`axon`'s primary surface is a connected, prompt-driven terminal session with streaming output and inline approval prompts. That makes it an **Interactive CLI** in this blueprint: the operator is conversing with a live runtime inside a single terminal flow, not navigating a full-screen layout with panels, panes, or persistent dashboard chrome. A future version could add a true TUI as an alternate surface, but that is not the primary interaction form assumed here. The *role* still remains Runtime because the CLI's center of gravity is execution governance. Classify the role by *what is controlled*; classify the interaction form by *how the user drives it*.

**How classification drives every subsequent section.**
- *Runtime role* → command structure uses lifecycle/governance verbs, not CRUD verbs (§4). Introspection surfaces describe execution state, not object schemas (§7).
- *Human-Primary user type* → human-readable output is the default; structured output is a secondary surface, not the primary contract (§6). Help and examples must be strong (§7).
- *Interactive CLI interaction form* → primary surface is a connected interactive session; batch exec is a deliberate secondary mode with its own contract (§11).
- *Sessionful statefulness* → session identity, resume, and attach/detach are core design requirements, not bolted-on features (§8).
- *High Side-Effect risk* → a concrete risk ladder with per-level guardrails is mandatory (§9). Approval flows are a first-class primitive, not a future nice-to-have.

## 3. Primary design stance

Optimize for a human operator who starts an agent session, watches it run, intervenes when the agent requests approval, and steers or terminates execution when needed. The interactive session is the primary surface; the human is the governor, not a spectator.

`axon` is **not** trying to be a headless agent orchestrator, a machine-to-machine execution protocol, or a resource CRUD tool. Batch and programmatic surfaces exist to support CI, testing, and script-driven workflows — but they are secondary to the interactive governance experience.

## 4. Command structure

**Shape:** Lifecycle-and-governance verbs at the top level, not noun-first CRUD.

```
axon start [--model ...] [--tools ...] [--policy ...]   # start a new session
axon attach <session-id>                                  # reconnect to a running session
axon stop <session-id>                                    # terminate a session
axon approve <request-id>                                 # approve a pending tool call
axon deny <request-id> [--reason ...]                     # deny a pending tool call
axon status [<session-id>]                                # inspect session state
axon list                                                 # list sessions
axon logs <session-id>                                    # view execution transcript
axon exec [--json] <prompt>                               # headless batch execution (secondary)
axon policy <subcommand>                                  # manage governance policies
```

**Why this shape.** Runtime role drives lifecycle verbs. The operator's primary actions are *start, attach, steer, approve, stop* — these are execution verbs, not resource verbs. `approve` / `deny` are first-class top-level commands because Human-Primary + High Side-Effect means the approval flow is a core interaction, not an edge case buried in subcommand flags. `axon exec` is deliberately separate from `axon start` to make the boundary between interactive governance and headless batch execution explicit.

## 5. Input model

**Primary:** Interactive-first. During an active session, input is conversational — the operator sends messages, approves/denies requests, and issues steering commands through the session interface. Session startup uses flags (`--model`, `--tools`, `--policy`, `--sandbox`) for configuration.

**Secondary:** `axon exec` accepts flags + prompt for batch execution. `axon policy` subcommands use flags-first input for policy CRUD. No raw-payload-first path is needed in v1 — the input domain (model selection, tool lists, policy names, natural-language prompts) maps cleanly to flags and positional arguments.

**Where machine input belongs:** `axon exec --json` accepts a structured request on stdin for programmatic invocation. This is the *only* raw-payload entry point, and it is explicitly a secondary surface.

## 6. Output model

**Default (TTY):** Human-readable. Session output streams agent reasoning, tool calls, approval prompts, and results in a formatted interactive view. `axon list` and `axon status` produce human-readable tables/summaries.

**Structured secondary:** `axon exec --json` emits a JSON result object. `axon logs --json <session-id>` emits NDJSON transcript. `axon status --json` emits machine-readable session state. `axon list --json` emits a JSON array of session summaries.

**Contract level:** The `--json` surfaces are strong contracts — field names are stable across minor versions, and breaking changes require a major version bump. The interactive session view is a human-optimized presentation layer with no stability guarantee on layout or formatting.

## 7. Help / discoverability / introspection

**Help and examples (high priority — Human-Primary drives this):**
- Every command must have `--help` with at least one realistic example.
- `axon start --help` must show a complete start-to-finish example including model, tools, and policy flags.
- `axon approve --help` must explain what happens when an approval times out.

**Discoverability (high priority):**
- `axon` with no arguments shows a short command summary grouped by lifecycle phase (start → interact → govern → inspect).
- Unknown commands suggest the closest match.

**Introspection (execution-state-oriented, not object-schema-oriented):**
- `axon status <session-id>` shows: model, active tools, sandbox state, pending approvals, elapsed time, token usage.
- `axon policy show <policy-name>` shows the effective governance rules.
- No generic `describe` / `schema` / `fields` surface is needed — Runtime CLIs expose *execution state*, not *object schemas*. This is a direct consequence of the Runtime classification. A Capability CLI would need field-level introspection; `axon` needs state-level introspection.

## 8. State / session model

**Derived from classification:** Sessionful statefulness means session identity is a core primitive, not an add-on. This section exists *because* the classification says Sessionful — for a Stateless or Config-Stateful CLI, this section would say "not applicable" and move on.

**Session identity:** Every `axon start` creates a session with a unique ID (short hash, human-typeable). Sessions are the unit of execution, governance, and auditability.

**Resume / attach / detach:**
- `axon attach <session-id>` reconnects to a running session from any terminal.
- Closing the terminal detaches but does not stop the session (agent continues in background).
- `axon stop <session-id>` explicitly terminates.
- Detached sessions with pending approvals remain blocked until the operator re-attaches or the approval times out (configurable).

**History / transcript:**
- `axon logs <session-id>` replays the full execution transcript (agent messages, tool calls, approvals, results).
- Transcripts are stored locally and are the primary audit artifact.

**State inspection:**
- `axon status` (no args) lists all active/paused sessions.
- `axon status <session-id>` shows detailed session state.

## 9. Risk / safety model

**Derived from classification:** High Side-Effect means every mutation path needs explicit guardrails. The risk ladder below is not generic advice — it is driven by what `axon` actually controls (agent execution, tool calls, system access).

**Low-risk operations (no confirmation):**
- `axon list`, `axon status`, `axon logs` — read-only inspection.
- `axon attach` — connecting to an existing session does not change state.

**Medium-risk operations (confirmation or explicit flag):**
- `axon start` with tools that have filesystem/network access — display the tool manifest and sandbox policy at startup, require `--confirm` or interactive acknowledgment.
- `axon approve` for tool calls within the session's declared sandbox — approve proceeds, but the tool call's scope is logged.

**High-risk operations (strict guardrails):**
- `axon approve` for tool calls that exceed the session's sandbox policy (e.g., agent requests a tool not in the allowed set) — explicit warning, require `--force` or interactive confirmation with the specific risk explained.
- `axon stop --force` (kill without graceful shutdown) — requires `--force` flag; without it, `axon stop` attempts graceful termination.
- `axon exec` in batch mode with broad tool access — requires an explicit policy file; refuses to run with no governance constraints.

**Dry-run:** `axon exec --dry-run` shows the resolved execution plan (model, tools, sandbox, policy) without starting the agent.

**Audit:** Every session produces a transcript log. Every approval/denial is timestamped and attributed. `axon logs --json <session-id>` is the machine-readable audit surface.

**Sanitization:** Prompts passed via `axon exec` are logged verbatim but never interpreted as shell commands. Tool call arguments are sandboxed and validated against the declared tool schema before execution.

## 10. Hardening model

**Input validation:**
- Session IDs and request IDs are validated syntactically before any operation.
- Unknown flags are rejected, not silently ignored.
- `axon exec` with `--json` on stdin validates the request object against a known schema and rejects unknown fields.

**Field stability:** `--json` output field names are stable. New fields may be added; existing fields are not removed or renamed without a major version bump.

**Exit codes:**
- `0` = success.
- `1` = general error.
- `2` = invalid input / usage error.
- `3` = session not found.
- `4` = approval denied / policy violation.
- `5` = timeout (approval timeout, execution timeout).
- Distinct exit codes matter because `axon exec` in CI pipelines needs to distinguish "agent failed" from "policy blocked the run."

**Timeout / idempotency:**
- `axon stop` is idempotent — stopping an already-stopped session succeeds with a notice.
- `axon approve` / `axon deny` on an already-resolved request fails with a clear error and exit code, not a silent no-op.
- Approval requests have a configurable timeout; expired approvals auto-deny and log the timeout.

## 11. Secondary surface contract

**`axon exec --json` (batch execution surface):**
- *Who:* CI pipelines, test harnesses, scripts.
- *What:* Run a prompt headlessly with a declared policy, return a structured result.
- *Contract:* Strong. Input schema is documented; output schema has stable field names; exit codes are meaningful. This is the primary machine surface.
- *Boundary:* `exec` is fire-and-forget — it does not support mid-execution approval. If the policy requires human approval, `exec` either uses auto-approve rules from the policy file or fails. This constraint is deliberate: interactive governance belongs on the primary surface.

**NDJSON event stream (`axon attach --events <session-id>`) — planned for post-v1:**
- *Who:* Monitoring tools, dashboards, agent-orchestration scripts.
- *What:* Tap into a running session's event stream (tool calls, approvals, agent messages) as newline-delimited JSON.
- *Contract:* Strong for event types and field names; event ordering is best-effort. This is a secondary observation surface, not a control surface — you cannot send commands through it. Included here to define the contract target; actual implementation is deferred to post-v1 (see §12) because the event vocabulary needs to stabilize first.
- *Boundary:* Read-only. Steering and approval happen through the primary interactive surface or dedicated commands (`axon approve`), not through the event stream.

**Scriptable session control (`axon approve`, `axon deny`, `axon stop` from a second terminal):**
- *Who:* Operators managing multiple sessions, automation scripts that handle approval queues.
- *What:* Issue governance commands to a session without being attached to it.
- *Contract:* Convenience layer with stable command signatures but no versioned wire protocol. These are CLI commands, not an API.

## 12. v1 boundaries

**v1 includes:**
- `start`, `attach`, `stop`, `approve`, `deny`, `status`, `list`, `logs` — the core lifecycle and governance commands.
- One sandbox backend (local process isolation).
- One policy format (YAML file declaring allowed tools, approval rules, timeouts).
- `axon exec --json` for batch execution.
- `axon logs --json` for machine-readable transcript export.
- Local session storage (filesystem-based).

**v1 defers:**
- Remote session management (multi-machine, cloud-hosted agents).
- Plugin system for custom tool backends.
- Multi-agent orchestration (sessions containing multiple cooperating agents).
- Web dashboard or GUI.
- `axon attach --events` (NDJSON event stream) — useful but not needed before the core lifecycle is stable.
- Policy inheritance / composition (v1 uses flat policy files).

**What would be premature abstraction:**
- Building a generic "resource management" layer for sessions — sessions are execution contexts, not REST resources. CRUD semantics would fight the runtime model.
- Designing a plugin API before the core sandbox and approval interfaces are stable — plugin boundaries cannot be drawn until v1 usage reveals where extensibility is actually needed.
- Adding a policy DSL or policy engine — v1 should validate that the policy model is correct with simple YAML before investing in expressive power.
- Exposing the event stream before the event vocabulary stabilizes — shipping an unstable event contract creates backwards-compatibility debt.

## 13. Direction for implementation

**Optimize for:** Interactive session governance. The attach → observe → approve/deny → steer loop is the core experience. If this loop is fast, clear, and trustworthy, the CLI succeeds.

**Do not optimize for:** Headless orchestration, agent-to-agent communication, or API-first design. These may matter later, but optimizing for them now would pull design decisions away from the human governance experience.

**Acceptable patterns:**
- Session state stored as local files (JSON or SQLite) — simple, inspectable, no server dependency.
- Approval flow as a blocking prompt in the interactive session, with timeout-based auto-deny for detached sessions.
- `axon exec` as a thin wrapper that creates a session, runs to completion, and returns the result — no special "batch mode" engine.

**What would be a category mistake:**
- Designing `axon` as `axon session create / session get / session update / session delete` — this treats sessions as REST resources and buries the execution lifecycle under CRUD verbs. The Runtime classification specifically warns against this.
- Making `axon exec --json` the primary surface and treating the interactive mode as a convenience wrapper — this inverts the Human-Primary design target.
- Requiring a policy file for interactive use — the operator *is* the governance layer in interactive mode; forcing policy-file configuration for a human sitting at the terminal adds friction without safety benefit.
- Omitting the approval flow from v1 — High Side-Effect classification means governance is not a nice-to-have; it is the product.
