## Description: <br>
将自然语言编码需求转换为当前项目中的 requests.txt 需求文档，并自动用本地编辑器打开。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bombers26](https://clawhub.ai/user/bombers26) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to turn brief Chinese natural-language coding requests into a starter requirements document for AI-assisted coding work. It is intended for use inside the project folder where the generated requests.txt should be created. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes or overwrites requests.txt in the current project directory. <br>
Mitigation: Run it only from the intended project folder and check for an existing requests.txt before use. <br>
Risk: The skill automatically launches a local editor after creating the requirements file. <br>
Mitigation: Use it only when local editor launch is expected, and prefer a future version that asks before launching the editor or removes shell=True. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bombers26/coder-helper) <br>
- [Publisher profile](https://clawhub.ai/user/bombers26) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style requirements text written to requests.txt plus a brief status message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or overwrites requests.txt in the selected project directory and launches a local editor when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
