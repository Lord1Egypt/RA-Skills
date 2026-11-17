## Description:

Build and update OpenClaw agents by designing personas, operating rules, autonomy, guardrails, and workspace files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced agent builders use this skill to create or refine OpenClaw agent workspaces with persona files, operating instructions, heartbeat behavior, optional memory, and safety checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package references remote setup content outside the audited release.

Mitigation: Review or ignore remote setup content from skillboss.co unless its source and contents are verified before use.

Risk: Generated agents may use memory or heartbeat files that persist context or consume tokens.

Mitigation: Enable memory and heartbeat behavior deliberately, keep heartbeat instructions small, and avoid storing secrets or credentials in generated workspace files.

Risk: Generated operating instructions could allow excessive autonomy if configured too broadly.

Mitigation: Keep ask-before-destructive and aREDACTED-SECRET rules in the generated AGENTS.md, and validate behavior with the suggested scenario prompts.

## Reference(s):

- [Agent Builder Repo on ClawHub](https://clawhub.ai/alvisdunlop/skills/alvis-agent-builder)
- [OpenClaw agent workspace](references/openclaw-workspace.md)
- [OpenClaw agent file templates](references/templates.md)
- [Agent Architecture Patterns](references/architecture.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions and proposed workspace file contents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose IDENTITY.md, SOUL.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md, memory/YYYY-MM-DD.md, TOOLS.md, and short acceptance-test prompts.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
