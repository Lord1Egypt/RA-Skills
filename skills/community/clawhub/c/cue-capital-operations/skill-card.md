## Description: <br>
Runs Cue deep research for capital operations scenarios, cross-checking public data sources and returning sourced conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Capital-markets researchers, analysts, and operators use this skill to run Cue research on corporate capital operations such as buybacks, equity incentives, M&A, event timelines, disclosures, and regulatory issues. It supports public-data research and should not be treated as legal, underwriting, or due-diligence advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow installs or updates an external Cue runner that reads the user's Cue API key from local configuration. <br>
Mitigation: Install only if comfortable with the Cue runner and keep the Cue API key managed through the expected local Cue configuration. <br>
Risk: Deep research runs can consume Cue credits. <br>
Mitigation: Confirm the credit-spend prompt before each run and stop if the selected research target or buddy is unclear. <br>
Risk: Outputs are based on public-data research and may be incomplete for legal, underwriting, or due-diligence decisions. <br>
Mitigation: Use sourced results as research inputs and review them with appropriate professional or compliance checks before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-capital-operations) <br>
- [Cue playbook API](https://cuecue.cn/api/playbook) <br>
- [Cue skills runner repository](https://github.com/sensedeal/cue-skills) <br>
- [Cue skills runner mirror](https://gitee.com/sensedeal/cue-skills) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with sourced links and inline shell commands when setup is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Cue account credits and explicit user confirmation before running deep research.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
