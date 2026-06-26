## Description: <br>
Manages email by reading mailbox counts, message lists, and message contents through POP3 and sending messages through SMTP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hpw03210](https://clawhub.ai/user/hpw03210) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to query a configured mailbox, read selected messages, count messages, and send simple text or HTML email from the same account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes mail deletion behavior that can remove messages without a documented confirmation step. <br>
Mitigation: Review the skill before installing and remove, document, or gate deletion behind explicit confirmation before granting access to important mailboxes. <br>
Risk: The skill relies on mailbox credentials in config.yaml, which can expose email access if mishandled. <br>
Mitigation: Use a dedicated app password or test mailbox, restrict permissions on config.yaml, and avoid granting access to sensitive mailboxes until the configuration handling is reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hpw03210/email-manager-pop3) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text responses, command-line output, and YAML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local config.yaml with POP3 and SMTP server settings, account credentials or an app token, and SSL preferences.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
