## Description:

Browser automation security audit pack that validates Playwright and Puppeteer headless configuration for dangerous arguments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and security engineers use this skill to audit Playwright and Puppeteer browser automation configurations for dangerous Chrome or Chromium arguments before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external OpenClaw extension package and audits configuration files supplied by the user.

Mitigation: Review the mcp-openclaw-extensions dependency in the target environment and only provide configuration files intended for audit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/skills/firm-browser-audit-pack)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with audit findings and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audits a supplied browser configuration path using the OpenClaw browser context check tool.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
