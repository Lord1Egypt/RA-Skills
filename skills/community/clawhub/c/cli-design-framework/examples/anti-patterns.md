# Anti-Patterns

Three worked negative examples showing common classification and design mistakes when applying the CLI design framework. Each case shows a concrete scenario, what went wrong, why the framework flags it as an error, and what the correct approach looks like. Two additional shorter cases cover interaction-form and statefulness errors.

---

## 1. Agent-washing a human-primary CLI

### Scenario

A team maintains `store`, a human-primary capability CLI for managing cloud storage buckets. Typical usage looks like:

```
store bucket list
store object get abc-123
store object delete abc-123    # prompts "Are you sure?"
```

The team reads about "agent-first CLI design" and ships a redesign:

- Human-readable table output is removed; JSON becomes the only output format.
- `store object get <id>` is replaced with `store object get --json '{"id":"...","fields":"..."}'` as the sole input path.
- Most `--help` examples are stripped because "agents don't read help."
- Confirmation prompts on destructive operations are removed because "agents need non-interactive mode."

### What went wrong

Category mistake — applying agent-primary design patterns to a human-primary CLI.

The CLI's actual user base is humans typing commands in a terminal. The redesign optimized for a user type that barely exists here while actively degrading the experience for the real users. Removing human-readable defaults, help text, and safety prompts doesn't make the CLI "modern" — it makes it hostile to its primary audience.

### Why it's wrong

The framework classifies this CLI as **Human-Primary** by user type. Human-primary CLIs require:

- Human-readable output as the default surface (tables, colored text).
- Strong `--help` with examples and discoverability.
- Confirmation prompts for destructive operations as a safety layer.

None of these conflict with also supporting machines. The mistake is treating human and machine surfaces as mutually exclusive rather than layered.

### Correct approach

Keep human-readable table output as the default. **Add** `--json` as a secondary machine-readable surface. Keep `--help` rich with examples. Keep confirmation prompts for interactive use; add `--yes` / `--force` flags for automation paths. The principle: layer machine surfaces on top of human defaults, never replace them.

---

## 2. Treating a runtime CLI as a capability CLI

### Scenario

A team builds `neuron`, an AI agent runtime (similar in role to `claude` or `codex`). They design it as a clean resource-CRUD interface:

```
neuron session list
neuron session get <id>
neuron session delete <id>
neuron tool list
neuron tool install <name>
neuron model list
neuron model set <name>
```

The command surface looks tidy. But there is no way to actually run an agent session, no approval model for tool use, no sandbox governance, no attach/resume/fork for live sessions, no event streaming, and no execution lifecycle management.

### What went wrong

Role misclassification — the CLI's primary role is **Runtime** (execution governance), but it was designed as if it were a **Capability CLI** (resource CRUD).

The team focused on "what objects exist" (sessions, tools, models) and built CRUD around them. But the core of a runtime CLI is not object inventory — it is how execution proceeds, who approves what, what is sandboxed, and how sessions live, pause, resume, and die.

### Why it's wrong

The framework distinguishes Runtime CLIs from Capability CLIs precisely because their primary surface is different. A runtime CLI's primary commands are execution-oriented: start, approve, pause, resume, attach, fork. Resource listing is a secondary concern. By building only CRUD, the team shipped a CLI that can describe agent sessions but cannot govern them — which is the entire point of a runtime.

### Correct approach

Start with the execution model as the primary surface:

- `neuron run "task description"` — start a session.
- `neuron resume <session-id>` — continue a paused session.
- `neuron attach <session-id>` — connect to a live session's event stream.

Build approval and sandbox governance into the execution flow (approval prompts, `--sandbox` flags, permission policies). Then layer resource inspection (`neuron session list`, `neuron tool list`) as secondary capability surfaces on top. Execution first, inventory second.

---

## 3. "We have JSON output, so we're script-friendly"

### Scenario

A CLI adds `--json` to its `list` and `get` commands. The README proudly states: *"Script-friendly: supports JSON output for automation."* But in practice:

- Field names change between minor versions without notice or deprecation.
- Some commands return `{"data": [...]}` while others return bare arrays.
- Exit code is always `0`, even when 3 of 5 items in a batch operation failed.
- There is no `--fields` or field selection mechanism.
- There is no `describe` or schema command.
- Error messages in JSON mode are still unstructured text on `stderr`.

### What went wrong

Surface existence does not equal contract maturity. Having a `--json` flag is necessary but not sufficient for a real machine-readable secondary surface.

Scripts and agents that consume JSON output depend on structural stability: predictable field names, consistent envelope shapes, meaningful exit codes, and parseable error output. Without these, `--json` is a formatting convenience, not a contract. Every downstream consumer becomes fragile.

### Why it's wrong

The framework requires that a machine-readable surface be evaluated on contract strength, not mere presence. A strong machine contract includes:

- **Field stability**: named fields don't disappear or rename without a major version bump.
- **Consistent envelope**: every command uses the same top-level shape (e.g., always `{"data": ...}`).
- **Meaningful exit codes**: `0` = full success, `1` = partial failure, `2` = complete failure.
- **Field selection**: `--fields id,name,status` for bandwidth- and context-window-conscious consumers.
- **Schema support**: a `describe` or `--schema` surface so agents can introspect the contract.

The CLI in this scenario satisfies none of these. Claiming "script-friendly" based on `--json` alone is an incomplete contract.

### Correct approach

Define and document field stability guarantees (ideally tied to semver). Standardize the JSON envelope across all commands. Make exit codes meaningful and documented. Add `--fields` for selective output. Consider a `describe` or `--schema` surface for agent consumers. Ensure errors in JSON mode are also structured JSON. The flag is the easy part — the contract is the work.

---

## 4. Promoting TUI to a role

### Scenario

A team classifies their monitoring dashboard CLI as a "TUI tool" — the role is TUI, the interaction form is TUI, and the design is driven by "TUI best practices." They build rich widgets, keyboard shortcuts, and live-updating panels, but never clarify whether the CLI is primarily monitoring resources (Capability), managing a running system (Runtime), or governing a workspace (Environment/Workspace).

### What went wrong

TUI is an interaction form, not a role. Calling a CLI a "TUI tool" is like calling a web app a "browser app" — it describes the delivery channel, not what the tool controls. Without identifying the role, the team cannot decide what the command structure should look like, what objects need introspection, or what risk model applies.

### Why it's wrong

The framework explicitly separates interaction form from role. A TUI can serve any role: `lazygit` is a TUI over a Capability CLI (git resources), `htop` is a TUI over an Environment/Workspace CLI (system processes), and `codex` is a TUI over a Runtime CLI (agent execution). Promoting TUI to role makes these three tools look identical in the taxonomy, when they actually need fundamentally different command structures, state models, and risk profiles.

### Correct approach

Classify the role by what the CLI controls, not by how it renders. Then classify the interaction form as TUI. The role determines command structure and state model; the interaction form determines surface ergonomics and feedback style. Both matter, but they are orthogonal.

---

## 5. Over-engineering statefulness for a Config-Stateful CLI

### Scenario

A team builds a package manager CLI. Users run `pkg install <name>`, `pkg list`, `pkg update`. The CLI writes a lockfile and modifies a local dependency directory — classic Config-Stateful behavior. But the team, inspired by database CLIs, adds:

- `pkg session start` / `pkg session end` to "track installation transactions"
- `pkg history` showing a "session log" of past installations
- `pkg rollback --session <id>` to undo a "session"
- A session ID attached to every `pkg install` invocation

### What went wrong

The CLI invented session semantics where none are needed. A lockfile and dependency directory are durable side-effects (Config-Stateful), not sessions. Users don't think of `pkg install lodash` as happening "inside a session" — they think of it as a single action that changes the project state.

### Why it's wrong

The framework's Statefulness dimension distinguishes Config-Stateful from Sessionful precisely to prevent this. Config-Stateful means "durable side-effects but no session identity." The correct design primitives are `init` / `reset` / `status` / `diff` — operations that inspect or manage durable state without imposing session structure. Adding sessions to a Config-Stateful CLI creates cognitive overhead (users must understand session lifecycle), implementation complexity (session tracking, rollback logic), and API surface area (session CRUD) — all for a mental model that doesn't match how users actually think about package installation.

### Correct approach

Keep the CLI Config-Stateful. Use `pkg install`, `pkg list`, `pkg update`, `pkg remove` as stateless-feeling commands with durable effects. Add `pkg status` to show current state, `pkg diff` to show pending changes (if applicable), and `pkg reset` for clean-state recovery. If undo is needed, implement it as `pkg remove <name>` (reversing a specific action), not as session rollback.
