## Description:

Deploy, manage, and monitor static websites via the EzyHost API, including file upload, AI site generation, analytics, custom domains, QR codes, email capture, and team collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[araratdev](https://clawhub.ai/user/araratdev)

### License/Terms of Use:


## Use Case:

Developers and site operators use this skill to manage EzyHost static website projects through API calls, including deployment, SEO checks, analytics review, domain setup, version rollback, team management, email capture, and API-key lifecycle actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an EzyHost API key and the security evidence says credential use is under-declared.

Mitigation: Treat EZYHOST_API_KEY as a secret, avoid logging or exposing it, and install only when the user trusts EzyHost with that key.

Risk: The skill can perform destructive or account-impacting actions, including deleting projects, rolling back versions, changing domains, managing teams, exporting emails, and revoking API keys.

Mitigation: Require explicit user confirmation before delete, rollback, domain, team, email export, or API-key actions.

Risk: The security verdict is suspicious because the skill exposes broad hosted-project and account management capabilities without clear confirmation guidance.

Mitigation: Review requested API operations before execution and scope use to the specific EzyHost project or account task the user approved.

## Reference(s):

- [ClawHub EzyHost skill page](https://clawhub.ai/araratdev/skills/ezyhost)
- [EzyHost homepage](https://ezyhost.io)
- [EzyHost API base URL](https://ezyhost.io/api)
- [EzyHost API key dashboard](https://ezyhost.io/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with API examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EZYHOST_API_KEY and network access to ezyhost.io.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
