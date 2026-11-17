## Description:

Audits OpenClaw agent behavior-layer rules and prompt sources to identify drift, redundancy, conflict, focus loss, and weak behavior guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gkso](https://clawhub.ai/user/gkso)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review OpenClaw agent behavior files, distinguish core behavior rules from supporting evidence, and produce concrete restructuring recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may inspect behavior and memory files in the workspace being audited.

Mitigation: Confirm the audit target and scope before use, and avoid widening beyond core behavior files unless the user asks or the core files are insufficient.

Risk: Recommended restructuring changes could alter future agent behavior if applied without review.

Mitigation: Review proposed changes before applying them, especially changes to core behavior files such as AGENTS.md, SOUL.md, USER.md, MEMORY.md, TOOLS.md, IDENTITY.md, and HEARTBEAT.md.

## Reference(s):

- [OpenClaw behavior sources](references/openclaw-behavior-sources.md)
- [Output template for agent-rule-audit](references/output-template.md)
- [Problem types for agent-rule-audit](references/problem-types.md)
- [Agent Rule Audit on ClawHub](https://clawhub.ai/gkso/skills/agent-rule-audit)
- [gkso publisher profile](https://clawhub.ai/user/gkso)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with ranked findings and file-specific recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces audit conclusions and executable restructuring recommendations; it does not include executable code.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
