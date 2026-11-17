## Description:

anygen CLI: Shared patterns for authentication, global flags, and output formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supertilico2001](https://clawhub.ai/user/supertilico2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as a reference for authenticating the anygen CLI, applying common global flags, formatting output, and discovering command schemas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill involves anygen authentication and use of ANYGEN_API_KEY, so credentials could be exposed if copied into user-facing output.

Mitigation: Treat API keys and sessions as sensitive and do not print auth tokens or API keys.

Risk: Using anygen may involve file access, uploads, or task creation.

Mitigation: Require explicit user confirmation before reading or uploading files or creating tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supertilico2001/skills/anygen-shared)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes guidance to protect API keys and require user confirmation before file access, uploads, or task creation.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
