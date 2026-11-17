## Description:

Interact with GitHub via the gh CLI -- issues, PRs, CI runs and repository health with auto-changelog and issue triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to inspect GitHub repository health, generate changelog text, triage open issues, and review pull request, check, and workflow-run status through the GitHub CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the user's existing gh authentication to read repository metadata, issues, PRs, commits, and workflow runs for requested repositories.

Mitigation: Run it only for repositories where that access is appropriate, and confirm the active gh account and scopes before using it with private or sensitive repositories.

Risk: Advanced gh api usage can run against repositories where the user's account may have write privileges.

Mitigation: Review advanced gh api commands before execution and prefer read-only account permissions for repository reporting workflows.

Risk: Some script output is Danish, which may make operational recommendations easier to misread for non-Danish readers.

Mitigation: Translate or review the generated output before using it to prioritize repository maintenance work.

## Reference(s):

- [ClawGit Pro ClawHub skill page](https://clawhub.ai/northcap-group/skills/clawgit-pro)
- [northcap-group publisher profile](https://clawhub.ai/user/northcap-group)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and terminal text with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the GitHub CLI; private repository data depends on the user's existing gh authentication.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
