## Description:

Manage Dokploy deployments, projects, applications, and domains via the Dokploy API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laoshu133](https://clawhub.ai/user/laoshu133)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to manage Dokploy projects, applications, deployments, domains, and application environment variables from an agent-assisted CLI workflow. It is intended for Dokploy instances where the user can provide an API URL and API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Dokploy API key with access to read and modify deployment resources.

Mitigation: Use the narrowest available API key permissions and review state-changing commands before execution.

Risk: Configuration and environment-variable commands can expose deployment secrets in local files, logs, or agent transcripts.

Mitigation: Prefer ephemeral environment variables, avoid using dokploy-config set or show with real keys until file handling is reviewed, and treat dokploy-app env list output as secret material.

Risk: Server security evidence marks the release suspicious because deployment credentials and environment secrets are handled unsafely.

Mitigation: Install only after reviewing the source and accepting the credential exposure risk for the target Dokploy instance.

## Reference(s):

- [Dokploy Skill on ClawHub](https://clawhub.ai/laoshu133/skills/dokploy-v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON-oriented command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq, plus DOKPLOY_API_URL and DOKPLOY_API_KEY for live Dokploy API calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
