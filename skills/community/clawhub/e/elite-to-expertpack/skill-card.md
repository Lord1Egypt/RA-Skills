## Description:

Converts Elite Longterm Memory data into a structured, Obsidian-compatible ExpertPack with YAML-frontmatter content files, a manifest, overview, indexes, and relationship metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianhearn](https://clawhub.ai/user/brianhearn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to migrate or back up Elite Longterm Memory workspaces into portable ExpertPack directories for review, retrieval, and publication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ExpertPacks can contain sensitive local memory, and the automatic secret removal is incomplete.

Mitigation: Treat generated packs as private, manually review all output, and run a dedicated secret scanner before sharing or publishing.

Risk: Conversion completeness can be overstated because LanceDB and cloud memory sources are skipped or require separate export.

Mitigation: Confirm skipped sources separately and document any missing LanceDB, SuperMemory, or Mem0 content before relying on the converted pack.

## Reference(s):

- [ExpertPack homepage](https://expertpack.ai)
- [ExpertPack skill on ClawHub](https://clawhub.com/skills/expertpack)

## Skill Output:

**Output Type(s):** [markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown and YAML files with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates an ExpertPack directory; requires python3 and PyYAML.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
