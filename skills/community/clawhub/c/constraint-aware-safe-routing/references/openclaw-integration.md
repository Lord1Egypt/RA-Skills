# OpenClaw integration guidance

Read this reference when applying the architecture to an OpenClaw installation.

## What the skill can do

The skill can teach an eligible OpenClaw agent to:

- classify a request into local response, cloud reasoning, tool proposal, or abstention;
- identify novelty and constraint-shift signals;
- request current authorization evidence;
- produce structured reasons and audit fields;
- design or review benchmarks and gates.

## What the skill cannot do

The skill cannot itself:

- add a new tool;
- prevent another instruction from reaching an existing tool;
- establish authoritative identity or permissions;
- guarantee that a model follows the workflow;
- create a hard security boundary.

OpenClaw documentation defines skills as instruction packages. Implement enforcement in a plugin or wrapper that owns the effectful tool call.

## Recommended layering

```text
OpenClaw agent + this skill
        |
        | structured action proposal
        v
tool wrapper or plugin
        |
        +-- load current principal and policy
        +-- validate action, resource, and schema
        +-- check policy/tool versions and freshness
        +-- fail closed when unavailable
        +-- issue one-use execution capability
        v
effectful backend or sandbox
```

Do not expose a raw effectful backend alongside the guarded wrapper. Otherwise the model may bypass the intended control path.

## Installation locations

Choose one supported OpenClaw skill root:

- workspace-specific: `<workspace>/skills/constraint-aware-safe-routing/`;
- shared personal library: `~/.openclaw/skills/constraint-aware-safe-routing/`;
- shared AgentSkills library: `~/.agents/skills/constraint-aware-safe-routing/`.

Workspace skills have higher precedence. OpenClaw does not treat Codex's native `$CODEX_HOME/skills` directory as an OpenClaw skill root.

After copying the folder, inspect eligibility with:

```bash
openclaw skills list --eligible
openclaw skills info constraint-aware-safe-routing
```

Invoke it explicitly with `$constraint-aware-safe-routing` when testing. Automatic selection remains available because the skill does not disable model invocation.

## Hardening checklist

- Expose only guarded effectful tools to the agent.
- Use a typed schema for action proposals and tool results.
- Delimit untrusted content before any model call.
- Resolve user identity outside model-generated text.
- Fetch policy and tool versions at execution time.
- Redact credentials, raw capabilities, and unnecessary personal data from logs.
- Test before/after constraint pairs and provider outages.
- Monitor false blocks and missed legitimate actions as well as unsafe executions.

