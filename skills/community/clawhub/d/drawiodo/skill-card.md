## Description:

Drawiodo helps an agent turn natural-language diagram requests into draw.io files for flowcharts, architecture diagrams, UML, ER diagrams, sequence diagrams, mind maps, and related visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and technical teams use this skill to generate and iteratively refine draw.io diagrams from natural language or structured diagram specifications. It supports local preview and version rollback workflows for diagram files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review flags under-scoped automatic local actions, including file writes, local preview launch, and local version-folder maintenance.

Mitigation: Install only in trusted workspaces and review automatic preview, backup, restore, and pruning behavior before deployment.

Risk: The server security review flags concrete file-deletion and overwrite safety flaws.

Mitigation: Avoid using the skill on preexisting .drawio_versions data until version-path validation, hook abort enforcement, and explicit confirmation for preview, pruning, and restore are fixed.

## Reference(s):

- [ClawHub Publisher Profile: ldxs001](https://clawhub.ai/user/ldxs001)
- [License](artifact/references/LICENSE.md)
- [Generation Reference](artifact/references/generation.md)
- [API Reference](artifact/references/api_reference.md)
- [Hooks Reference](artifact/references/hooks.md)
- [Layout Rules](artifact/references/layout_rules.md)
- [Known Issues](artifact/references/known_issues.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; generated artifacts are .drawio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local draw.io diagram files and may open local preview applications or manage local version folders during normal use.]

## Skill Version(s):

2.6.1 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
