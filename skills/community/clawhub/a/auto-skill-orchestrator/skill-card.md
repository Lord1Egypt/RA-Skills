## Description:

Helps users draft an ordered written plan for coordinating multiple OpenClaw skills when they explicitly ask for workflow sequencing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to break a multi-skill task into ordered steps, record dependencies, and mark higher-risk actions for explicit approval before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow plans could include incorrect sequencing or misleading guidance for a multi-skill task.

Mitigation: Review the plan before execution and verify expected results against actual outcomes.

Risk: A plan may include destructive, credential-related, or system-changing steps.

Mitigation: Flag those steps for explicit user approval and redact secrets before logging or displaying them.

Risk: The server evidence notes a slug mismatch between artifact metadata and displayed release metadata, which may confuse reviewers.

Mitigation: Use the server-resolved release slug and publisher handle for the card, and confirm metadata before publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pmuhammadagus-byte/skills/auto-skill-orchestrator)
- [ClawHub Publisher Profile](https://clawhub.ai/user/pmuhammadagus-byte)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown checklist or ordered written plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planning-only output; execution remains with the user or agent after explicit approval.]

## Skill Version(s):

1.1.5 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
