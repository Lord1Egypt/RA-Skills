# Taxonomy

This taxonomy describes a CLI along five primary dimensions plus secondary surfaces.

## 1. User Type

Answer: who is the stable primary user?

- **Pure Human** — effectively human-only
- **Human-Primary** — mainly for humans, with secondary script/agent support
- **Balanced** — humans and agents are both first-class users
- **Agent-Primary** — mainly for agents/automation, with some human debugging/inspection use
- **Agent-Only** — fundamentally program/agent facing

Use **Balanced** only when removing either the human or machine surface would materially harm a core workflow. If automation exists but is still secondary to an operator-centric experience, classify as **Human-Primary**.

## 2. Role / Control-Surface Type

Answer: what does the CLI primarily control?

- **Capability** — resources, objects, actions, CRUD/query surfaces
- **Runtime** — agent/model/session/tool/sandbox/approval execution surfaces
- **Environment / Workspace** — workspaces, panes, sessions, layouts, shells, attach/detach
- **Workflow / Orchestration** — multi-step tasks, pipelines, goals, dependency chains
- **Package / Build / Toolchain** — dependencies, build, run, publish, environment/toolchain lifecycle
- **Meta / Control-Plane** — configuration, profiles, feature flags, policy, plugin/settings/control surfaces

When distinguishing **Meta / Control-Plane** from **Capability**: Meta CLIs primarily configure policy or settings that govern another system's behavior (rate limits, routing rules, feature flags, config layers). Capability CLIs primarily manage resources that exist at rest (issues, records, certificates, endpoints). If a CLI manages both resources and policy, classify by center of gravity — if the primary user action is "configure how the system behaves," lean Meta; if the primary user action is "manage discrete objects," lean Capability. Use hybrid notes to acknowledge the secondary role.

## 3. Interaction Form

Answer: how is it primarily used?

- **Batch CLI**
- **Interactive CLI** — prompt-driven conversational or wizard-style interaction within a single invocation; differs from REPL (no persistent eval loop) and TUI (no full-screen layout)
- **REPL**
- **TUI**
- **Machine Protocol / Event Stream Surface**

Interaction form describes the primary interaction pattern, not the data entry method. **Input model** (flags-first, raw-payload-first, dual-track, interactive-first) is a separate design property driven primarily by user type — it belongs in the blueprint's §5, not in this classification field. Do not combine interaction form and input model in the classification — e.g., write `Batch CLI`, not `Batch CLI with raw-payload-first input model`.

## 4. Statefulness

Answer: how much durable or ongoing state shapes use?

- **Stateless** — no durable state across invocations
- **Config-Stateful** — no sessions, but invocations produce durable side-effects (config files, lockfiles, environment changes, caches)
- **Sessionful** — explicit session identity across invocations
- **Long-running** — persistent process with ongoing state
- **Attach/Detach-capable** — sessions that survive disconnection and can be resumed

Remote resources having durable state does not, by itself, make the CLI Config-Stateful. Use **Config-Stateful** when durable local or user-scoped config, caches, lockfiles, or contexts materially shape invocation behavior. A pure remote CRUD CLI can still be **Stateless**.

## 5. Risk Profile

Answer: what is the dominant side-effect profile?

- **Read-heavy**
- **Mixed**
- **High Side-Effect**
- **Irreversible / External-Action Heavy**

## 6. Secondary Surfaces

Modern CLIs often have a primary identity plus secondary surfaces.

Examples:
- human-primary capability CLI + JSON secondary surface
- runtime CLI with TUI primary surface + machine event-stream secondary surface
- workspace CLI with interactive primary surface + scriptable control secondary surface

Always classify the primary role and primary interaction form first. Add secondary surfaces only afterward.

## Decision order

Use this sequence:
1. State the CLI purpose in one sentence.
2. Classify the primary role.
3. Classify the primary user type.
4. Classify the primary interaction form.
5. Classify statefulness.
6. Classify risk profile.
7. Note secondary surfaces.
8. Derive design consequences.

## Design consequence map

### Role type primarily drives
- command structure
- object model vs execution model vs workspace model
- expected introspection type
- what counts as a category mistake

Role-specific defaults:
- **Capability** → noun/verb or resource/action surfaces; resource-state introspection
- **Runtime** → lifecycle/governance verbs; execution-state introspection
- **Environment / Workspace** → workspace/session verbs; attach/detach and layout/state inspection
- **Workflow / Orchestration** → task/pipeline verbs; dependency-graph and run-state introspection
- **Package / Build / Toolchain** → lifecycle-phase verbs; dependency, environment, cache, and artifact introspection
- **Meta / Control-Plane** → config/policy/profile verbs; settings and effective-policy introspection

### User type primarily drives
- default output surface: Human-Primary/Balanced → human-readable default, `--json` secondary; Agent-Primary → JSON default, human-readable secondary (surface inversion)
- input model: Human-Primary → flags-first; Agent-Primary → raw-payload-first with schema introspection; Balanced → dual-track
- discoverability: Human-Primary/Balanced → help/examples/error suggestions; Agent-Primary → runtime schema introspection, `--fields` selection, context-window discipline
- hardening focus: Human-Primary → typo correction, readable errors; Agent-Primary → unknown field rejection, type validation, double-encoded JSON detection

### Interaction form primarily drives
- surface ergonomics
- progress/feedback style
- prompting/confirmation style
- event stream or view-layer needs

### Statefulness primarily drives
- need for session identity
- need for resume/fork/attach/detach
- need for history/transcript/state inspection
- for Config-Stateful CLIs: need for init/reset/status/diff of durable effects, without inventing session semantics

### Risk profile primarily drives
- dry-run needs
- confirmation and impact preview needs
- audit and sanitization needs
- hardening and guardrail intensity
- for Irreversible / External-Action Heavy: multi-step confirmation (not just `--yes`), mandatory attribution (`--reason`), audit-write-before-execute with abort-on-failure, automatic impact preview showing blast radius, explicit scope flags on all mutations (never infer destructive scope from defaults)
- for Read-heavy: conservative defaults for resource-intensive operations (concurrency limits, scope warnings) to prevent accidental overload of target systems

## Classification precision

Each dimension uses discrete representative labels, not continuous scales. When a CLI does not fall cleanly into one value:

1. **Pick the dominant value** — the one that best describes the CLI's center of gravity for that dimension.
2. **Add a parenthetical qualifier** if needed — e.g., `High Side-Effect (reads are safe but agent execution carries high mutation risk)`.
3. **Do not use slashes between two values** — `Mixed / High Side-Effect` is ambiguous. Pick one: `High Side-Effect` or `Mixed`, then qualify.
4. **Handle per-operation variation in the design/review body, not in the classification label.** The risk ladder (§9 in blueprints) is where per-operation risk variation is described in detail. The classification label captures the dominant profile.

The same principle applies to all dimensions. Statefulness values are roughly cumulative (a Long-running CLI is also Sessionful), so listing multiple values with commas is acceptable when the CLI genuinely exhibits all of them (e.g., `tmux`: Sessionful, Long-running, Attach/Detach-capable).
