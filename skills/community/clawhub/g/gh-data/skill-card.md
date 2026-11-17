## Description:

股海罗盘 is a Chinese-language A-share and ETF analysis skill that gathers market, technical, financial, fund-flow, and research-report data, compares signals against historical patterns, and can generate DOCX reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunbinpy](https://clawhub.ai/user/sunbinpy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather China A-share and ETF market data, compare current signals with historical patterns, and generate concise Markdown-style summaries or DOCX reports. The outputs are informational research aids and are not investment advice.

### Deployment Geography for Use:

Global; data coverage is focused on China A-share and ETF markets.

## Known Risks and Mitigations:

Risk: The skill creates a persistent local API key and the security evidence reports risky key storage and transmission.

Mitigation: Use only a low-value or trial key until the publisher documents key storage and rotation and uses HTTPS for credential-bearing calls; remove or rotate the local key after testing.

Risk: Preview outputs may include paid upgrade links.

Mitigation: Review generated analysis and DOCX reports before sharing them, and treat upgrade links as payment content rather than analysis evidence.

Risk: Stock-analysis output can be mistaken for investment advice.

Mitigation: Preserve the skill's risk disclaimer and review outputs so they remain framed as historical data and statistical reference, not buy, sell, or hold guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunbinpy/skills/gh-data)
- [Publisher profile](https://clawhub.ai/user/sunbinpy)
- [股海罗盘 product homepage](https://www.oraskl.com/ghdata-admin)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown-style analysis text with optional DOCX report files and generated chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local report paths, risk disclaimer text, and preview-mode upgrade links.]

## Skill Version(s):

2.2.51 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
