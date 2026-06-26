## Description: <br>
Reviews AI-modified code for requirement alignment, unnecessary file changes, code quality issues, and change-impact risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanghao-smile](https://clawhub.ai/user/yanghao-smile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review AI-generated code changes against the original request, detect unrelated modifications, assess quality and security concerns, and produce actionable review guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads repository files and Git history, which can expose sensitive project information during review. <br>
Mitigation: Install and run it only in repositories where that access is acceptable, and avoid using it on projects containing secrets or restricted data unless appropriate controls are in place. <br>
Risk: The skill declares file.write permission even though its primary behavior is analysis and report generation. <br>
Mitigation: Review generated reports or file changes before accepting them, and disable or constrain file-writing behavior where the host environment permits. <br>
Risk: Optional pre-commit and CI snippets can run automated review commands as part of development workflows. <br>
Mitigation: Review those snippets before enabling them and scope automation to the intended branches, events, and repositories. <br>


## Reference(s): <br>
- [Code Review Guidelines](references/review-guidelines.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yanghao-smile/easy-code-review) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/yanghao-smile) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, html, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown review reports by default, with optional JSON or HTML report output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include requirement-fit findings, unnecessary-change findings, risk levels, quality notes, and improvement recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
