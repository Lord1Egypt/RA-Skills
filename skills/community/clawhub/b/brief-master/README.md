# brief-master

![Validate](https://github.com/LeoStehlik/brief-master/actions/workflows/validate.yml/badge.svg)

Write sharp, precise agent briefs for OpenClaw. Zero wasted tokens. Zero vague instructions.

Brief Master is an agent brief writer for AI coding workflows. It extracts 9 dimensions of intent, asks max 3 clarifying questions, applies the right format for your target agent, runs a token efficiency audit, and delivers one clean brief ready to fire.

Built for OpenClaw's multi-agent workflow: dev agents, code reviewers, testers, researchers, and cron jobs.

Inspired by [prompt-master](https://github.com/nidhinjs/prompt-master). Built as our own OpenClaw-native implementation.


## Safety Boundary

Brief Master only drafts execution briefs. Review the generated brief before handing it to an autonomous agent, especially commands, file paths, credentials, scheduled jobs, external services, and anything that changes code or system state.

The skill must not invent access, approval, hostnames, secrets, destructive commands, or cron schedules. If execution needs elevated privileges or persistent automation, the brief should say that explicit approval is required.

## Use Cases

- turn a messy request into a precise agent brief
- make acceptance criteria explicit before an agent starts work
- capture constraints, non-goals, inputs, and verification steps
- reduce rework from vague prompts and missing context

---

## The Problem

Every wasted token is a wasted API call.
Every vague word is a future bug.
Every missing acceptance criterion is a future rework cycle.

"Improve the translation system" is not a brief.
"Fix formSchemaTranslated being NULL for German locale — AC1: all 50 prompt rows have formSchemaTranslated populated after running translate/de endpoint" is a brief.

---

## Credibility Artifact

See [`examples/README.md`](examples/README.md) for the example index, or jump straight to [`examples/messy-to-clean-brief.md`](examples/messy-to-clean-brief.md) for a concrete messy request -> clean agent brief example with ACs, constraints, non-goals, and verification commands.

## The Pipeline

1. Detect the target agent and runtime
2. Extract 9 dimensions of intent
3. Ask max 3 clarifying questions (only if critical info is missing)
4. Apply the right format for the target agent
5. Run token efficiency audit
6. Deliver one clean, ready-to-use brief

---

## The 9 Dimensions

1. **Task** - what exactly should be done (one verb, one outcome)
2. **Input** - what does the agent need to start (files, machines, branches)
3. **Output** - what should exist when done
4. **Constraints** - what must not break
5. **Context** - only what changes what the agent does
6. **Audience/Role** - which agent, what runtime
7. **Memory** - what files to read first
8. **Success Criteria** - AC1, AC2, AC3 (testable, specific)
9. **Examples** - reference points that clarify expected behaviour

---


## When To Use Which Repo

Use this repo when the task is still too vague to hand to an agent safely. Brief Master turns messy intent into a clear brief with task scope, inputs, outputs, constraints, non-goals, acceptance criteria, and verification shape.

Use the neighbouring tools at different points in the workflow:

| Need | Use |
| --- | --- |
| Turn a fuzzy request into an executable agent brief | [Brief Master](https://github.com/LeoStehlik/brief-master) |
| Prove one coding task is actually done | [Proof Loop](https://github.com/LeoStehlik/proof-loop) |
| Improve repeated agent behaviour with evals | [Loopsmith](https://github.com/LeoStehlik/loopsmith) |
| Keep source-backed memory for long-running agents | [Sovereign Brain](https://github.com/LeoStehlik/decoupled-agent-memory) |
| Stop frontend agents producing generic UI sludge | [no-slop-ui](https://github.com/LeoStehlik/no-slop-ui) |

A practical chain looks like this: messy request -> Brief Master brief -> Proof Loop task -> Loopsmith eval if the same failure keeps recurring -> Sovereign Brain records the durable decision.

## Related Tools

- [Proof Loop](https://github.com/LeoStehlik/proof-loop) - use after Brief Master when the task needs frozen acceptance criteria, separate verifier roles, and durable proof artifacts.
- [Loopsmith](https://github.com/LeoStehlik/loopsmith) - use when recurring weak briefs or agent failures should become eval cases and promotion decisions.
- [Sovereign Brain](https://github.com/LeoStehlik/decoupled-agent-memory) - use as source-backed context for briefs that need current decisions, project state, or changed evidence.

## Installation

### OpenClaw

```json
{
  "skills": {
    "load": {
      "extraDirs": ["/path/to/your/skills"]
    }
  }
}
```

```bash
git clone https://github.com/LeoStehlik/brief-master.git /path/to/your/skills/brief-master
```

### Claude Code / Codex

Copy into `.agents/skills/brief-master/` or `.claude/skills/brief-master/`.

---

## Usage

```
Write me a brief for my dev agent to fix the translation timeout issue
```

```
Help me write a cron job prompt for overnight research
```

```
I need a code review brief for Sprint 5
```

---

## What's Inside

```
brief-master/
├── SKILL.md                           Core pipeline + quality rules
└── references/
    ├── 9-dimensions.md                Intent extraction framework
    └── brief-formats.md               Ready-to-use templates per agent type
```

---

## License

MIT - see [LICENSE](LICENSE)
