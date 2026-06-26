## Description: <br>
Enforce conventional commit messages with semantic validation, scope checking, and automated fix suggestions for git workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review, validate, and improve conventional commit messages in local Git workflows, hooks, CI checks, and branch cleanup before merge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Git hook or CI configuration could enforce an unintended commit policy if enabled without review. <br>
Mitigation: Review any proposed hook or CI configuration before enabling it for local development or shared repositories. <br>
Risk: Automated commit-message fixes could affect commit history when paired with amend or history-rewrite workflows. <br>
Mitigation: Require explicit confirmation before amending commits or rewriting branch history. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/flyai-commit-lint) <br>
- [Publisher Profile](https://clawhub.ai/user/dingtom336-gif) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with commit-message examples, validation findings, fix suggestions, and optional shell or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest Git hook or CI configuration; users should review generated automation before enabling it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
