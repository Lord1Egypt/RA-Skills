## Description: <br>
Convert Word documents (.doc, .docx) to HTML using MinerU's document processing engine, producing clean HTML output while preserving document structure and formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content managers, and publishing teams use this skill to convert .doc and .docx files into HTML for web publishing, CMS integration, and email templates. It guides agents to install and run the MinerU CLI with token-based authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external MinerU CLI/API and token-based authentication. <br>
Mitigation: Verify the mineru-open-api package source before installation and protect MINERU_TOKEN as a secret. <br>
Risk: Word documents submitted through MinerU may contain confidential or regulated data. <br>
Mitigation: Use the skill only when MinerU/OpenDataLab data handling is acceptable for the document content and applicable policies. <br>


## Reference(s): <br>
- [Doc To HTML on ClawHub](https://clawhub.ai/mzlzyca/doc-to-html) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU API Token Management](https://mineru.net/apiManage/token) <br>
- [OpenDataLab MinerU](https://github.com/opendatalab/MinerU) <br>
- [MinerU Ecosystem CLI](https://github.com/opendatalab/MinerU-Ecosystem) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the mineru-open-api CLI and MINERU_TOKEN; the external CLI produces HTML output from Word documents.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
