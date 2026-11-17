## Description:

Query and manage personal finances through the official Actual Budget Node.js API for self-hosted Actual Budget instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thisisjeron](https://clawhub.ai/user/thisisjeron)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to help an agent query, import, export, categorize, and update data in self-hosted Actual Budget instances while keeping credentials in the runtime environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive Actual Budget credentials and financial data.

Mitigation: Use a dedicated private credentials file or environment wrapper with restrictive permissions, keep it out of repositories, and redact credentials and full transaction exports unless explicitly requested.

Risk: Mutating operations can change accounts, transactions, categories, rules, schedules, budget amounts, or bank sync state.

Mitigation: Confirm whether the task is mutating, summarize intended changes before applying them, sync only after intended writes, and shut down the API after use.

Risk: Budget data may be cached locally through ACTUAL_DATA_DIR or the default cache path.

Mitigation: Choose and protect the cache directory deliberately, and clean or restrict it according to the user's data-handling requirements.

## Reference(s):

- [ClawHub Actual Budget skill page](https://clawhub.ai/thisisjeron/skills/actual-budget)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should redact credentials, minimize sensitive financial data, and summarize mutating actions before execution.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
