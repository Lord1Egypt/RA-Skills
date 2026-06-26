## Description: <br>
飞书会议纪要自动生成工具。从飞书妙记链接、minute token 或现成 transcript 文件生成结构化中文会议纪要，并可选导出 PDF、上传回飞书云空间。适用于用户提供飞书妙记链接要求整理会议纪要、要求将逐字稿转正式文档、或希望把会议录音对应 transcript 快速整理成可分发纪要的场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jfvincentyang](https://clawhub.ai/user/jfvincentyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to turn Feishu meeting minutes links, minute tokens, or local transcript files into structured Chinese meeting minutes. It can also export the minutes as PDF and upload the PDF to Feishu Drive when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may access Feishu meeting transcripts through lark-cli when fetching minutes. <br>
Mitigation: Install only when transcript access is acceptable and grant only the Feishu scopes needed for the intended workflow. <br>
Risk: The optional upload path can send generated PDFs to Feishu Drive. <br>
Mitigation: Grant the Drive upload scope only when upload is required and review the PDF before uploading or sharing it. <br>
Risk: Generated meeting minutes may omit context or misstate decisions from the transcript. <br>
Mitigation: Review generated minutes against the original transcript before distribution. <br>
Risk: PDF generation and upload depend on local external tools. <br>
Mitigation: Use trusted local installations of pandoc, xelatex, and lark-cli. <br>


## Reference(s): <br>
- [Meeting Minutes Template](references/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown meeting minutes with optional PDF file and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces session-scoped transcript-derived minutes; PDF export and Feishu Drive upload are optional.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, release evidence, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
