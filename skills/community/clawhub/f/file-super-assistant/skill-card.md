## Description: <br>
文件创建与 AI 降味助手。支持 docx/xlsx/pptx/pdf 文件创建和编辑，提供 AI 内容改写为人类风格功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create DOCX, XLSX, PPTX, and PDF files and to rewrite Chinese AI-generated text into a more natural human style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some scripts silently write to hard-coded OneDrive/Desktop destinations and keep local file history. <br>
Mitigation: Review before installing, prefer scripts that require an explicit output path, and remove or modify hard-coded destinations before use. <br>
Risk: Generated files may overwrite or alter important local content if paths are reused. <br>
Mitigation: Confirm output paths and overwrite behavior before running the document generation or rewriting scripts on important files. <br>
Risk: The AI-humanization feature may be misused to obscure AI assistance where disclosure is required. <br>
Mitigation: Use rewriting only for legitimate editing and disclose AI assistance when policy, law, or platform rules require it. <br>


## Reference(s): <br>
- [AI 内容特征与降味规则](artifact/references/ai-flavor-rules.md) <br>
- [ClawHub release page](https://clawhub.ai/cp3d1455926-svg/file-super-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands, generated document files, and rewritten text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local files; some artifact scripts use fixed Windows desktop output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
