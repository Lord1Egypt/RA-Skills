## Description:

Run retrospective analysis for campaigns on Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, and DSP/programmatic channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danyangliu-sandwichlab](https://clawhub.ai/user/danyangliu-sandwichlab)

### License/Terms of Use:


## Use Case:

Marketing, growth, and advertising operations teams use this skill to review campaign performance, diagnose variance drivers, and plan measurable next actions across paid media platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations based on incomplete KPI definitions, date ranges, or data-source scope could misstate campaign performance.

Mitigation: Require metric scope, date range, and data-source context before drawing conclusions, and mark low-confidence findings as directional.

Risk: Campaign optimization advice can affect paid media spend.

Mitigation: Use measurable recommendations with rollback or stop-loss conditions when spend risk exists.

Risk: Users may provide sensitive advertising account details while requesting analysis.

Mitigation: Use only the campaign data needed for the review and avoid providing account credentials unless a separate trusted integration explicitly requires them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/danyangliu-sandwichlab/skills/campaign-retrospective-analyst)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured analysis, query plans, caveats, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compact query specifications and JSON-shaped result examples when useful.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
