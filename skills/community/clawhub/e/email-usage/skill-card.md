## Description: <br>
Email Usage lets an agent send email, read recent inbox headers, and create mailbox accounts on a local domain mail server using bundled Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or mailserver operators can use this skill to let an agent send messages, inspect recent inbox headers, and create mailbox accounts on an authorized local domain mail server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent sensitive mailbox access and the ability to create email accounts. <br>
Mitigation: Require explicit operator approval for mailbox reads and account creation, and limit Docker and mailserver access to authorized operators. <br>
Risk: Passwords are passed on the command line, where they may be exposed through shell history or process listings. <br>
Mitigation: Use secure prompting or a secret store before operational use. <br>
Risk: The send script can fall back to unauthenticated SMTP after authentication failure. <br>
Mitigation: Remove the unauthenticated fallback or restrict it to a tightly controlled trusted network. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/email-usage) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/axelhu) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker access to the local mailserver container and valid mailbox credentials for authenticated operations.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
