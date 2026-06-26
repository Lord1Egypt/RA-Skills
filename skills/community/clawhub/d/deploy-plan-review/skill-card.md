## Description: <br>
变更方案自动审核助手用于审核变更方案 docx 和部署表 xlsx，按 /home/deploy_template 下的模板进行对比，默认返回精简 Markdown 并保存 Word 报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bounding-elk](https://clawhub.ai/user/bounding-elk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations engineers and deployment reviewers use this skill to check change-plan documents against standard deployment templates, verify consistency with deployment spreadsheets, and produce concise review findings plus saved report files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores raw deployment plans, spreadsheets, generated reports, and issue evidence under the skill directory without stated retention controls. <br>
Mitigation: Use it only where persistent local storage of those documents is acceptable, avoid live credentials in submitted files, and manually purge raw archives, outputs, and tracking workbooks when retention is not appropriate. <br>


## Reference(s): <br>
- [Python 中文 f-string 引号陷阱](artifact/references/pitfalls.md) <br>
- [ClawHub skill page](https://clawhub.ai/bounding-elk/skills/deploy-plan-review) <br>
- [Publisher profile](https://clawhub.ai/user/bounding-elk) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with generated Word and Excel report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a change-plan .docx and normally a deployment .xlsx; may also use an optional management spreadsheet.] <br>

## Skill Version(s): <br>
3.3.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
