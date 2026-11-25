## Description:

This assistant researches foreign regulations using official databases and produces Chinese reports with bilingual key provisions, legislative context, applicability boundaries, and source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External legal, compliance, and business teams can use the assistant to research cross-border regulatory questions and prepare Chinese summaries with official source links. Its reports support research and do not replace formal legal advice.

### Deployment Geography for Use:

United States, European Union, and Singapore (primary coverage)

## Known Risks and Mitigations:

Risk: The security summary reports concerns about billing access and sending research questions to a third-party service, which may affect account credits or expose sensitive business context.

Mitigation: Check billing behavior before use and avoid sending confidential or personal details unless the service's data handling is acceptable.

Risk: The skill retrieves or updates an external runner, and the security assessment was partial because a referenced runner file was unavailable.

Mitigation: Review the runner and pin a known revision before execution; review remote changes before updating it.

Risk: The workflow includes promotional prompts and links that may be unexpected during research tasks.

Mitigation: Review promotional content and destinations before sharing information or following links.

Risk: Coverage is limited and the reports are not formal legal opinions.

Mitigation: Check cited primary sources and consult qualified counsel for consequential legal decisions.

## Reference(s):

- [Cue platform](https://cuecue.cn)
- [Cue playbook](https://cuecue.cn/playbook)
- [EUR-Lex](https://eur-lex.europa.eu)
- [U.S. Code](https://uscode.house.gov)
- [eCFR](https://www.ecfr.gov)
- [Singapore Statutes Online](https://sso.agc.gov.sg)
- [External runner repository referenced by the skill](https://github.com/sensedeal/cue-skills)
- [Runner repository mirror referenced by the skill](https://gitee.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Files]

**Output Format:** [Chinese Markdown research reports with bilingual legal terms and official source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coverage focuses on the United States, European Union, and Singapore; conclusions include links for source checking.]

## Skill Version(s):

1.0.12 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
