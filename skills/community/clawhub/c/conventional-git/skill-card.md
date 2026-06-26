## Description: <br>
Conventional Commits v1.0.0 branch naming, worktree naming, and commit message standards for GitHub and GitLab projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to create consistent Git branch names, worktree names, commit messages, and issue-closing footers that support parseable history and changelog automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated git or gh commands can affect repository state or remote GitHub resources if approved without review. <br>
Mitigation: Review generated commands before approval and run them only in the intended repository and branch. <br>
Risk: Issue-closing footers can close the wrong GitHub or GitLab issue when the reference is incorrect. <br>
Mitigation: Verify issue numbers and cross-repository references before merging to the default branch. <br>
Risk: The skill advises against AI attribution in commits, which may conflict with a project's disclosure policy. <br>
Mitigation: Override that convention when project, legal, or governance requirements require AI disclosure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/conventional-git) <br>
- [Project Homepage](https://github.com/samber/cc-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with branch names, commit-message examples, and inline git or gh commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git; may propose git or gh commands for user review before execution.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
