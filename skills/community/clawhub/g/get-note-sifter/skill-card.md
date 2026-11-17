## Description:

Analyzes Get notes and external links against a research map, then produces structured triage reports and Obsidian organization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duzhilei951](https://clawhub.ai/user/duzhilei951)

### License/Terms of Use:

MIT-0

## Use Case:

People managing Obsidian research vaults use this skill to evaluate Get notes or article links, match them to known research topics, detect likely overlap, and draft wiki-format notes when content should be saved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad read/write access to an Obsidian vault.

Mitigation: Restrict access to the intended vault folder and require a path plus content preview before any note or index file is created or changed.

Risk: The skill describes possible automatic weekly scanning.

Mitigation: Disable automatic scanning unless the user explicitly opts in.

Risk: The artifact recommends a global, unpinned vaultctl install.

Mitigation: Prefer a pinned local vaultctl installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duzhilei951/skills/get-note-sifter)
- [Research map](artifact/memory/research-map.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with optional Obsidian wiki-note drafts and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Obsidian vault reads or writes through vaultctl or filesystem access when the user grants access.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
