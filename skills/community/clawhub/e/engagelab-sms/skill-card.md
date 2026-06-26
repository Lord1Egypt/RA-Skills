## Description: <br>
Call EngageLab SMS REST APIs to send SMS messages and manage SMS templates and signatures (sender IDs). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devengagelab](https://clawhub.ai/user/devengagelab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate requests, code, and guidance for sending EngageLab SMS messages and managing SMS templates and sender ID signatures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help send real SMS messages, including scheduled sends. <br>
Mitigation: Require the agent to show recipients, template parameters, schedule time, and template ID before any live send. <br>
Risk: The skill can help create, update, or delete SMS templates and sender ID signatures. <br>
Mitigation: Require explicit review of the operation, target IDs, and requested changes before modifying or deleting messaging resources. <br>
Risk: EngageLab credentials may be exposed through shared logs, prompts, or shell history. <br>
Mitigation: Use limited-scope credentials where available and keep dev_key and dev_secret out of shared logs and command history. <br>


## Reference(s): <br>
- [Template & Signature API Reference](references/template-and-signature-api.md) <br>
- [EngageLab SMS API Error Codes](references/error-codes.md) <br>
- [EngageLab SMS API Base URL](https://smsapi.engagelab.com) <br>
- [EngageLab SMS Messages Endpoint](https://smsapi.engagelab.com/v1/messages) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, API request examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include placeholder credentials and resource IDs when live values are not supplied.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
