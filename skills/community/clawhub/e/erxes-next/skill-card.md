## Description:

Manage contacts, companies, products, tags, documents, brands, automations, team members, and organization data on an erxes instance through GraphQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlkr123](https://clawhub.ai/user/wlkr123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to authenticate to an erxes workspace and perform GraphQL-backed CRM and organization administration tasks, including listing, creating, updating, merging, and removing business records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The login flow prints session JSON containing bearer and refresh tokens.

Mitigation: Treat the session payload as a secret, keep it only in memory for the current task, and do not write it to project files, prompts, logs, or examples.

Risk: The skill can perform live mutations that delete, merge, invite, deactivate, automate, or change organization structure.

Mitigation: Require explicit user confirmation and show the target records and intended mutation before executing destructive or administrative changes.

Risk: Untrusted or non-HTTPS gateway URLs can expose credentials or direct API calls to the wrong erxes instance.

Mitigation: Use only trusted HTTPS erxes gateway URLs for real work and avoid remote http:// endpoints.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wlkr123/skills/erxes-next)
- [erxes Quick Login](artifact/erxes-app-token-auth.md)
- [erxes GraphQL API reference](artifact/erxes-graphql-api.md)
- [Browser login helper](artifact/scripts/login.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, GraphQL examples, JSON payloads, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce authenticated GraphQL request examples and task-specific execution guidance for a live erxes workspace.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
