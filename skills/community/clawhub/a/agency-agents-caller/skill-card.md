## Description:

Provides on-demand access to 179 professional agent prompts from a local SQLite-backed catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[717986230](https://clawhub.ai/user/717986230)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search, browse, randomly select, and retrieve full prompts from a bundled catalog of professional agent personas for coding, business, creative, academic, and support workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes guidance that asks users to share ClawHub tokens or other secrets in an assistant conversation.

Mitigation: Do not paste tokens or secrets into chat; create and manage tokens directly in ClawHub settings or other trusted credential-management surfaces.

Risk: The skill stores broad third-party prompt content that can be retrieved as full_content and reused as system prompts.

Mitigation: Review retrieved prompts before use, especially prompts involving payments, identity, email, infrastructure, or generated code execution.

Risk: Setup writes a local SQLite database during initialization.

Mitigation: Install only in an environment where creating and updating a local prompt catalog database is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/717986230/skills/agency-agents-caller)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, Python data structures, and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieves catalog records and full prompt text from a local SQLite database initialized from bundled JSON data.]

## Skill Version(s):

1.0.3 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
