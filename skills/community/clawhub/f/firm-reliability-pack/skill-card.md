## Description:

Reliability probing and documentation sync pack for gateway health checks, documentation sync validation, channel audits, and ADR generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to probe gateway reliability, validate documentation-code alignment, audit channel configuration, and generate Architecture Decision Records in MADR format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the external mcp-openclaw-extensions package and user-provided configuration files.

Mitigation: Install it only when the dependency is trusted and the referenced configuration files are appropriate to share with its tools.

Risk: Generated ADRs, audit outputs, or reliability findings may be incomplete or misleading if used without review.

Mitigation: Review generated ADRs and audit results before using them for operational or architectural decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline tool invocation examples and generated ADR or audit text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcp-openclaw-extensions >= 3.0.0 and user-provided configuration files.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
