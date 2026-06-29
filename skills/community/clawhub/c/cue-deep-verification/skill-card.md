## Description: <br>
Runs Cue deep research for Deep Verification scenarios, cross-checking multiple public sources and returning source-linked conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to run Cue deep-verification research for enterprise due diligence, disclosures, regulatory checks, fact checking, and cross-source public-data verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow may clone or update Cue runner code under ~/.cue/cue-skills. <br>
Mitigation: Confirm the Cue runner source is trusted before setup or update, as recommended by the security guidance. <br>
Risk: Deep research runs consume Cue credits. <br>
Mitigation: Require explicit user confirmation for the exact subject and selected Cue module before running. <br>
Risk: The skill covers public data and may produce incomplete or non-authoritative conclusions. <br>
Mitigation: Keep source links in the output, review conclusions against primary sources, and do not treat reports as a substitute for professional due diligence, legal, or insurance review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-deep-verification) <br>
- [Cue playbook API](https://cuecue.cn/api/playbook) <br>
- [Cue runner source](https://github.com/sensedeal/cue-skills) <br>
- [Cue runner mirror](https://gitee.com/sensedeal/cue-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance, Research guidance] <br>
**Output Format:** [Markdown report with source links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Cue account API key; prompts for confirmation before credit-consuming research runs; may clone or update the Cue runner under ~/.cue/cue-skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
