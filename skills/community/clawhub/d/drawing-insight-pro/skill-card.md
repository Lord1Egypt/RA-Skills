## Description:

图纸解析(专业版) helps engineering teams and cost-consulting organizations batch-analyze construction drawings across PDF and DWG inputs, with OCR preprocessing, cross-drawing indexing, Chinese annotation classification, custom templates, and version-difference analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Engineering teams, cost consultants, design reviewers, construction teams, and supervisors use this skill to convert construction drawing sets into searchable indexes, reports, issue lists, and exportable project data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad file, command, and webhook capabilities may expose sensitive project drawings or run unintended actions.

Mitigation: Review before installation, keep drawing processing local by default, permit only trusted callback or webhook endpoints, and approve package installation or command execution explicitly.

Risk: OCR and drawing extraction can produce incomplete or incorrect results for construction documents.

Mitigation: Use outputs as review aids, validate extracted measurements, annotations, indexes, and issue lists against source drawings before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/drawing-insight-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with code and configuration examples, plus optional JSON, CSV, Excel, and webhook-oriented outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose package installation, local file reads and writes, batch exports, and optional trusted callback or webhook use.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
