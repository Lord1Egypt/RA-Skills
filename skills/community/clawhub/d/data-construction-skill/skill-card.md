## Description: <br>
Builds concept, process, and case-application supervision datasets from markdown books or long markdown documents, with full chunk coverage, resumable batch processing, status tracking, validation, and coverage auditing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[technomad-ds](https://clawhub.ai/user/technomad-ds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data builders use this skill to turn markdown books or long markdown documents into structured supervision data for book-to-SFT workflows. It is suited to pipelines that need reusable knowledge extraction, grounded reasoning examples, case-application samples, and auditable chunk coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated manifests, chunks, and supervision files can include source text and absolute local paths. <br>
Mitigation: Use a narrow input folder and review generated manifest, chunk, and supervision files before sharing or publishing them. <br>
Risk: Input documents may contain secrets or material that should not be reused in training data. <br>
Mitigation: Exclude sensitive or unauthorized documents before processing and review outputs for retained sensitive content. <br>
Risk: Incomplete status tracking can make a dataset appear complete while chunks remain unprocessed or mismatched. <br>
Mitigation: Run the bundled validation and coverage checks and only treat the run as complete when unprocessed chunks and mismatch previews are empty. <br>


## Reference(s): <br>
- [Data Construction Skill page](https://clawhub.ai/technomad-ds/data-construction-skill) <br>
- [README](artifact/README.md) <br>
- [Quality rubric and supervision schema](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus JSONL supervision files and JSON validation reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces manifest, chunk, status, batch supervision, merged supervision, validation, and coverage files for local dataset-preparation workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
