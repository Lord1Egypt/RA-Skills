## Description: <br>
CamScanner-Image2Markdown helps agents convert image files into structured Markdown using CamScanner's OCR and document parsing service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camscanner-ai](https://clawhub.ai/user/camscanner-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users can use this skill when they need an agent to extract text, tables, code, or structured document content from screenshots or image files and return it as Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images may be uploaded to CamScanner servers when the skill is used for OCR or image-to-Markdown conversion. <br>
Mitigation: Use the skill only for explicit OCR or image-conversion requests, and avoid sensitive personal, legal, medical, financial, proprietary, or regulated images without clear user approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/camscanner-ai/skills/camscanner-image2markdown-office) <br>
- [CamScanner homepage](https://www.camscanner.com) <br>
- [CamScanner AI tools API](https://ai-tools.camscanner.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; converted image content is downloaded as a Markdown file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; image files are uploaded to CamScanner servers for processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
