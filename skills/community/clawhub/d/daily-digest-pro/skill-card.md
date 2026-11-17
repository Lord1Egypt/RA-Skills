## Description:

Generates a structured daily work digest from memory notes, session transcript results, and optional git activity, with source cross-referencing for accomplishments, decisions, pending items, and in-progress work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to turn a day's local notes, session transcript results, and optional git activity into a concise work digest for standups, recaps, or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local memory notes, session transcript results, and git history may contain private information.

Mitigation: Review the generated digest before sharing it and remove secrets, personal data, or sensitive project details.

Risk: A daily digest can be misleading if it includes unsupported or duplicated activity.

Mitigation: Include only items that trace to concrete sources and deduplicate repeated events across memory, session, and git sources.

## Reference(s):

- [Daily Digest Supporting Description](references/DESCRIPTION.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown daily digest with sectioned bullet lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aims for 5-15 lines, matches the user's primary language, and may optionally write a dated digest file.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
