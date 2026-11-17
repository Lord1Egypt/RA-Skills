## Description:

Ai Workforce turns an OpenClaw agent into an autonomous business operator with progressive trust, structured knowledge management, worker delegation patterns, and reflection cycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[km2411](https://clawhub.ai/user/km2411)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operators use this skill to configure an OpenClaw agent as an AI Chief for onboarding, persistent business memory, worker delegation, trust management, and scheduled reflection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad autonomous authority can cause workspace changes, worker activity, or business actions beyond user expectations.

Mitigation: Start action categories at propose and require explicit confirmation for onboarding writes, cron jobs, worker spawning, spending, external communications, public posts, deleting data, commitments, and sensitive systems.

Risk: Persistent business memory can store personal context, credentials, or sensitive operational data.

Mitigation: Do not store passwords, API keys, payment data, SSNs, auth tokens, or raw PII in workspace files; review memory, bank, USER, and shared files before reuse or backup.

Risk: Automated Git backup and scheduled reflection behavior can persist or publish private context.

Mitigation: Enable remote backup only after review, keep the repository private, exclude sensitive memory files, and require explicit confirmation before Git commits, pushes, or remote backup setup.

Risk: Delegated workers may receive excess context or follow injected instructions from user-provided content.

Mitigation: Share only curated org-level context with workers, wrap user content, give narrow task constraints, and review worker outputs before delivery.

## Reference(s):

- [ClawHub Ai Workforce page](https://clawhub.ai/km2411/skills/ai-workforce)
- [Bootstrap first meeting guide](references/bootstrap.md)
- [Worker delegation patterns](references/delegation.md)
- [Operational patterns](references/operational.md)
- [Reflection cycle prompts](references/reflection-prompts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline command and prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes templates for persistent workspace memory, shared worker context, scheduled reflection prompts, and optional Git backup behavior.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact/_meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
