## Description:

Scores text from 0 to 100 using surface-level writing patterns and reports a three-band, non-definitive AI-style indication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, reviewers, and developers can compare drafts for repetitive phrasing and uniform structure as a prompt for human review, not as proof of AI authorship.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Declared Read, Write, Bash, and WebFetch access exceeds this local scorer's needs and conflicts with its stated permissions.

Mitigation: Review requested tool permissions before installation; restrict access to local execution and input reading, without network or write permissions unless separately justified.

Risk: Pattern-based scoring may incorrectly suggest AI authorship, especially across languages and writing styles.

Mitigation: Treat scores only as review cues; check the text and context manually, and do not use scores alone for consequential decisions.

Risk: The --text option may interpret a path or @-prefixed value as a file to read.

Mitigation: Check whether the input is a file or literal text and only supply material authorized for analysis.

## Reference(s):

- [AI Reply Heuristics on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-reply-heuristics)

## Skill Output:

**Output Type(s):** [Text, Analysis]

**Output Format:** [Plain text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a 0–100 score, three-band label, matched phrases, and a non-definitive disclaimer.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; bundled frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
