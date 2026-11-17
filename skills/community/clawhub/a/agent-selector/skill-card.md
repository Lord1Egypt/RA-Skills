## Description:

Agent-Selector matches a task description to one of 146+ bundled specialist agent personas and supports automatic or manual persona selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krislu1221](https://clawhub.ai/user/krislu1221)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route tasks to specialist personas and load matching prompt context for coding, design, testing, product, marketing, sales, support, strategy, and operations work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled personas can direct agents toward public posting, scheduled work, or payment handling without sufficient approval boundaries.

Mitigation: Review selected persona prompts before use in environments with browser, scheduler, social-media, payment, or secret access; disable or tightly sandbox high-impact personas and require explicit confirmation for public posts, scheduled runs, and payments.

Risk: Persona loading can change an agent's behavior even when the selector itself is described as read-only.

Mitigation: Scan the package before deployment and keep tool permissions, credential access, and execution approvals separate from persona selection.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krislu1221/skills/agent-selector)
- [Skill Usage Documentation](artifact/SKILL.md)
- [Release Notes and Setup](artifact/README.md)
- [ClawHub Package Metadata](artifact/clawhub.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown or plain text with agent identifiers, persona prompt content, and optional Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selects from bundled local persona files; package metadata says no external APIs are required.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
