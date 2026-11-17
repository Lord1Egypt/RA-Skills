## Description:

Runtime environment and configuration audit pack that validates Node.js version, secrets workflow, HTTP headers, allowed commands, trusted proxy, disk budget, and DM allowlist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to audit OpenClaw runtime configuration for Node.js compatibility, secrets handling, HTTP security headers, command allowlists, proxy settings, disk budget limits, and direct message allowlist policy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required OpenClaw extension provider and reviewed configuration files may involve security-sensitive deployment settings.

Mitigation: Install only a trusted mcp-openclaw-extensions provider and run the audit tools only against configuration files intended for review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/skills/firm-runtime-audit-pack)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces runtime audit guidance for configuration files supplied by the user.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
