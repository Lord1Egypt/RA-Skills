## Description: <br>
EngageLab Omnichannel communications tool (SMS, WhatsApp, Email) with template management and messaging capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GPTBOTS](https://clawhub.ai/user/GPTBOTS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support teams use this skill to prepare and send EngageLab SMS, WhatsApp, and email communications, including approved-template discovery and message payload construction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing commands can upload unintended files or private material if run against the wrong folder. <br>
Mitigation: Before publishing, confirm the target path, review included files, remove secrets or private material, and use ignore rules where supported. <br>
Risk: The skill requires channel credentials for EngageLab SMS, WhatsApp, and Email APIs. <br>
Mitigation: Provide credentials only through the documented environment variables and avoid placing secrets directly in prompts, skill files, or publishable artifacts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/GPTBOTS/engagelab-omni-connect) <br>
- [EngageLab SMS API endpoint](https://smsapi.engagelab.com/v1/messages) <br>
- [EngageLab WhatsApp API endpoint](https://wa.api.engagelab.cc/v1/messages) <br>
- [EngageLab Email API endpoint](https://email.api.engagelab.cc/v1/mail/send) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with API request examples and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EngageLab channel credentials supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
