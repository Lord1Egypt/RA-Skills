## Description: <br>
Analyze staged or committed changes and recommend split, squash, amend, or commit-message strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect staged, unstaged, or recently committed Git changes and decide when to split, squash, amend, or rewrite commits. It also guides commit-message discipline, intentional staging, and public-repository secret checks before commit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git history rewrite operations such as reset, amend, rebase, and force-push can disrupt shared or protected branches. <br>
Mitigation: Review every reset, amend, rebase, and force-push step before execution; verify the target branch and CI state; prefer force-with-lease when a force push is explicitly approved. <br>
Risk: Commit recommendations or generated commands may not match the repository's review, branch, or language policy. <br>
Mitigation: Check the staged file list, repository visibility, and drafted commit message before committing; override the skill's commit-message guidance when local policy differs. <br>
Risk: A public commit may accidentally include sensitive credentials in staged content. <br>
Mitigation: Run the documented staged-diff secret checks before public-repository commits, sanitize any match, and re-scan before proceeding. <br>


## Reference(s): <br>
- [Commit Tidy skill definition](SKILL.md) <br>
- [Interactive Amend](interactive-amend.md) <br>
- [Soft Reset Amend](soft-reset-amend.md) <br>
- [Staging Discipline](staging-discipline.md) <br>
- [Security Scan](security-scan.md) <br>
- [Commit Message Discipline](message-discipline.md) <br>
- [ClawHub release page](https://clawhub.ai/drumrobot/commit-tidy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include changed-file categories, split or squash recommendations, proposed commit messages, and Git command sequences for user review.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata and CHANGELOG, released 2026-06-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
