## Description: <br>
Doc OCR helps agents use MinerU to extract searchable, editable text from scanned or image-embedded Word (.docx) documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, office teams, legal teams, and archivists use this skill to configure MinerU OCR for Word documents whose useful content is embedded as scanned pages or images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents processed through MinerU may contain confidential, regulated, customer, or secret-bearing information that is sent to an external parsing provider. <br>
Mitigation: Use the skill only when organizational policy permits sending the document content to MinerU and the provider retention and privacy terms are understood. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mzlzyca/doc-ocr) <br>
- [MinerU Homepage](https://mineru.net) <br>
- [MinerU Token Management](https://mineru.net/apiManage/token) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI flags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mineru-open-api and MINERU_TOKEN; OCR output can be sent to stdout or saved to a target directory.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
