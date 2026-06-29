## Description: <br>
Cue Opportunity Mining uses Cue to run deep research for opportunity-mining scenarios, cross-referencing public data sources and returning conclusions with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business researchers use this skill to run Cue deep research for lead generation, company due diligence, industry-chain research, public-data opportunity analysis, and related business-development workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch or update an external Cue runner before execution. <br>
Mitigation: Review or pin the cue-skills runner source before use in controlled environments. <br>
Risk: Business, company, or client queries are sent through online Cue research flows and may rely on a stored Cue API key. <br>
Mitigation: Review sensitive queries and credential handling before approving a run. <br>
Risk: Deep research runs consume Cue credits. <br>
Mitigation: Require explicit confirmation before each credit-consuming run. <br>
Risk: The output is based on public data and may be incomplete for diligence, legal, underwriting, or compliance decisions. <br>
Mitigation: Treat reports as research inputs and verify conclusions against authoritative sources before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-opportunity-mining) <br>
- [Cue playbook API](https://cuecue.cn/api/playbook) <br>
- [Cue runner source](https://github.com/sensedeal/cue-skills) <br>
- [Cue runner mirror](https://gitee.com/sensedeal/cue-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research guidance and reports with source links, plus inline shell commands for runner setup when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before credit-consuming research runs; may return an empty result instead of fabricating content.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
