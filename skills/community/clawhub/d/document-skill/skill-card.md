## Description: <br>
Enables an agent to read, parse, extract, summarize, translate, and combine information from PDF, DOCX, PPT, WPS, and related document formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MskrQ](https://clawhub.ai/user/MskrQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill when they want an agent to analyze documents, extract key content, summarize reports, combine content across files, or transform document content into useful text outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broad document-analysis trigger may cause the skill to be selected for general document-analysis requests. <br>
Mitigation: Confirm the user actually wants document parsing, extraction, or summarization before applying the skill. <br>
Risk: Private, encrypted, or business-sensitive documents supplied to the agent are treated as intentional input data. <br>
Mitigation: Use the skill only with documents the user is authorized to provide, and redact sensitive content that is not needed for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MskrQ/document-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text summaries, extracted content, tables, translations, checks, and document-analysis guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; it does not define executable commands or hidden data flows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
