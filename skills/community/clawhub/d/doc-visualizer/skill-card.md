## Description:

文档可视化 converts Feishu documents, Word, PDF, Excel, text, and CSV inputs into dark command-center-style HTML dashboards with five themes and optional PDF and full-page PNG exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzm2023](https://clawhub.ai/user/lzm2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow users use this skill to turn business documents, tables, reports, or Feishu content into shareable visual dashboards and exported PDF or long-image deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted document content may be rendered as active HTML in Playwright.

Mitigation: Process only documents you control or trust, run in an isolated environment with no sensitive network access, and escape document content before HTML generation.

Risk: The skill has unclear automatic activation boundaries.

Mitigation: Narrow trigger rules so the skill runs only on explicit document-visualization requests.

Risk: Browser export and document parsing dependencies increase operational exposure.

Mitigation: Pin dependencies, review parser behavior, and disable JavaScript or block outbound browser requests before broad enterprise use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lzm2023/skills/doc-visualizer)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [HTML dashboard files with optional PDF and full-page PNG exports; Markdown or shell snippets when guiding use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports five named themes and returns html, pdf, png, and output_dir paths when run as a Python module.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
