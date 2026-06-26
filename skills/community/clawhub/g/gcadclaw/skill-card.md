## Description: <br>
Generates, modifies, validates, and repairs 2D GstarCAD drawings through pygcadwin, including DWG automation, screenshot feedback, and before/after entity validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dolphindz](https://clawhub.ai/user/dolphindz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CAD engineers use this skill to turn natural-language mechanical drawing requirements into GstarCAD 2D DWG outputs with documented assumptions, validation artifacts, screenshots, and repair steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended to let an agent control GstarCAD and write local drawing artifacts. <br>
Mitigation: Run it only in a Windows environment where GstarCAD automation is expected, and use a dedicated project or output folder. <br>
Risk: Generated DWG files, screenshots, and entity exports may contain sensitive design information. <br>
Mitigation: Review the DWG, PNG, JSON, and feedback files before sharing them outside the intended project context. <br>
Risk: Drawing execution depends on local Windows, Python, pygcadwin, and GstarCAD COM availability. <br>
Mitigation: Validate the Python environment and inspect feedback artifacts before treating a drawing task as complete. <br>


## Reference(s): <br>
- [Gcadclaw ClawHub Listing](https://clawhub.ai/dolphindz/gcadclaw) <br>
- [pygcadwin PyPI Package](https://pypi.org/project/pygcadwin/) <br>
- [2D pygcadwin Workflow](references/2d-pygcadwin-workflow.md) <br>
- [Feedback Loop](references/feedback-loop.md) <br>
- [Python Package Manifest](references/python_package_manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python code and shell commands, plus generated DWG files, JSON entity feedback, PNG screenshots, and summary reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows, Python, pygcadwin, and a live GstarCAD installation for drawing execution and screenshot validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
