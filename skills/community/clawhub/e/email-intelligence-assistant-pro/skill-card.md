## Description: <br>
Connects to IMAP mailboxes to classify emails by urgency, suggest multilingual replies, and push real-time summaries to Feishu chats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffersplind92](https://clawhub.ai/user/jeffersplind92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer support and operations teams use this skill to monitor IMAP mailboxes, triage incoming email, draft reply suggestions, and route urgent summaries to Feishu. It is suited for mailbox workflows where users can supply dedicated credentials and review suggested replies before taking action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive mailbox credentials and email contents. <br>
Mitigation: Use a dedicated app password, store configuration outside public repositories, and avoid regulated or highly confidential mailboxes unless redaction and consent controls are added. <br>
Risk: Email content may be transferred to configured AI API and Feishu services. <br>
Mitigation: Use a revocable AI API key, restrict the Feishu webhook or app token, and document external data transfers before production use. <br>
Risk: The security review flags unsafe or unclear side-effect controls and says not to rely on dry-run for a no-side-effect test. <br>
Mitigation: Validate behavior in an isolated mailbox and Feishu destination before connecting production accounts. <br>
Risk: The security review flags under-disclosed third-party credential validation and yk-global token validation behavior. <br>
Mitigation: Review and either remove, document, or explicitly accept that validation behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jeffersplind92/email-intelligence-assistant-pro) <br>
- [Publisher profile](https://clawhub.ai/user/jeffersplind92) <br>
- [YK-Global](https://yk-global.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell-command and YAML examples; runtime behavior produces email classifications, summaries, reply suggestions, and Feishu notification content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMAP credentials, an AI API key, and Feishu webhook or user-push credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
