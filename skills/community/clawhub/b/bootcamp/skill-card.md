## Description:

Auto-generates a CLI reference doc so your agent stops guessing OpenClaw commands and starts working. Discovers all commands, subcommands, and flags from your installed version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dank-varley](https://clawhub.ai/user/dank-varley)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent users run this skill to generate a local Markdown reference for the installed OpenClaw CLI, including commands, subcommands, flags, JSON support, and selected usage notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a persistent CLI reference file into the OpenClaw workspace notes directory, or to a custom output path when provided.

Mitigation: Review the target output path before running, use the interactive prompt to keep or overwrite existing references, and inspect the generated Markdown before relying on it.

Risk: Enrich mode fetches documentation from docs.openclaw.ai and appends fetched content to the generated reference.

Mitigation: Use local-only mode when network access is not desired, and use enrich mode only when documentation-derived additions are acceptable for the agent's workspace.

## Reference(s):

- [OpenClaw Boot Camp ClawHub page](https://clawhub.ai/dank-varley/skills/bootcamp)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration]

**Output Format:** [Markdown reference file with CLI commands, flags, subcommands, and usage notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes openclaw-cli-reference.md to the OpenClaw workspace notes directory by default; optional enrich mode can add documentation-derived flag details.]

## Skill Version(s):

1.2.1 (source: server-resolved release metadata and script header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
