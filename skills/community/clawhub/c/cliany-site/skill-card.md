## Description:

Use when the user wants to automate web workflows into CLI commands via Chrome CDP and LLM. Supports exploring pages, generating adapters, and replaying actions through the cliany-site tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pearjelly](https://clawhub.ai/user/pearjelly)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent users use this skill to turn browser workflows into repeatable CLI commands, including environment checks, website login sessions, workflow exploration, adapter generation, and command replay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive logged-in browser sessions and perform actions on websites.

Mitigation: Use it only on sites where automation is authorized, avoid sensitive accounts unless necessary, and require explicit confirmation before login, form submission, purchases, account changes, or replaying generated adapters.

Risk: Page accessibility structure from logged-in or private pages may be sent to the configured LLM provider.

Mitigation: Use an approved LLM provider and avoid pages containing sensitive information unless the provider and data handling are acceptable.

Risk: The release installs and replays generated web-automation code.

Mitigation: Prefer a pinned, reviewed release in an isolated environment and review generated adapters before replaying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pearjelly/skills/cliany-site)
- [ClawHub publisher profile](https://clawhub.ai/user/pearjelly)
- [Project homepage](https://github.com/pearjelly/cliany.site)
- [Project documentation](https://cliany.site)
- [Support issues](https://github.com/pearjelly/cliany.site/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples and JSON command envelopes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated adapters are described as Python/Click CLI code and metadata; commands can return a standard JSON envelope when --json is used.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
