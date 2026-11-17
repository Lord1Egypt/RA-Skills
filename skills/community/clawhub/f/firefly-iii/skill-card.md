## Description:

Manage personal finances via Firefly III API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pushp1997](https://clawhub.ai/user/pushp1997)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query and manage Firefly III personal finance data, including accounts, transactions, categories, budgets, piggy banks, subscriptions, recurring transactions, rules, tags, and financial summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles and can change sensitive financial data.

Mitigation: Use it only with a Firefly III server you control, require clear confirmation before create or update operations, and review proposed API calls before execution.

Risk: Credential handling guidance is under-scoped for a personal access token.

Mitigation: Use HTTPS for FIREFLY_URL, prefer a secure secret store or tightly protected environment variable over ~/.firefly_token, and restrict and rotate the token where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pushp1997/skills/firefly-iii)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read or modify sensitive financial records through the configured Firefly III API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
