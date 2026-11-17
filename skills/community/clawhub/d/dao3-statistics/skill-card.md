## Description:

Dao3 Statistics helps agents query DAO3 (Shendao) user, map, comment, search, message, and statistics data through a Python CLI that returns JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ifishcool](https://clawhub.ai/user/ifishcool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch DAO3 platform profile, map, comment, relationship, search, message, and statistics data. It supports public lookups and authenticated account-scoped queries when the user intentionally provides a DAO3 token and user-agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated DAO3 commands accept account tokens on the command line.

Mitigation: Use short-lived or scoped credentials when possible, avoid pasting long-lived tokens into chat or shell history, and rotate any token that may have been exposed.

Risk: The raw endpoint mode can access broader authenticated DAO3 API paths than the curated commands.

Mitigation: Use curated commands for normal queries and reserve raw endpoint calls for intentional, reviewed API access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ifishcool/skills/dao3-statistics)
- [DAO3 API endpoint](https://code-api-pc.dao3.fun)

## Skill Output:

**Output Type(s):** [shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command outputs are JSON objects; failures include error details such as endpoint, status code, message, and response when available.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
