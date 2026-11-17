## Description:

Helps connect an agent or user to Deutero by setting up accounts, authorizing MCP or SDK access, and checking plan and credit limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[francisjervis](https://clawhub.ai/user/francisjervis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Deutero users use this skill to create or connect an account, configure MCP or SDK access, and confirm authorization, plan features, and credits before starting research work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance suggests sending vendor feedback without user approval or clear limits on shared information.

Mitigation: Make feedback optional and have the user review the exact report; remove credentials, participant information, and confidential study details before sending it.

Risk: API keys grant organization-wide access, and external SDK code, remote service behavior, and plugin configuration were not verified.

Mitigation: Prefer OAuth where available, keep API keys in an owner-only secret store or environment variable, and verify client configuration and external SDK behavior before relying on them.

## Reference(s):

- [Deutero Setup on ClawHub](https://clawhub.ai/francisjervis/skills/deutero-setup)
- [Deutero API documentation](https://dashboard.deutero.ai/study-api/api/v1/docs)
- [Deutero Python SDK repository](https://github.com/deutero-ai/deutero-python)
- [Account signup guide](artifact/references/account-signup.md)
- [MCP and REST configuration guide](artifact/references/mcp-clients.md)
- [Plan limits guide](artifact/references/plan-limits.md)
- [Python SDK guide](artifact/references/python-sdk.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline JSON, shell command, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
