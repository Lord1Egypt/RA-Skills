## Description: <br>
Doc Scan is a deprecated document scanning skill, merged into doc-process v4.0.0+, that converts document photos into perspective-corrected scanned images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piyush-zinc](https://clawhub.ai/user/piyush-zinc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-workflow users use this deprecated skill to evaluate and run a local scanner that turns document photos into clean scanned PNG or PDF outputs. The skill points users to doc-process for current document scanning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read document photos, write scan outputs, run local Python code, and record filenames and processing summaries to a local timeline. <br>
Mitigation: Review the skill before installing, scan only documents whose filenames and metadata are acceptable to store locally, and prefer the newer doc-process skill when it is trusted for the workflow. <br>


## Reference(s): <br>
- [Doc Scan ClawHub page](https://clawhub.ai/piyush-zinc/doc-scan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON scanner status; generated scan files may be PNG or PDF.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deprecated; recommends doc-process for newer document scanning workflows.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
