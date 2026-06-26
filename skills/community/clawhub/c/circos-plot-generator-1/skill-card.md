## Description: <br>
This release is listed as Circos Plot Generator, but the packaged artifact provides a blind-review manuscript anonymizer for double-blind submissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and academic writing users use the packaged skill to anonymize manuscripts before double-blind review. Users looking for Circos plotting should not rely on this release until the listing mismatch is resolved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The registry name advertises a Circos plot generator, but the package behaves as a blind-review manuscript anonymizer. <br>
Mitigation: Install only for manuscript anonymization, verify the skill purpose before use, and do not use it for Circos plotting until the listing is corrected. <br>
Risk: Manuscript anonymization can miss metadata, figures, supplemental files, or identifiers outside simple text patterns. <br>
Mitigation: Run on copies, review generated files manually, and check document metadata, figures, and supplemental materials before submission. <br>
Risk: The tool reads and writes local manuscript files and can overwrite a chosen output path. <br>
Mitigation: Confirm input and output paths before execution and keep original manuscripts unchanged. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub release page](https://clawhub.ai/aipoch-ai/circos-plot-generator-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance, command output, and local .docx, .md, or .txt manuscript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [DOCX processing requires python-docx; generated manuscript outputs require manual anonymity review before submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
