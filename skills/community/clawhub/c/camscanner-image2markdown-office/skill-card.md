## Description: <br>
Use CamScanner to convert images such as PNG or JPG files into structured Markdown with OCR, table recognition, and reading-order extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camscanner-ai](https://clawhub.ai/user/camscanner-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to extract text, tables, code, and structured document content from images into Markdown before analysis or response generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may upload image files to CamScanner servers by default. <br>
Mitigation: Use only after the user understands and approves the upload, especially when images may contain private or regulated content. <br>
Risk: Sensitive personal, legal, medical, financial, proprietary, or regulated images may leave the local environment during OCR conversion. <br>
Mitigation: Avoid this skill for sensitive images unless explicit approval and applicable compliance review are in place; use a local OCR workflow when images must remain private. <br>


## Reference(s): <br>
- [CamScanner Homepage](https://www.camscanner.com) <br>
- [CamScanner Image2Markdown on ClawHub](https://clawhub.ai/camscanner-ai/camscanner-image2markdown-office) <br>
- [CamScanner AI Tools API](https://ai-tools.camscanner.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown file output with shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; image files are uploaded to CamScanner servers for conversion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
