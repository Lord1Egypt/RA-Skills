## Description:

Search and browse local Beeper chat history, including threads, messages, and full-text search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krausefx](https://clawhub.ai/user/krausefx)

### License/Terms of Use:


## Use Case:

People who use Beeper Desktop use this skill to let an agent search, browse, and summarize local chat history without sending messages. It is useful for finding threads, retrieving message context, and exporting structured results from local Beeper data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent access to sensitive local Beeper chat history.

Mitigation: Install it only when that access is intended, use narrow searches, limit result counts, and avoid unnecessary extraction of full conversations.

Risk: The documented go install flow can track the latest upstream beeper-cli code.

Mitigation: Pin or review the beeper-cli version before installing in managed or sensitive environments.

## Reference(s):

- [ClawHub Beeper skill](https://clawhub.ai/krausefx/skills/beeper)
- [beeper-cli](https://github.com/krausefx/beeper-cli)
- [Beeper](https://www.beeper.com/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with bash command examples; CLI examples request JSON output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Beeper Desktop data and the beeper-cli binary on PATH; supports local database path overrides.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
