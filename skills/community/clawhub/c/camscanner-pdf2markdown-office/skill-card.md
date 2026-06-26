## Description: <br>
Use CamScanner to convert PDF documents to Markdown through its hosted upload, conversion, and download workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camscanner-ai](https://clawhub.ai/user/camscanner-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to convert PDF files into Markdown for editing, summarization, extraction, or downstream document processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF contents are uploaded to CamScanner's online service for conversion. <br>
Mitigation: Use only documents approved for that service and avoid confidential, regulated, or sensitive PDFs unless organizational data-handling terms permit it. <br>


## Reference(s): <br>
- [CamScanner homepage](https://www.camscanner.com) <br>
- [CamScanner PDF conversion API base URL](https://ai-tools.camscanner.com) <br>
- [ClawHub skill page](https://clawhub.ai/camscanner-ai/camscanner-pdf2markdown-office) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; uploads the selected PDF to CamScanner's hosted service and saves the converted Markdown to a local output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
