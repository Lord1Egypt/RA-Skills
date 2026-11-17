## Description:

Searches and views a Calibre catalog or prepares and validates one-book analysis without changing library metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Calibre users and developers use this skill to look up book metadata and prepare a single book for offline analysis. It returns summaries and a local proposal for separately reviewed metadata changes, without editing the library itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported books and extracted text remain in local cache and state directories.

Mitigation: Keep these directories private and review retained files before sharing or deleting them.

Risk: An unintended library or server could expose the wrong books during analysis.

Mitigation: Specify the intended Calibre endpoint and library, and use a dedicated password environment variable when authentication is needed.

Risk: Short, image-heavy, or incompletely read books can produce unreliable summaries.

Mitigation: Stop on skipped or low-text results unless the user explicitly accepts incomplete extraction; disclose partial coverage.

Risk: A generated metadata proposal may contain inaccurate descriptions or tags.

Mitigation: Review proposals and route any actual update through a separate metadata apply workflow.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nextaltair/skills/calibre-catalog-read)
- [One-book analysis prompt](references/subagent-analysis.prompt.md)
- [Analysis input schema](references/subagent-input.schema.json)
- [Analysis output schema](references/subagent-analysis.schema.json)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Catalog metadata and analysis summaries in text; local JSONL metadata proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports full or partial text coverage; proposals require a separate review and apply workflow.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
