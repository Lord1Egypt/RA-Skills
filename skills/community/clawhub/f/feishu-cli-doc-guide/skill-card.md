## Description:

Provides a Chinese-language compatibility guide for preparing Feishu Markdown documents, covering Mermaid and PlantUML constraints, table splitting, callouts, formulas, images, API limits, and fallback behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giswilson](https://clawhub.ai/user/giswilson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent authors use this read-only reference before generating Markdown for Feishu document import so diagrams, tables, callouts, formulas, and images follow Feishu-compatible patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown prepared without applying the compatibility checklist can still fail Feishu import, especially for complex diagrams or oversized tables.

Mitigation: Review generated Markdown against the packaged Feishu compatibility rules and test representative imports for diagram-heavy or table-heavy documents.

Risk: The skill is mainly Chinese-language Feishu compatibility guidance and may be misapplied outside Feishu document workflows.

Mitigation: Use it only when preparing Markdown for Feishu document creation or import, and confirm the target workflow before applying its constraints.

Risk: The optional local ~/.claude/rules style-guide reference may not exist in every installer environment.

Mitigation: Rely on the packaged guidance in the skill artifact unless the local style-guide file is intentionally maintained.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/giswilson/skills/feishu-cli-doc-guide)
- [Mermaid Feishu board syntax guide](artifact/references/mermaid-spec.md)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown guidance and compatibility checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only reference content; no code execution, persistence, or credential handling identified in security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
