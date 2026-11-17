## Description:

Configure Caddy as a reverse proxy with automatic HTTPS and simple Caddyfile syntax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to get concise guidance for configuring Caddy reverse proxies, automatic HTTPS, Docker networking, certificate storage, validation, and reload workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HSTS guidance in the skill may be inaccurate or incomplete for deployments that require Strict-Transport-Security.

Mitigation: Configure and verify Strict-Transport-Security explicitly when HSTS is required.

Risk: Applying generated or adapted Caddy configuration without review can break routing, certificates, or reload behavior.

Mitigation: Run Caddy formatting and validation commands, inspect the adapted configuration, and review changes before reloading a live server.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Caddyfile and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Caddy CLI for validation, formatting, reload, and adaptation commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
