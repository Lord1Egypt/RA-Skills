## Description:

ArchMap is a terminal-native architecture mapping agent that analyzes a project, builds architecture baselines, supports incremental impact analysis, synchronizes changes, and produces line-level diff impact reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xu-jin-cs](https://clawhub.ai/user/xu-jin-cs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use ArchMap to generate architecture inventories, dependency maps, impact analysis, and diff-based test-selection inputs for software projects. It is suited to release, review, and maintenance workflows where teams need text-based architecture evidence without modifying source code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed expert-router guidance and saved internalizations can influence future analyses.

Mitigation: Review or disable the expert-router, gate-switch, internalizations.jsonl reuse, and global skill promotion workflow before deployment.

Risk: The skill writes generated reports and state files under the target project's archmap directory.

Mitigation: Run it only against intended projects or controlled copies, and review generated files before committing or using them as release evidence.

Risk: Dependency installation may pull broad version ranges.

Mitigation: Install in an isolated environment and pin dependency versions where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xu-jin-cs/skills/archmap)
- [Server-Resolved GitHub Source](https://github.com/xu-jin-cs/dsh-skills/tree/main/archmap)

## Skill Output:

**Output Type(s):** [Analysis, Files, Markdown, JSON, Configuration]

**Output Format:** [JSON, YAML, Markdown, and Mermaid text files with terminal summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes analysis state and reports under the target project's archmap directory; does not generate images.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
