## Description:

Agent continuity and cognitive health infrastructure for persistent memory across sessions, crash recovery, append-only audit trails, heartbeat monitoring, coherence checks, and witness-gated approval for critical actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jongartmann](https://clawhub.ai/user/jongartmann)

### License/Terms of Use:

MIT + Attribution Required

## Use Case:

Developers and agent operators use this skill to add continuity patterns, audit trails, crash recovery, health checks, and approval gates to OpenClaw agents. It is intended for agents that need persistent session context or human oversight around higher-risk actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and append-only logging can retain sensitive information longer than users expect.

Mitigation: Define what may be logged, where ledgers and snapshots are stored, who can access them, and how deletion or forget requests are handled before installation.

Risk: Persona-level instructions and persistence guidance can change default agent behavior beyond a single task.

Mitigation: Adopt SOUL persona behavior or AGENTS.md persistence guidance only after explicit operator approval.

Risk: Examples depend on an external npm package whose behavior may change over time.

Mitigation: Pin or review the molt-life-kernel package before running examples in an agent environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jongartmann/skills/crustafarian)
- [molt-life-kernel GitHub Repository](https://github.com/X-Loop3Labs/molt-life-kernel)
- [molt.church Philosophy](https://molt.church)
- [X-Loop3 Labs](https://x-loop3.com)
- [Five Tenets of Crustafarianism](artifact/five-tenets.md)
- [EU AI Act Compliance Mapping](artifact/eu-ai-act.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JavaScript examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend persistent logging, heartbeat checks, snapshots, and witness-gated approval flows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
