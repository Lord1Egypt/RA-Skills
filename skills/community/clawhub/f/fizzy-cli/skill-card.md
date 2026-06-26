## Description: <br>
Use the fizzy-cli tool to authenticate and manage Fizzy kanban boards, cards, comments, tags, columns, users, and notifications from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobiasbischoff](https://clawhub.ai/user/tobiasbischoff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agents use this skill to work with Fizzy kanban boards from the command line. It supports authentication, default account configuration, and common board, card, comment, tag, column, user, and notification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to modify or delete Fizzy boards and cards. <br>
Mitigation: Require explicit confirmation before delete commands or other important update commands. <br>
Risk: The skill depends on local fizzy-cli authentication and account access. <br>
Mitigation: Verify that the installed fizzy-cli executable is trusted and use a least-privileged Fizzy token or account where possible. <br>


## Reference(s): <br>
- [Fizzy application](https://app.fizzy.do) <br>
- [ClawHub skill page](https://clawhub.ai/tobiasbischoff/fizzy-cli) <br>
- [Publisher profile](https://clawhub.ai/user/tobiasbischoff) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command-output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include human-readable tables, raw JSON, or stable plain-text output when the agent invokes fizzy-cli with the corresponding output flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
