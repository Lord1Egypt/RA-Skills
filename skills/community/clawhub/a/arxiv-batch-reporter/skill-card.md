## Description: <br>
Builds a final arXiv collection report by having the model draft a report template and then injecting each paper's Brief Conclusion and arXiv abstract URL from per-paper summary files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xukp20](https://clawhub.ai/user/xukp20) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers and developers use this skill after per-paper arXiv summaries exist to assemble a collection-level Markdown report with a hierarchy, brief per-paper conclusions, and arXiv abstract links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted paper summaries may contain prompt-injection or misleading content that influences the model-written collection report. <br>
Mitigation: Review generated summaries_bundle.md and the final collection report before relying on them, especially when papers, metadata, or summaries came from untrusted sources. <br>
Risk: Custom paths can cause the report workflow to read or write files outside the intended run directory. <br>
Mitigation: Keep custom base, template, and output paths inside the intended report directory. <br>


## Reference(s): <br>
- [Arxiv Batch Reporter on ClawHub](https://clawhub.ai/xukp20/arxiv-batch-reporter) <br>
- [Collection Report Template Format](references/report-format.md) <br>
- [Lean 4 Report Example](references/report-example-lean4-en.md) <br>
- [LLM Math Report Example](references/report-example-llm-math-en.md) <br>
- [Multimodal Report Example](references/report-example-multimodal-en.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown files with command-line workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes summaries_bundle.md, collection_report_template.md, and collection_report.md under the selected base directory.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
