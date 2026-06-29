## Description: <br>
Runs Cue deep research for credit diligence, cross-referencing public data from multiple sources and returning source-linked conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Credit, diligence, and research teams use this skill to run Cue research workflows for company diligence, credit risk review, disclosure and regulatory checks, and pre-lending screening. It helps an agent select a live Cue research template, confirm credit use, run the research, and return the source-linked report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A deep research run may spend Cue credits. <br>
Mitigation: Confirm the selected Cue research workflow, subject, and credit use with the user before running. <br>
Risk: The workflow uses Cue services and local Cue credentials. <br>
Mitigation: Use it only where Cue access is approved, and protect the local Cue configuration that stores credentials. <br>
Risk: The workflow may clone or update the Cue runner from external repositories. <br>
Mitigation: Review the runner source and repository location before executing it in controlled environments. <br>
Risk: Public-data diligence reports can be incomplete or unsuitable as a sole basis for lending, legal, or underwriting decisions. <br>
Mitigation: Preserve source links, review conclusions manually, and apply formal diligence and compliance review before relying on the output. <br>


## Reference(s): <br>
- [Cue Credit Diligence on ClawHub](https://clawhub.ai/wangxiaoxu/skills/cue-credit-diligence) <br>
- [Cue playbook](https://cuecue.cn/playbook) <br>
- [Cue playbook API](https://cuecue.cn/api/playbook) <br>
- [Cue runner repository](https://github.com/sensedeal/cue-skills) <br>
- [Cue runner mirror](https://gitee.com/sensedeal/cue-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with source links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before spending Cue credits; final reports should keep source links intact.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
