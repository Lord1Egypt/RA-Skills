## Description: <br>
Converts Word .doc and .docx documents into structured Markdown with MinerU while preserving headings, lists, tables, and paragraph structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and content teams use this skill to convert Word documents from local files or URLs into Markdown for documentation, static sites, wikis, blogs, GitHub, Notion, Obsidian, or migration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document conversion may involve the third-party MinerU/OpenDataLab service, including content from Word documents or private URLs. <br>
Mitigation: Avoid processing confidential documents or private URLs unless that service use is approved, and use a revocable MINERU_TOKEN where possible. <br>
Risk: .doc conversion requires MINERU_TOKEN authentication. <br>
Mitigation: Use the token-free flash-extract path for eligible .docx files, and avoid exposing MINERU_TOKEN in shared logs or transcripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mzlzyca/doc-to-markdown) <br>
- [MinerU Homepage](https://mineru.net) <br>
- [MinerU Token Management](https://mineru.net/apiManage/token) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Converted document content can stream to stdout or be saved to an output directory; status messages are sent to stderr.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
