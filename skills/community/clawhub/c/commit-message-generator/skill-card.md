## Description: <br>
Git 提交信息生成器。根据代码变更内容自动生成符合 Conventional Commits 规范的提交信息，包含类型、范围、简短描述、详细说明和关联的 Issue/需求号。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gnllk](https://clawhub.ai/user/gnllk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill after code changes to draft Conventional Commits-style Git commit messages, including change type, scope, body text, and issue references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Git-related activation phrases may trigger the skill during normal development discussion. <br>
Mitigation: Invoke it only when a commit message is intended, and review the generated message before using it. <br>
Risk: Diffs or change descriptions can contain secrets or sensitive implementation details. <br>
Mitigation: Avoid pasting secrets, credentials, customer data, or private operational details into the skill input. <br>


## Reference(s): <br>
- [Conventional Commits Reference](references/conventional-commits.md) <br>
- [Commit Message Examples](references/commit-examples.md) <br>
- [Conventional Commits](https://www.conventionalcommits.org/) <br>
- [ClawHub Skill Page](https://clawhub.ai/gnllk/commit-message-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown containing a generated commit message, metadata, and copyable git commit command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated content should be reviewed before use, especially when input includes diffs or issue references.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
