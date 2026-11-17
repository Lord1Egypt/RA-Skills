## Description:

Tracks an A-share merger or restructuring across multiple announcements, arranging milestones and step-by-step changes into a sourced timeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

A-share research and deal-monitoring teams use it to organize official announcements for one restructuring by date, compare changes between releases, and link each point to its source.

### Deployment Geography for Use:

China (A-share announcements)

## Known Risks and Mitigations:

Risk: ClawScan flagged retrieval-date behavior and undisclosed remote tool discovery as inconsistent with the stated tracking purpose; the evidence does not establish intent and the scan was partial.

Mitigation: Before installing, review the release source and version, clarify how retrieval dates and remote discovery work, and confirm what requests send and what file access the host permits.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-restructuring-tracker)
- [Cue MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Chinese Markdown change brief with a dated announcement timeline, sourced changes, pending items, and source links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cross-period tracking requires multiple announcements; each timeline entry includes a source and retrieval date. The brief excludes investment recommendations.]

## Skill Version(s):

0.1.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
