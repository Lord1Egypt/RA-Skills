## Description:

Manage Coolify deployments, applications, databases, and services via the Coolify API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[visiongeist](https://clawhub.ai/user/visiongeist)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to manage Coolify-hosted applications, databases, services, deployments, servers, projects, teams, SSH keys, GitHub Apps, and environment variables through the Coolify API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform destructive production actions such as deletes, stops, restarts, deployment cancellation, and environment-variable changes.

Mitigation: Use narrowly scoped Coolify tokens and require manual confirmation before delete, stop, restart, cancellation, or environment-variable mutation commands are executed.

Risk: The skill can handle sensitive values such as API tokens, environment variables, SSH private keys, and GitHub App private keys.

Mitigation: Avoid placing private keys or passwords directly in command arguments; prefer secure environment or configuration storage and review command logs for accidental secret exposure.

Risk: A misconfigured API URL could send authorization tokens or management requests to an untrusted endpoint.

Mitigation: Set COOLIFY_API_URL only to a trusted HTTPS Coolify Cloud or self-hosted Coolify endpoint.

## Reference(s):

- [Coolify Homepage](https://coolify.io)
- [Coolify Documentation](https://coolify.io/docs/)
- [Coolify GitHub Repository](https://github.com/coollabsio/coolify)
- [ClawHub Coolify Skill](https://clawhub.ai/visiongeist/skills/coolify)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with bash commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires COOLIFY_TOKEN and a trusted Coolify API endpoint.]

## Skill Version(s):

2.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
