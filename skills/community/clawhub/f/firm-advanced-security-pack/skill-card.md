## Description:

Advanced security audit pack covering secrets lifecycle, path canonicalization, exec plan freeze, hook routing, config includes, prototype pollution, safeBins profiles, and group policy defaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and security engineers use this skill to audit OpenClaw configuration files for high-impact security issues across secrets handling, path canonicalization, execution approvals, hooks, includes, prototype pollution, safeBins profiles, and group policy defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit conclusions depend on the external OpenClaw extension that supplies the listed tools.

Mitigation: Confirm the extension provider and version before relying on audit results.

Risk: Configuration audits may process sensitive configuration content if broad file paths are supplied.

Mitigation: Provide only the specific configuration files intended for audit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/skills/firm-advanced-security-pack)
- [ClawHub publisher profile](https://clawhub.ai/user/romainsantoli-web)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline YAML and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces audit guidance and tool invocation examples for OpenClaw configurations; requires mcp-openclaw-extensions >= 3.0.0.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
