## Description:

Guides agents in finding, safely reading, verifying, and handing off another coding agent's task state across command-line and desktop tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lawson2019](https://clawhub.ai/user/lawson2019)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to review or resume another coding agent's work, reconstruct task state from project artifacts when transcripts are missing, or prepare a Markdown handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented npx installation commands are unpinned.

Mitigation: Pin a version or reviewed source revision before installing.

Risk: Security inspection was partial, with unresolved references.

Mitigation: Review the remaining components and references before deployment.

Risk: Session transcripts can contain secrets, and pattern-based redaction may miss them.

Mitigation: Review and redact transcript content before sharing it or including it in a handoff.

## Reference(s):

- [Agent session store reference](references/agent-stores.md)
- [Cross-agent handoff landscape](references/landscape.md)
- [ClawHub release page](https://clawhub.ai/lawson2019/skills/agent-task-takeover)
- [Project repository](https://github.com/lawson2019/agent-task-takeover)
- [npm package](https://www.npmjs.com/package/agent-task-takeover)
- [skills.sh listing](https://www.skills.sh/lawson2019/agent-task-takeover)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Code, Files]

**Output Format:** [Markdown task-state reports and handoffs, with shell commands and optional code or file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content depends on the target session and available project artifacts.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
