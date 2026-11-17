## Description:

Organizes multiple Chinese-language sources into a traceable research brief with dated citations, named gaps, and conclusions reserved for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and researchers use it to turn multiple Chinese-language announcements, reports, and web pages into a source-traceable brief for preliminary screening, industry updates, competitor comparisons, or policy checks. It leaves judgments and final decisions to a human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional connection instructions send an API key to a destination that is not checked in the instructions.

Mitigation: Verify the exact destination independently, require HTTPS, and use a limited-scope key. The bundled local tools can run without the key.

Risk: The checker can pass briefs with section-order or source-anchor errors, and brief content still needs review against original sources.

Mitigation: Manually check section order and source anchors, then verify each claim against its cited source before relying on the brief.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huhoo/skills/cue-cn-research-brief)
- [Data channel configuration](https://cuecue.cn/hub/mcp)
- [Document parsing configuration](https://cuecue.cn/hub/omni-reader)
- [API key information](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Four-section Markdown research brief with [S#] source anchors and a dated source list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Names missing items and definitions; leaves judgment calls for human review.]

## Skill Version(s):

0.1.6 (source: server-resolved release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
