## Description: <br>
GitHub Pull Request lifecycle management for creating, reviewing, merging, checking CI, resolving conflicts, managing drafts, and generating changelogs via the gh CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to manage GitHub pull request workflows, including PR creation, review status checks, CI checks, merge preparation, conflict handling, and changelog generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide or run powerful GitHub pull request actions such as approvals, merges, auto-merge, label edits, and review comments through the currently authenticated gh account. <br>
Mitigation: Confirm the active GitHub account, repository, PR number, target branches, CI status, and review requirements before executing those actions. <br>
Risk: Conflict-resolution workflows may involve merging, rebasing, and pushing branch updates after local changes. <br>
Mitigation: Review the branch, base ref, diff, and push target before pushing, especially after a rebase. <br>


## Reference(s): <br>
- [PR Templates](references/pr-templates.md) <br>
- [Label Conventions](references/label-conventions.md) <br>
- [GitHub CLI](https://cli.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON or Markdown changelog output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed and authenticated GitHub CLI for live repository operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
