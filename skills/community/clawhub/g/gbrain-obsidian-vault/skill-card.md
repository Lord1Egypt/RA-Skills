## Description:

Helps agents connect an OpenClaw memory directory and gbrain wiki to an Obsidian vault so users can inspect local notes, backlinks, and graph relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spikesubingrui-design](https://clawhub.ai/user/spikesubingrui-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to wire an existing gbrain markdown wiki and OpenClaw memory notes into Obsidian for local graph browsing, backlink review, and manual note edits that continue through the existing sync workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script modifies the selected wiki vault, creates a `memory` symlink, appends `.gitignore` entries, and writes Obsidian configuration files.

Mitigation: Back up the vault's `.obsidian` directory, confirm `WIKI_DIR` and `MEMORY_DIR`, and inspect any existing `memory` path before running setup.

Risk: Symlinking OpenClaw memory notes into the vault can expose private daily notes in Obsidian and adjacent local tooling.

Mitigation: Install only when local memory visibility is acceptable, keep `memory` in `.gitignore`, and verify `git status` does not include memory note files.

Risk: The artifact recommends `git add -A` after `gbrain export`, which can stage unrelated local changes.

Mitigation: Inspect `git status` after export and stage only intended generated markdown or configuration paths.

## Reference(s):

- [Architecture](references/architecture.md)
- [Example vault layout](examples/vault-layout.md)
- [Gbrain Obsidian Vault on ClawHub](https://clawhub.ai/spikesubingrui-design/skills/gbrain-obsidian-vault)
- [Obsidian](https://obsidian.md)
- [OpenClaw](https://openclaw.ai)
- [gbrain](https://github.com/spikesubingrui-design/gbrain)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local filesystem changes to a user-selected wiki vault and Obsidian configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
