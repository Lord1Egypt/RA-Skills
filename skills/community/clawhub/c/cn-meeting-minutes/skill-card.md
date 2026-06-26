## Description: <br>
会议纪要生成工具。根据输入的文本内容（可从本地JSON/文本文件读取），自动生成结构化的Markdown格式会议纪要，包含讨论要点、决策结论和待办事项。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and developers use this skill to turn Chinese meeting text from local text, JSON, or standard input into structured Markdown meeting minutes with discussion points, decisions, and action items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads whichever local input file path the user provides, which may contain sensitive meeting content. <br>
Mitigation: Run it only on intended local files and review whether meeting content is appropriate for the execution environment. <br>
Risk: The selected output path can be written or overwritten. <br>
Mitigation: Use an explicit output path and check for existing files before writing generated minutes. <br>
Risk: Rule-based extraction may miss or misclassify discussion points, decisions, or action items. <br>
Mitigation: Review the generated Markdown before sharing it or treating it as an official meeting record. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-meeting-minutes) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown meeting-minutes document with CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local .txt or .json input, or standard input, and writes a Markdown file to the selected output path.] <br>

## Skill Version(s): <br>
1.4.3 (source: server release metadata; artifact frontmatter says 1.4.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
