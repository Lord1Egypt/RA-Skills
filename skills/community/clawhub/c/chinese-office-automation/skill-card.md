## Description: <br>
中文办公自动化 - 专为中文用户设计的办公自动化技能套件。集成中文文档处理、拼音转换、节假日判断、农历支持等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LiJie298](https://clawhub.ai/user/LiJie298) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking employees, external users, and developers use this skill to automate Chinese office workflows such as document processing, pinyin conversion, Chinese date formatting, lunar calendar conversion, workday checks, and standard office templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on Python packages for Chinese calendar, pinyin, and conversion behavior. <br>
Mitigation: Install dependencies only from trusted package sources and review the installed package versions before deployment. <br>
Risk: The artifact describes referenced scripts and an automatic holiday update mechanism that are not supplied in the artifact. <br>
Mitigation: Treat the skill as documentation or a scaffold until the scripts and update mechanism are supplied and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LiJie298/chinese-office-automation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are oriented to Simplified Chinese office automation workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
