## Description: <br>
Runs Cue deep research for post-loan monitoring by cross-checking public data and returning source-linked conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial-risk, credit, and due-diligence users use this skill to monitor borrowers, track company events, review disclosure or regulatory signals, and prepare evidence-linked post-loan research notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may clone or update the external cue-skills runner and execute it locally. <br>
Mitigation: Review the external runner source or pin a trusted copy before use when stricter supply-chain control is required. <br>
Risk: Deep research runs can spend Cue credits. <br>
Mitigation: Confirm the selected research buddy, subject, and expected credit use with the user before running. <br>
Risk: Results are based on public sources and may be incomplete for lending, legal, or underwriting decisions. <br>
Mitigation: Review the linked sources and treat the report as research support rather than a substitute for formal diligence. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangxiaoxu/skills/cue-post-loan-monitoring) <br>
- [Cue Playbook API](https://cuecue.cn/api/playbook) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with source links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Cue account/API key; deep research runs may consume Cue credits after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
