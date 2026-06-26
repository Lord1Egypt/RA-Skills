## Description: <br>
从抖音链接提取完整文案并生成Word文件。支持视频和图文笔记，保持原文案完整，不总结或改写。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[csak47mu](https://clawhub.ai/user/csak47mu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operators use this skill to extract complete caption text from user-provided Douyin links and receive the original text in a generated Word document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-provided Douyin pages and processes their content into a local temporary Word file. <br>
Mitigation: Use only links whose content may be fetched and returned through the chat, and avoid sensitive or private links unless that processing is acceptable. <br>
Risk: The bundled script suggests installing python-docx with --break-system-packages if the dependency is missing. <br>
Mitigation: Install python-docx in a normal virtual environment before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/csak47mu/douyin-text-grab) <br>
- [Publisher profile](https://clawhub.ai/user/csak47mu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated DOCX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local temporary Word documents from user-provided Douyin content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
