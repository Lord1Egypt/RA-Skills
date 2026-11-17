## Description:

Use the fizzy-cli tool to authenticate and manage Fizzy kanban boards, cards, comments, tags, columns, users, and notifications from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobiasbischoff](https://clawhub.ai/user/tobiasbischoff)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill to let an agent operate Fizzy kanban workflows from the command line, including authentication, board and card management, comments, tags, columns, users, and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication tokens, magic-link codes, or local Fizzy configuration could be exposed through shared terminals, logs, command history, or unprotected config files.

Mitigation: Use short-lived or scoped tokens when possible, avoid printing credentials in shared contexts, and protect the local Fizzy config file.

Risk: Board, card, comment, tag, column, user, and notification commands can change or delete live Fizzy data.

Mitigation: Review target account, board, and card identifiers before running destructive or mutating commands.

## Reference(s):

- [Fizzy application](https://app.fizzy.do)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that authenticate to Fizzy or mutate live Fizzy board data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
