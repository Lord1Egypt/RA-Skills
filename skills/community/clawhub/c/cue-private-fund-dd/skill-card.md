## Description: <br>
Runs Cue deep research for private-fund due diligence using cross-referenced public data and source-linked conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to run Cue private-fund due diligence workflows for fund managers, products, FOF screening, registrations, filings, regulatory signals, and related-party checks using public data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup may fetch and run code from an external repository. <br>
Mitigation: Review the external repository before use and pin installation to a trusted commit or release instead of auto-updating from the latest branch. <br>
Risk: Deep research runs consume Cue credits. <br>
Mitigation: Require explicit user confirmation before starting a credit-consuming run. <br>
Risk: The skill relies on public data and does not replace formal due diligence, legal review, or underwriting. <br>
Mitigation: Keep source links in the report and require users to verify findings against authoritative records before acting on them. <br>
Risk: The runner may return no content for a selected subject or template. <br>
Mitigation: Report the empty result and suggest retrying with a different subject or template rather than fabricating findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-private-fund-dd) <br>
- [Cue playbook API](https://cuecue.cn/api/playbook) <br>
- [Cue skills runner](https://github.com/sensedeal/cue-skills) <br>
- [Cue skills runner mirror](https://gitee.com/sensedeal/cue-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown] <br>
**Output Format:** [Markdown report with source links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Cue runner, Cue API key, user confirmation before credit-consuming runs, and public-data availability; returns no fabricated content when the runner reports empty.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
