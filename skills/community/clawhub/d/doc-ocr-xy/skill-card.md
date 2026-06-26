## Description: <br>
Scans PDF, OFD, and image documents and sends selected files to Xiangyun OCR to extract document text and table content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liudengkui](https://clawhub.ai/user/liudengkui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run OCR over selected document files or folders, especially table-heavy PDFs, OFD files, and images, through Xiangyun's OCR API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are uploaded to netocr.com/Xiangyun for OCR processing. <br>
Mitigation: Use the skill only for documents approved for that external service, and avoid confidential IDs, contracts, financial records, or regulated data unless the provider and billing model are acceptable. <br>
Risk: The skill requires Xiangyun API credentials and its source guidance asks for secrets in chat. <br>
Mitigation: Enter credentials through the local --config flow where possible, avoid sharing secrets in chat, and protect or delete the local config.json after use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liudengkui/doc-ocr-xy) <br>
- [Xiangyun OCR service](https://netocr.com) <br>
- [Xiangyun OCR API reference](https://www.netocr.com/table.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text for single-file OCR, Markdown file output for folder OCR, and shell commands for configuration and execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create an OCR results Markdown file in the input folder and requires local Xiangyun API credentials before OCR execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
