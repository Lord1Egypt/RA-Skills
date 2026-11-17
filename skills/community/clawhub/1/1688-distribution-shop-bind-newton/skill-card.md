## Description:

Guides users through the 1688 distribution buyer shop-binding flow in the Newton client, including platform selection, authorization login, and shop binding in an embedded Electron browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External Newton client users use this skill to bind 1688 distribution buyer shops to supported platform tools through guided command and browser authorization steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send signed API requests to a gateway selected by runtime environment configuration.

Mitigation: Lock DISTRIBUTE_BASE_URL to the official HTTPS 1688 gateway and restrict who can set runtime environment variables.

Risk: The authorization flow can open browser URLs during login and shop authorization.

Mitigation: Verify authorization page hostnames before entering credentials or approving authorization.

Risk: Tracking logs may be collected from stderr during execution.

Mitigation: Review logging expectations before deployment and avoid exposing sensitive values in command arguments or environment variables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-distribution-shop-bind-newton)
- [Command reference](artifact/references/commands.md)
- [Output schema](artifact/references/output_schema.md)
- [1688 gateway API reference](artifact/references/api_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON responses with user-facing Markdown and optional browser action fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return status through exit codes; tracking logs may be emitted as JSON on stderr.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
