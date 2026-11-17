## Description:

AhaPoint 生成专家按 AhaPoints Protocol v1.0 标准挖掘并生成独立的 aha point 报告，覆盖痛点、妙点和乐点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyuxing](https://clawhub.ai/user/lyuxing)

### License/Terms of Use:

CC-BY-4.0

## Use Case:

External users and developers use this Chinese-first skill to research a domain, identify pain, innovation, or fun points, and turn them into APS v1.0 AhaPoint reports with metadata, validation steps, and relationship graphs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may perform web searches while generating reports.

Mitigation: Review cited research and distinguish source-backed findings from generated synthesis before relying on a report.

Risk: The skill may create or update local AhaPoint files and registry files.

Mitigation: Confirm the output directory and require user approval before overwriting existing reports or updating registry files.

## Reference(s):

- [AhaPoint Generator on ClawHub](https://clawhub.ai/lyuxing/skills/aha-point-generator)
- [Publisher profile](https://clawhub.ai/user/lyuxing)
- [Skill README](artifact/README.md)
- [Runner workflow](artifact/runner.md)
- [Example output](artifact/example-output.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown reports with YAML metadata, Mermaid relationship graphs, and JSON registry updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first output; may use browser research and create or update local AhaPoint files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
