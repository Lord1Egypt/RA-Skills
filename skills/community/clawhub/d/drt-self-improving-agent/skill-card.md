## Description:

Self-improving DRT/ICT trading agent that journals trades, analyzes win/loss patterns, and maintains a local trading memory without network calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and trading workflow builders use this skill to journal DRT/ICT trades locally, review historical setup performance, and receive simple rule reminders based on the recorded trade history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trade history is stored locally in the skill's data/trades.json file.

Mitigation: Install only if local storage of the trade journal is acceptable, and manage that file according to the user's privacy and retention requirements.

Risk: Analysis output could be mistaken for financial advice or an autonomous trading decision system.

Mitigation: Treat the output as simple historical statistics and user review support, not as financial advice or automated trading authority.

Risk: Trading-window guidance is expressed in CET/Danish time.

Mitigation: Convert the killzone reminders to the user's trading timezone before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/northcap-group/skills/drt-self-improving-agent)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local JSON trade history in data/trades.json; analysis is historical statistics, not financial advice.]

## Skill Version(s):

1.0.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
