## Description:

ChangeBrief compares previous and current knowledge snapshots to surface newly added information, changed claims, stale conclusions, conflicts needing a decision, and the three changes that deserve immediate action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Managers, operators, and knowledge workers use ChangeBrief to compare previous and current notes, documents, meeting summaries, research snapshots, policies, roadmaps, or release notes. It produces a concise delta brief that highlights important additions, changed claims, stale conclusions, conflicts needing a decision, and the top three action-worthy changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to Chinese-facing output, which may not match every deployment or reviewer audience.

Mitigation: Confirm the desired output language during deployment and adjust routing or prompts when an English or bilingual brief is required.

Risk: Broad change-briefing trigger wording can route requests that need a full summary, retrieval workflow, or separate decision brief.

Mitigation: Use this skill when the user provides or asks for before/after comparison, and route import, retrieval, or one-page decision brief tasks to the adjacent skills named in the artifact.

Risk: The generated priorities and stale-conclusion flags are decision-support guidance, not authoritative review.

Mitigation: Have a knowledgeable reviewer check high-impact changes before updating policies, roadmaps, legal assumptions, or customer commitments.

## Reference(s):

- [Change Signals](references/change-signals.md)
- [ChangeBrief ClawHub Page](https://clawhub.ai/harrylabsj/skills/changebrief)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown-style change brief or structured JSON analysis from local before/after text or files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese-facing brief text and can return raw JSON with counts, additions, changed claims, invalidations, decisions, priorities, and unmatched statements.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
