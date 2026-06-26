## Description: <br>
Converts PDF and image documents to Markdown through CamScanner's document parsing service, preserving text, tables, and reading order for downstream agent use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camscanner-ai](https://clawhub.ai/user/camscanner-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and external users use this skill to turn user-provided PDFs or images into local Markdown files for review, extraction, or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents are uploaded to CamScanner's servers for processing, which can expose confidential, regulated, or highly sensitive content to a third-party service. <br>
Mitigation: Use only with documents suitable for CamScanner processing; avoid sensitive files unless the provider's handling and retention claims are approved, or use a local converter. <br>
Risk: Converted Markdown may be incomplete or inaccurate for complex layouts, tables, or image-heavy documents. <br>
Mitigation: Review the generated Markdown before relying on it for decisions, records, or downstream automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/camscanner-ai/camscanner-any2markdown-office) <br>
- [CamScanner homepage](https://www.camscanner.com) <br>
- [CamScanner conversion service](https://ai-tools.camscanner.com) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown file, with usage guidance expressed as shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; uploads selected source documents to CamScanner's ai-tools service for conversion.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
