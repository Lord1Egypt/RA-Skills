## Description:

Personal bookkeeping assistant for local income and expense tracking, monthly reports with comparisons, budget alerts, and savings goal management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to maintain local personal bookkeeping records, review income and expense reports, manage category budgets, and track savings goals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal financial records and command history on local disk without clear permission hardening.

Mitigation: Review storage paths before use, avoid entering secrets in command arguments, and restrict permissions on ~/.bookkeeping and the beancount data directory when storing real data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/skills/beancount)
- [Publisher profile](https://clawhub.ai/user/bytesagain-lab)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal-oriented text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill writes local JSON bookkeeping records, budget data, savings goals, and command history files.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
