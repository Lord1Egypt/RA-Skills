## Description: <br>
Email API for AI agents. Send and receive emails programmatically via ClawMail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heyarviind](https://clawhub.ai/user/heyarviind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to give agents a dedicated ClawMail inbox, poll and read email threads, and send plain text or HTML messages through the ClawMail API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow downloads and runs an unpinned remote setup script. <br>
Mitigation: Review the setup script before execution, or ask the publisher for checksums or a packaged installer. <br>
Risk: The skill stores mailbox credentials in ~/.clawmail/config.json and can access mailbox content and outbound email. <br>
Mitigation: Protect the local config file, use a dedicated inbox, and install only when the ClawMail service is trusted. <br>
Risk: Inbound email content can influence agent behavior or cause unintended replies. <br>
Mitigation: Validate trusted senders before processing messages and confirm recipients and message content before sending. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/heyarviind/clawmail) <br>
- [ClawMail Website](https://clawmail.cc) <br>
- [ClawMail API Documentation](https://clawmail.cc/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with bash, JSON, curl, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to use ClawMail API endpoints and local configuration; the skill itself does not produce standalone executable software.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
