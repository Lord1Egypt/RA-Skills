## Description: <br>
Delivery Notifier fetches delivery emails from Gmail, filters likely personal courier updates, extracts tracking details, and sends WhatsApp alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[o0o-sp](https://clawhub.ai/user/o0o-sp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals or operators use this skill to monitor a Gmail inbox for personal delivery notifications and receive concise WhatsApp alerts with courier and tracking information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private Gmail contents and forwards shipment details to a hard-coded WhatsApp number with weak safeguards. <br>
Mitigation: Use only with a mailbox and WhatsApp recipient you control, replace the hard-coded phone number, and minimize retained state. <br>
Risk: The artifact includes a debug script that can print full email fetch responses and message bodies. <br>
Mitigation: Remove or disable the debug script before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/o0o-sp/delivery-notifier) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [WhatsApp message text and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Gmail credentials from environment variables, writes notification state, and sends alerts to a configured WhatsApp recipient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
