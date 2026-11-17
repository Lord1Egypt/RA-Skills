## Description:

Performs dual-mode deep reading of academic papers from PDF attachments or URLs, producing both an in-depth academic analysis and a concise logic-focused distillation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sterlingfrank1](https://clawhub.ai/user/sterlingfrank1)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, analysts, and other external users use this skill to turn scholarly PDFs or paper URLs into a structured reading report with a rigorous Part A analysis and a concise Part B summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL-based papers may need to be fetched externally, and submitted papers or URLs may be processed in the runtime environment.

Mitigation: Provide only papers or URLs the user is comfortable having processed.

Risk: The skill creates temporary analysis content and a final Markdown report in the workspace.

Mitigation: Review generated reports before sharing and keep workspace files aligned with the user's document-handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sterlingfrank1/skills/academic-paper-parse-en)
- [Part A template](artifact/references/part-a-template.md)
- [Part B template](artifact/references/part-b-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report file plus a brief message summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a dual-mode reading report with Part A in-depth academic analysis and Part B core logic distillation.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
