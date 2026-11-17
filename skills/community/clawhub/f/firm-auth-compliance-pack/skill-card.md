## Description:

Authentication and compliance audit pack for OAuth 2.1/OIDC Discovery, token scope enforcement, tool deprecation lifecycle, circuit breakers, GDPR residency, DID identity, model routing, and resource links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and compliance engineers use this skill to audit OpenClaw authentication, identity, routing, and residency configurations before release or deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The actual audit behavior appears to come from mcp-openclaw-extensions rather than bundled code in this Markdown-only skill.

Mitigation: Review mcp-openclaw-extensions before installation and confirm it provides the expected compliance tools.

Risk: Compliance outputs may be incomplete or incorrect for real authorization, residency, identity, or routing decisions.

Mitigation: Validate findings with qualified reviewers before relying on them for production compliance decisions.

Risk: The audit tools are expected to inspect user-provided compliance configuration files.

Mitigation: Use non-secret representative configs where possible and handle configuration data according to internal data-handling rules.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/romainsantoli-web/skills/firm-auth-compliance-pack)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or text audit guidance with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on mcp-openclaw-extensions >= 3.0.0; the skill itself bundles no executable code.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
