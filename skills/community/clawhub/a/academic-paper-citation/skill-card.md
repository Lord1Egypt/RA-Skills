## Description: <br>
Automates citation handling for Chinese academic papers by converting DOCX and Markdown, extracting references, inserting citation markers, expanding manuscript content, and generating final Word documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codhealer](https://clawhub.ai/user/codhealer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Academic writers, developers, and agents use this skill to process Chinese thesis-style manuscripts, manage references, insert citation markers, convert between DOCX and Markdown, and run final document checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill modifies academic drafts and creates persistent outputs, including possible overwrites of thesis files. <br>
Mitigation: Run it only on backed-up working copies and review all generated files before replacing an original manuscript. <br>
Risk: Hard-coded local paths may direct processing to an unintended workspace. <br>
Mitigation: Inspect and update hard-coded /Users/openclaw2026/.qclaw/workspace paths before execution. <br>
Risk: Expanded or injected content can create authorship, institutional-header, or academic-integrity concerns. <br>
Mitigation: Review generated and expanded text manually and confirm it meets the applicable academic and institutional requirements. <br>
Risk: Running generated JavaScript from document text can be unsafe for confidential or untrusted manuscripts. <br>
Mitigation: Avoid confidential manuscripts and inspect generated scripts and document-derived content before execution. <br>


## Reference(s): <br>
- [Implementation Details](references/implementation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Word documents, Shell commands, Guidance] <br>
**Output Format:** [Markdown, JSON, DOCX, and command-line instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent local document artifacts and intermediate reference or report files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
