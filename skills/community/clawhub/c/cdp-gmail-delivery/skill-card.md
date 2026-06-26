## Description: <br>
Sends Gmail messages with optional attachments from an operator-controlled Chrome debug session using Gmail CDP automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joustonhuang](https://clawhub.ai/user/joustonhuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send Gmail messages from the local machine through a visible, logged-in Chrome session, including optional file attachments when Gmail permits them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can send email and attachments from a logged-in Gmail session without a separate built-in approval gate. <br>
Mitigation: Before each run, independently verify the recipient, subject, body, and attachments in the visible compose draft, then verify the sent message by unique subject. <br>
Risk: Sensitive files could be attached to email or exposed through a Drive-link fallback. <br>
Mitigation: Avoid sensitive files unless necessary, and treat Drive fallback sharing as a separate approval decision with restricted recipient access. <br>
Risk: Existing drafts or blocked Gmail attachment classes can cause incorrect or failed delivery. <br>
Mitigation: Close or save existing drafts before sending, preflight attachment size and file type constraints, and stop rather than retrying when Gmail blocks an attachment. <br>


## Reference(s): <br>
- [CDP Gmail Delivery](https://clawhub.ai/joustonhuang/cdp-gmail-delivery) <br>
- [Google Drive Fallback Delivery](references/drive-fallback.md) <br>
- [Receipts (Agent-Browser + Chrome Debug + CDP Gmail)](references/receipts.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit send status markers such as EMAIL_SENT_OK or limitation markers for blocked Gmail attachment cases.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
