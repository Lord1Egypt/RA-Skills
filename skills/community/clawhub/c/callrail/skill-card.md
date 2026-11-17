## Description:

Connects an agent to CallRail through Maton to review calls and analytics and manage tracking numbers, companies, and tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers can review CallRail call data and analytics, manage tracking numbers and tags, and set up approved CallRail automations through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Maton grants access to CallRail account data.

Mitigation: Connect only with user approval, review OAuth scopes, and remove unused connections.

Risk: Write operations or unattended automations can change records or continue acting after the initial task.

Mitigation: Confirm each write or automation separately and delete unused functions, triggers, and destinations.

Risk: Using a raw API key where the CLI is available increases credential exposure.

Mitigation: Prefer OAuth-backed CLI access; use the API-key fallback only when the CLI cannot be used.

## Reference(s):

- [CallRail skill release](https://clawhub.ai/byungkyu/skills/callrail)
- [Maton](https://maton.ai)
- [CallRail API documentation](https://apidocs.callrail.com/)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown guidance with CLI commands, API examples, and optional automation code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-first workflow; user approval required for connections, writes, and automations.]

## Skill Version(s):

1.2.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
