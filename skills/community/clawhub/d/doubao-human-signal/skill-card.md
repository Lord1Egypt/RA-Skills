## Description:

Checks draft writing for formulaic patterns and returns a heuristic AI-flavor score to guide revisions, not determine authorship.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and editors check drafts such as emails, applications, and social posts for repetitive phrasing and rhythm, then compare revisions using a heuristic score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow encourages reducing AI-detectability before sending sensitive communications.

Mitigation: Use it for clarity and style, not to conceal AI involvement where authorship transparency is expected.

Risk: A heuristic score may be mistaken for proof of authorship.

Mitigation: Treat the score as a revision hint and never use it alone to judge or accuse a writer.

Risk: The skill requests Write permission despite describing a read-only checking workflow.

Mitigation: Avoid granting Write access unless it is needed and justified by the publisher.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/doubao-human-signal)
- [LGD governance reference linked in README](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, Analysis, JSON]

**Output Format:** [Plain text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [0–100 heuristic score, three score bands, matched clichés, and a non-verdict disclaimer.]

## Skill Version(s):

1.1.1 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
