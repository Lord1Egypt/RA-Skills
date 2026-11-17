## Description:

Professional AI stock analysis for OpenClaw that fetches TTfox market sentiment, sector momentum, stock screening, capital-flow alerts, and individual stock diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hengruiyun](https://clawhub.ai/user/hengruiyun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an OpenClaw agent for stock-market research, including sentiment, sector rankings, high-rating stock screens, and stock-specific risk and recommendation summaries. Outputs should be treated as research support rather than trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock symbols, sector names, market parameters, and investment interests are sent to TTfox.

Mitigation: Inform users before external requests and avoid sending sensitive or unnecessary financial-interest details.

Risk: Documentation makes inconsistent live or real-time claims while evidence warns data may be delayed.

Mitigation: Present outputs as delayed research signals, not current trading data or high-frequency trading guidance.

Risk: Generated recommendations may be mistaken for investment advice.

Mitigation: Label outputs as educational market research and require users to make independent investment decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hengruiyun/skills/ai-stock-master)
- [Publisher Profile](https://clawhub.ai/user/hengruiyun)
- [TTfox Intelligence Server](https://master.ttfox.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown and text responses with Python examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fetched JSON-derived market summaries, stock symbols, ratings, recommendations, and risk levels.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
