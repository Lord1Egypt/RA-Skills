## Description:

Guides agents through context capture, serialization, compression, and retrieval workflows for preserving project knowledge across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[watermelon11](https://clawhub.ai/user/watermelon11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan and document context-saving workflows for project onboarding, long-running sessions, semantic retrieval, and knowledge transfer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad project capture can include private code, credentials, customer data, or internal architecture notes.

Mitigation: Use explicit capture scope, exclude secrets and sensitive files, and review saved context before storage or sharing.

Risk: Persistent or vector-database storage can retain sensitive context longer or wider than intended.

Mitigation: Prefer local storage unless external storage is approved, and define retention, deletion, and access-control rules for saved context.

Risk: Context-saving guidance may omit user-control boundaries for what is captured and restored.

Mitigation: Require human approval for capture granularity, storage format, semantic tags, and any restoration into future work sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/watermelon11/skills/context-management-context-save)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions]

**Output Format:** [Markdown with structured guidance and illustrative code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce context schemas, checklists, workflow steps, and storage guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
