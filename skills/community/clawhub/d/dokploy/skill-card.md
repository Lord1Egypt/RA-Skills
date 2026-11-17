## Description:

Manage Dokploy deployments, projects, applications, and domains via the Dokploy API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joshuarileydev](https://clawhub.ai/user/joshuarileydev)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to manage Dokploy projects, applications, deployments, domains, and application environment variables from an agent-assisted command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Dokploy API keys and application secrets, and the security summary says users should review it before installing.

Mitigation: Review or patch the shell scripts before use, prefer environment variables or a secret store, and rotate any API key that may have been printed or stored in a readable configuration file.

Risk: Configuration and environment commands can expose sensitive API keys or application secrets in files, terminal output, logs, or transcripts.

Mitigation: Avoid running config show or environment variable listing commands in shared logs or transcripts, and restrict access to any local configuration file containing credentials.

Risk: The command scripts can create, update, delete, and deploy Dokploy resources against the configured server.

Mitigation: Use least-privilege Dokploy API keys, confirm the target DOKPLOY_API_URL before mutating commands, and review destructive operations before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command guidance with CLI output from Dokploy API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, DOKPLOY_API_URL, and DOKPLOY_API_KEY.]

## Skill Version(s):

1.0.0 (source: package metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
