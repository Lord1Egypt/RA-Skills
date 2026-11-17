## Description:

Memory infrastructure audit pack for pgvector configuration validation and knowledge graph integrity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and infrastructure engineers use this skill to audit memory infrastructure by checking pgvector configuration and knowledge graph integrity before relying on memory-backed agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required OpenClaw extension package or target configuration path could be untrusted or unintended.

Mitigation: Confirm the extension package is trusted and run audit commands only against intended configuration files.

Risk: Audit findings may be incomplete or misleading if accepted without human review.

Mitigation: Have a qualified reviewer validate audit results before using them to change memory infrastructure.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown with tool-call style commands and audit findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcp-openclaw-extensions >= 3.0.0.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
