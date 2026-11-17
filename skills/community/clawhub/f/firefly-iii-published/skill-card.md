## Description:

Firefly III API Client helps agents access and manage Firefly III finance data through a token-authenticated REST API wrapper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josetseph](https://clawhub.ai/user/josetseph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent query and update a Firefly III instance for accounts, transactions, recurring rules, rules, and related automation. It is suited to workflows where the user intentionally grants an agent API access to personal finance data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad Firefly III financial mutation and administration authority to an agent.

Mitigation: Use the least-privileged token available and require explicit human confirmation before exports, bulk edits, deletes, cron, webhook, or user-administration calls.

Risk: Bearer tokens can be sent over HTTP if FIREFLY_URL is configured with an insecure URL.

Mitigation: Configure FIREFLY_URL with HTTPS and avoid the documented HTTP example except in isolated local development.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josetseph/skills/firefly-iii-published)
- [Firefly III API documentation](https://docs.firefly-iii.org/references/firefly-iii/api/)
- [Firefly III project site](https://firefly-iii.org)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request or response bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FIREFLY_URL and FIREFLY_TOKEN environment variables; API results depend on the connected Firefly III instance and token permissions.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
