## Description: <br>
Review Avito message drafts for clarity, consent, respectful tone, one clear next step, and safe checkout wording before a human decides what to send. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to review and improve Avito seller-facing message drafts before deciding what to send. It focuses on respectful wording, one clear next step, safe checkout language, and a short human-send checklist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user may provide sensitive account, payment, contact, or private chat data while asking for message review. <br>
Mitigation: Use only the message text and non-sensitive transaction context; omit phone numbers, payment details, cookies, private chat exports, and unnecessary personal identifiers. <br>
Risk: A draft may include unsafe checkout wording or off-platform payment suggestions. <br>
Mitigation: Keep checkout wording inside Avito-supported safe flows and do not advise off-platform payments. <br>
Risk: Reviewed text could be mistaken for permission to send messages or operate an Avito account automatically. <br>
Mitigation: Keep all account activity outside the skill; a human reviews and sends any final message. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zack-dev-cm/avito-outreach-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a revised Avito message, what changed, a human-send checklist, and a payment-safety reminder.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
