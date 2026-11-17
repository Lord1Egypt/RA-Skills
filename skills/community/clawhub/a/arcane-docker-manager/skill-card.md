## Description:

Manage Docker containers, compose stacks, templates, images, networks, volumes, users, API keys, and system monitoring through the Arcane Docker Management API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cougz](https://clawhub.ai/user/cougz)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to administer an Arcane-managed Docker environment from an agent, including container lifecycle tasks, stack deployment, resource cleanup, API key management, and operational monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger destructive Docker and account-management actions such as deletes, prunes, container exec, user changes, and API-key changes.

Mitigation: Require explicit user confirmation before destructive or privileged operations, and scope credentials to the minimum permissions needed.

Risk: Arcane API tokens or API keys could be exposed or transported insecurely.

Mitigation: Use HTTPS for non-local APIs and store credentials in environment variables or a secret store rather than hardcoding them in prompts or files.

Risk: Broad Docker administration access can affect running services and persisted data.

Mitigation: Review proposed stack, container, network, image, and volume changes before execution, especially in production environments.

## Reference(s):

- [Personal Docker Manager on ClawHub](https://clawhub.ai/cougz/skills/arcane-docker-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl, Python, Bash, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides API endpoint patterns and operational examples; actions require Arcane API credentials and a configured base URL.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
