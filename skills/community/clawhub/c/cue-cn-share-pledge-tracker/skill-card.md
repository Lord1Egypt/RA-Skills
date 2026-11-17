## Description:

A-share pledge tracking: chain one shareholder's pledge and release announcements into a balance timeline, six elements per pledge and three per release, cumulative as before → after, each anchored to the announcement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Financial analysts and market research assistants use this skill to track an A-share shareholder's successive pledge and release announcements as a sourced balance timeline. It records announcement quotes, source anchors, and before-and-after totals while leaving risk judgments and ratio calculations to human review.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security assessment flags external parsing and MCP discovery as privacy concerns; one referenced script received only partial analysis.

Mitigation: Use external parsing only when needed, avoid submitting private URLs or local paths unless their disclosure is acceptable, and review the partially analyzed script before use.

Risk: The pledge checker verifies that percentages appear in quoted rows but does not establish that the underlying values or balance arithmetic are correct.

Mitigation: Check quoted facts against the original announcements and have a person independently verify percentages and balance arithmetic before relying on the note.

## Reference(s):

- [Pledge terms and field definitions](references/pledge-terms.md)
- [Cue MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown note with announcement quotes, source anchors, and before-and-after balance entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records disclosed percentages without calculating them; missing announcement details are identified for follow-up.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and CHANGELOG.md; server release 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
