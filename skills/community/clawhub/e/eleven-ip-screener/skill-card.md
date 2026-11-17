## Description:

Screens unadapted novels from major Chinese web-novel platforms for short-drama or AI comic adaptation potential, scoring candidates by pacing, character fit, scene complexity, audience resonance, novelty, episode fit, and production cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elevenzhou](https://clawhub.ai/user/elevenzhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, producers, and content research teams use this skill to compare novels for short-drama or AI comic adaptation potential and produce a ranked TOP5 screening report with score breakdowns, highlights, risks, and selection advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on web searches and recent public novel-platform data, which may be incomplete, stale, or inconsistent across platforms.

Mitigation: Cite the public sources used for each candidate and mark missing scoring dimensions explicitly instead of filling unsupported values.

Risk: Broad Chinese trigger phrases such as 小说筛选 could activate the workflow outside the intended adaptation-screening context.

Mitigation: Use explicit prompts about novel or IP adaptation screening before invoking the skill.

Risk: Adaptation-rights status may be difficult to verify from public data.

Mitigation: Exclude works clearly marked as sold or authorized, and flag uncertain rights status for human review before business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elevenzhou/skills/eleven-ip-screener)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with ranked entries, score tables, source links, risk notes, and selection recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses recent public platform data where available and asks the agent to cite sources for scoring decisions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
