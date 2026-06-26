# Classification Examples

Use these examples to stabilize classification decisions. Treat them as representative anchors, not rigid templates.

## 1. Capability — `gh`

- **Primary role:** Capability
- **Primary user type:** Human-Primary
- **Primary interaction form:** Batch CLI
- **Statefulness:** Config-Stateful (auth tokens, aliases, repo-level defaults)
- **Risk profile:** Mixed
- **Secondary surfaces:** `--json`, `--jq`, `--template`

Why it fits:
- Primarily controls GitHub resources and collaboration objects.
- Human-readable output is the default.
- Machine-readable output exists as a strong secondary surface (`--json`, `--jq`, `--template`), making it close to Balanced — but the default output, help text, and discoverability all optimize for human operators, keeping the center of gravity on Human-Primary.
- It is not a runtime CLI and not a workspace manager.

## 2. Runtime — `codex`

- **Primary role:** Runtime
- **Primary user type:** Human-Primary
- **Primary interaction form:** TUI
- **Statefulness:** Sessionful
- **Risk profile:** High Side-Effect (agent execution with code, filesystem, and network mutation capabilities)
- **Secondary surfaces:** `exec --json`, batch execution, machine event streams

Why it fits:
- Primarily controls agent execution, sessions, sandboxing, approvals, and runtime behavior.
- The main product surface is an interactive TUI; batch execution and machine event streams are secondary surfaces.
- Read-only inspection exists (session list, status) but the dominant activity is execution governance with high mutation potential.

## 3. Environment / Workspace — `tmux`

- **Primary role:** Environment / Workspace
- **Primary user type:** Human-Primary
- **Primary interaction form:** TUI
- **Statefulness:** Sessionful, Long-running, Attach/Detach-capable
- **Risk profile:** Mixed
- **Secondary surfaces:** Batch CLI command surface for scripting (`tmux new-session`, `tmux send-keys`, etc.)

Why it fits:
- Primarily manages terminal workspace state.
- The primary experience is the full-screen workspace inside a tmux session; the `tmux` CLI command surface is a secondary control interface used for setup, automation, and scripting.
- Session identity and attach/detach are core.
- It is not primarily about business resources or agent execution.

## 4. Workflow / Orchestration — `make`

- **Primary role:** Workflow / Orchestration
- **Primary user type:** Human-Primary
- **Primary interaction form:** Batch CLI
- **Statefulness:** Stateless
- **Risk profile:** Mixed (varies by target; build targets are low-risk, deployment targets can be high-risk)
- **Secondary surfaces:** CI and automation invocation

Why it fits:
- Primarily orchestrates multi-step tasks and dependencies.
- The core abstraction is targets and execution flow, not persistent resources.

## 5. Package / Build / Toolchain — `uv`

- **Primary role:** Package / Build / Toolchain
- **Primary user type:** Human-Primary
- **Primary interaction form:** Batch CLI
- **Statefulness:** Config-Stateful (lockfiles, virtualenv, toolchain installations)
- **Risk profile:** Mixed
- **Secondary surfaces:** CI automation and reproducible toolchain flows

Why it fits:
- Primarily manages dependency, environment, and toolchain lifecycle.
- It is neither a generic workflow CLI nor a runtime CLI.

## 6. Meta / Control-Plane — `git config`

- **Primary role:** Meta / Control-Plane
- **Primary user type:** Human-Primary
- **Primary interaction form:** Batch CLI
- **Statefulness:** Config-Stateful (durable configuration effects that change downstream system behavior)
- **Risk profile:** Mixed
- **Secondary surfaces:** Scripted configuration management

Why it fits:
- Primarily controls configuration that changes how another system behaves.
- The controlled object is not a resource or workflow target but an effective configuration layer.

## 7. Balanced — `kubectl`

- **Primary role:** Capability (+ Meta / Control-Plane secondary)
- **Primary user type:** Balanced
- **Primary interaction form:** Batch CLI
- **Statefulness:** Config-Stateful (kubeconfig context, namespace state)
- **Risk profile:** Mixed (reads like `get`/`describe`/`logs` are safe; mutations like `delete`/`apply`/`scale` affect live cluster state)
- **Secondary surfaces:** `-o json`, `-o jsonpath`, `--dry-run=server`, extensive label/field selectors

Why it fits:
- Used equally heavily by human operators (interactive debugging, ad-hoc inspection) and by CI/CD pipelines, GitOps controllers, and automation scripts.
- Human-readable table output is the default, but structured output is not an afterthought — it is a production-critical surface.
- Neither side dominates: removing the human experience would break operator workflows; removing the machine surface would break the entire ecosystem.

## 8. Agent-Primary — `gws` (Google Workspace CLI)

- **Primary role:** Capability
- **Primary user type:** Agent-Primary
- **Primary interaction form:** Batch CLI
- **Statefulness:** Stateless
- **Risk profile:** High Side-Effect (wraps mutation-capable Workspace APIs; agent-primary means most invocation paths are mutations)
- **Secondary surfaces:** Schema introspection (`gws schema`), MCP JSON-RPC surface, Gemini Extension surface, SKILL.md agent knowledge packaging

Why it fits:
- Designed from day one for AI agents as the primary consumer.
- Input model is raw-payload-first (`--json`, `--params`) rather than flags-first.
- Runtime schema introspection replaces static documentation as the primary discoverability surface.
- Context window discipline (field masks, NDJSON pagination) is a first-class design concern.
- Input hardening is designed against agent-specific failure modes (hallucination, path traversal, double-encoding), not just human typos.
- Human debugging use exists but is secondary.

Agent-Primary design patterns visible in `gws` (use as reference when designing Agent-Primary CLIs): raw-payload-first input model in §5; JSON-default output with human-readable as convenience layer in §6; schema introspection replacing help as primary discoverability in §7; `--fields` for context-window discipline in §6; agent-specific input hardening (unknown field rejection, double-encoding detection) in §10.

Input sketch:
- Primary machine path is raw-payload-first: `gws users create --json @payload.json` or `gws groups patch --params @patch.json`.
- Flags remain available for lightweight debugging and human inspection, but they are not the primary entry path.
- Unknown fields, wrong enum values, and double-encoded JSON are rejected loudly rather than coerced.

Output sketch:
- Default output is JSON with stable field names and a documented contract level.
- Human-readable output exists as a convenience layer for debugging, not as the canonical surface.
- `--fields` and field masks are first-class so agents can limit payload size and context-window pressure.

Discoverability sketch:
- Runtime schema introspection (`gws schema`, `gws users describe`) is the primary discovery path.
- Help text points to schema commands rather than trying to inline every field in prose.
- Examples emphasize minimal valid payloads, field selection, and contract-safe mutation patterns.

## 9. Agent-Only — MCP server binaries / internal execution engines

- **Primary role:** varies (Capability, Runtime, or Meta depending on the tool)
- **Primary user type:** Agent-Only
- **Primary interaction form:** Machine Protocol / Event Stream Surface
- **Statefulness:** varies
- **Risk profile:** varies
- **Secondary surfaces:** minimal or none; human surfaces limited to version/health checks

Why this category exists:
- Agent-Only CLIs are rarely standalone consumer products. They more commonly exist as execution engines behind higher-level tools (e.g., `runc` behind `docker`, MCP server binaries behind agent frameworks).
- The defining characteristic: there is no meaningful human-interactive workflow. Human invocation is limited to debugging, health checks, or version inspection.
- Design consequences: human discoverability is low-priority; machine contract stability, schema rigor, and input hardening are the dominant concerns.

Note: If you find yourself classifying a user-facing product as Agent-Only, re-examine whether it is truly Agent-Only or Agent-Primary with a thin human debugging surface.

## Notes

- A product may expose multiple roles through different surfaces or subcommands.
- Classify the **primary** role first.
- Add secondary surfaces afterward.
- Do not promote TUI or REPL to role type; treat them as interaction forms.

## Coverage notes

Not every taxonomy value requires a dedicated anchor example. The following values are intentionally left without a standalone example because they are either self-explanatory or rare enough that an example would not improve calibration:

- **Pure Human** (User Type): Rare in modern CLIs. Most tools have at least some script/automation use. Examples include pure display utilities (`cal`, `banner`). If the CLI has no plausible machine consumer, classify as Pure Human and design entirely for discoverability and ergonomics.
- **REPL** (Interaction Form): Well-understood pattern (Python REPL, `sqlite3`, `node`). Classify the role by what the REPL controls, not by the fact that it is a REPL.
- **Read-heavy** (Risk Profile): CLIs that primarily query/inspect without mutation (e.g., `jq`, monitoring CLIs, network diagnostics). Low guardrail intensity for individual operations, but read-only does not mean risk-free — resource-intensive reads (network sweeps, large-scale queries, CIDR scans) require conservative concurrency defaults and scope warnings to prevent accidental overload. Focus on output quality, machine-readable contracts, and exit codes as the primary machine signal.
- **Irreversible / External-Action Heavy** (Risk Profile): CLIs that trigger actions that cannot be undone (revoking certificates, rotating secrets, sending emails, issuing payments, publishing packages). Design patterns for this risk level:
  - Multi-step confirmation on the most destructive operations (type the resource name, not just `y/N`); no `--yes` bypass for truly irreversible actions.
  - Mandatory `--reason` flag on irreversible mutations for audit attribution.
  - Audit-write-before-execute: write the audit event first; if it fails, abort the operation.
  - Automatic impact preview before confirmation (blast radius, affected consumers, active usage stats).
  - Explicit scope flags on all mutations (e.g., `--env prod`); never infer destructive scope from a config default.
  - `--dry-run` that validates against the backend in read mode, producing a realistic preview.
