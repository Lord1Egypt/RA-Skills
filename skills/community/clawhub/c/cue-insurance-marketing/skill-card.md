## Description: <br>
Runs Cue deep research for insurance marketing scenarios, including cross-source public data checks and source-linked conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Insurance, marketing, and product-analysis users use this skill to run Cue research on insurance product comparisons, marketing leads, suitability checks, policy-term reviews, and compliance boundary checks. It helps produce source-linked research reports from public data and reminds users that the output does not replace due diligence, legal advice, or underwriting review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install, update, and run mutable external Cue code while using a local Cue API key. <br>
Mitigation: Install only if Cue, the sensedeal/cue-skills repository, and the local Cue account are trusted; review or pin the runner source before first use. <br>
Risk: Running deep research can consume Cue credits. <br>
Mitigation: Require explicit user confirmation before executing a selected research run. <br>
Risk: Insurance research outputs may be mistaken for due diligence, legal advice, or underwriting review. <br>
Mitigation: Keep source links in the report and treat findings as public-data research that requires qualified review before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangxiaoxu/skills/cue-insurance-marketing) <br>
- [Cue playbook source](https://cuecue.cn/playbook) <br>
- [Cue playbook API](https://cuecue.cn/api/playbook) <br>
- [Cue skills repository](https://github.com/sensedeal/cue-skills) <br>
- [Cue skills Gitee mirror](https://gitee.com/sensedeal/cue-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with source links and inline shell commands for runner setup and execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May consume Cue credits after explicit user confirmation; failed or empty runs should be reported without fabricating findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
