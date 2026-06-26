## Description: <br>
Delegate research, analysis, content, and data collection tasks to specialized agents through the ClawHarbor API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shadowpigy](https://clawhub.ai/user/shadowpigy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to delegate natural-language tasks that require outside research, data collection, writing, translation, or analysis, then return the delivered result to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task descriptions and resulting work are shared with the external ClawHarbor service and its human agents. <br>
Mitigation: Redact passwords, tokens, personal information, confidential business material, proprietary source code, and regulated data before submitting tasks. <br>
Risk: The workflow can present a Stripe payment link for user approval. <br>
Mitigation: Review the task summary, quoted price, and complete payment URL before paying. <br>


## Reference(s): <br>
- [ClawHarbor website](https://clawharbor.app) <br>
- [ClawHarbor API documentation](https://clawharbor.app/v1) <br>
- [ClawHub listing](https://clawhub.ai/shadowpigy/clawharbor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown, with optional inline shell commands for API usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task status, payment links, and delivered result text from the external ClawHarbor service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
