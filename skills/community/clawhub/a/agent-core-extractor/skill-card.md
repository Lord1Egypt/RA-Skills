## Description:

Exports agent-defining source files from supported framework repositories into a small source-only zip for AI migration or cross-framework analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moshiii](https://clawhub.ai/user/moshiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to detect supported agent framework repositories, extract the files that define agent behavior, and package them into portable source-only archives for migration or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The export may package sensitive agent configuration such as secrets, local paths, allowlists, or private policy files.

Mitigation: Review the generated archive, README.txt, MANIFEST.txt, and included configuration files before sharing or using the pack in another workflow.

Risk: Crafted path-like values in archive or repository inputs can cause writes outside the intended output area.

Mitigation: Use simple archive names and repository names, avoid path-like values in --name and --repos, and run the exporter on repositories and output directories you control.

## Reference(s):

- [Agent Core Design](references/AGENT_CORE.md)
- [Project homepage from metadata](https://github.com/moshiwei/AgentPearl)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Text, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated source-only zip archives containing README.txt and MANIFEST.txt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the zip command for archive creation; exported packs are intended for review before sharing.]

## Skill Version(s):

1.0.0 (source: server release and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
