## Description:

Generates batch arXiv collection reports by combining a model-authored template with brief conclusions and abs URLs extracted from per-paper summary.md files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukp20](https://clawhub.ai/user/xukp20)

### License/Terms of Use:


## Use Case:

Developers and research analysts use this skill after per-paper arXiv summaries exist to assemble a final collection report with consistent paper entries and direct summary-derived conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Report input, template, or output paths can escape the intended run directory if arguments are misused or influenced.

Mitigation: Use only trusted local arXiv workflow inputs, avoid untrusted template or file path values, and run in a workspace where accidental reads or overwrites outside the run directory would not expose secrets or damage important files.

## Reference(s):

- [Collection Report Template Format](references/report-format.md)
- [ArXiv Collection Report Template Example, Lean 4](references/report-example-lean4-en.md)
- [ArXiv Collection Report Template Example, LLM for Math](references/report-example-llm-math-en.md)
- [ArXiv Collection Report Template Example, Multimodal LLM Research](references/report-example-multimodal-en.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown files with inline shell commands and arXiv placeholder syntax]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces summaries_bundle.md, a model-authored collection_report_template.md, and a rendered collection_report.md under the selected base directory.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
