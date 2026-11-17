## Description:

Pre-market A-share morning brief: five market slots plus three instrument slots, each anchored to a source and retrieval date; the header declares filled-over-total and reconciles it against the slot table; gaps named both ways; judgement stays human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, including investors and analysts, use this skill before the A-share market opens to assemble an overnight or pre-market brief for a covered instrument list. It records eight source-anchored market and instrument slots, reports missing data, and leaves judgments to a human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports behavior beyond the stated briefing purpose; its inspection was partial.

Mitigation: Review the skill's behavior and outputs against the eight-slot briefing purpose before use.

Risk: The security guidance flags external handling of URLs or paths as an output-handling concern.

Mitigation: Verify URLs and paths before processing them, especially when supplied by an untrusted source.

Risk: The security guidance flags a provenance-check weakness, and the scan does not cover every component fully.

Mitigation: Verify the release source independently and inspect the partially covered component before deployment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-morning-brief)
- [Cue MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown structured note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One time point per brief; eight fixed slots with source and retrieval-date anchors, reconciled coverage and named gaps; judgment fields remain [待人工].]

## Skill Version(s):

0.1.3 (source: skill frontmatter, server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
