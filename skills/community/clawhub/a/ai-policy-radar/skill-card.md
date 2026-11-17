## Description:

Scans user-provided Markdown policy notes for AI regulatory terms and themes, then summarizes matching entries with file references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance teams and developers use the skill to review their own AI policy notes for regulatory topics across jurisdictions and identify entries worth investigating. It does not fetch live regulatory updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local notes may be incomplete or outdated and could be mistaken for a live regulatory feed.

Mitigation: Verify important legal conclusions against official regulatory sources.

Risk: Scanning an unintended directory could expose unrelated local notes to the agent.

Mitigation: Invoke the skill explicitly and select only policy-note directories you intend the agent to read.

## Reference(s):

- [AI Policy Radar on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-policy-radar)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text summary of matching policy-note lines, themes, and filenames]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the Markdown files supplied; an empty match is not evidence that no regulations changed.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
