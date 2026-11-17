## Description:

Character Manager helps agents create, edit, query, validate, and export novel character profiles with relationship networks, emotional arcs, and motivation tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writing agents use this skill during novel-planning workflows to create structured YAML character profiles, manage character relationships, track character growth, and export profiles for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local CLI can recursively read YAML files from any directory supplied with --project.

Mitigation: Run it only against a dedicated novel workspace and avoid system or sensitive directories.

Risk: The CLI can overwrite or delete files at paths supplied with --output, especially when --force is used.

Mitigation: Review target paths before execution, avoid --force unless the file is confirmed, and keep backups for character files.

Risk: Dependencies are installed from requirements.txt and are not pinned to exact versions.

Mitigation: Prefer a virtual environment and review dependency versions before installation.

## Reference(s):

- [Character Manager on ClawHub](https://clawhub.ai/yuzhihui886/skills/character-manager)
- [Character Design Guide](references/character_design.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files, Markdown]

**Output Format:** [Markdown guidance with inline shell commands, YAML character profiles, and optional Markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses YAML character files and local filesystem paths supplied by the agent or user.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
