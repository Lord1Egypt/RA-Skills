## Description:

Runs Cue's 财报深读 financial-research workflow to analyze recent public-company financial reports, business drivers, earnings quality, supply-chain signals, fund flows, and related risk evidence with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to launch Cue research on listed companies and financial-report topics, then receive a sourced research report and risk-signal summary. It supports financial statement review, fund-flow tracking, audit-opinion or convertible-bond checks, and pre/post guidance verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to clone or update and run external cue-skills code that can change after this release was reviewed.

Mitigation: Review the external repository before installation or execution, pin a trusted revision where possible, and proceed only if the user trusts Cue/sensedeal.

Risk: Runs may consume Cue credits using the user's local Cue API key.

Mitigation: Confirm the selected Cue buddy, research subject, and expected credit use with the user before running.

Risk: The generated financial analysis uses public data and should not be treated as diligence, legal, underwriting, or investment advice.

Mitigation: Keep source links in the report, separate facts from interpretations, and have a qualified reviewer validate material conclusions before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-financial-deep-read)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue API key setup](https://cuecue.cn/hub/api-key)
- [cue-skills runner repository](https://github.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with source links and inline shell commands for setup and run steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final reports depend on live Cue playbook availability, user confirmation for credit spend, and the external cue-skills runner.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
