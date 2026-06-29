## Description: <br>
Run Cue deep research for market-cap management scenarios with cross-source public data synthesis and source-linked conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, finance teams, and developers use this skill to run Cue research workflows for market-cap management, M&A target discovery, IPO forecasting, incentive-plan design, market monitoring, company overviews, and valuation diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may clone or update an external Cue runner and use the Cue account API key stored in the local Cue configuration. <br>
Mitigation: Install and run it only after trusting the Cue runner source, and avoid using it with subjects or queries that should not be sent to Cue. <br>
Risk: Deep research runs consume Cue credits and can return empty results. <br>
Mitigation: Require explicit user confirmation before each credit-spending run and report empty results without inventing findings. <br>


## Reference(s): <br>
- [Cue playbook API](https://cuecue.cn/api/playbook) <br>
- [Cue skills runner on GitHub](https://github.com/sensedeal/cue-skills) <br>
- [Cue skills runner mirror on Gitee](https://gitee.com/sensedeal/cue-skills) <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-market-cap-mgmt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and source-linked research reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Cue account API key, user confirmation before credit-spending research runs, and public-data-only due diligence limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
