## Description:

Provides Git commit, pull request, and branch workflow guidance with strict removal of AI-tool attribution from repository-facing content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to draft branch names, commits, and pull request descriptions according to prescribed Git workflow standards. It is also used to check repository-facing content against a policy that forbids AI-tool attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly instructs agents to remove AI-use disclosures, which can mislead collaborators or weaken audit trails.

Mitigation: Use only in repositories where policy explicitly forbids AI-tool attribution and confirm disclosure, authorship, and audit requirements before applying the guidance.

Risk: The skill includes amend, rebase, hook installation, and force-push workflows that can disrupt shared Git history.

Mitigation: Require explicit approval and repository-policy confirmation before amending commits, rebasing, installing hooks, or force-pushing.

## Reference(s):

- [AI Attribution Enforcement](references/ai-attribution-enforcement.md)
- [PR Templates](references/pr-templates.md)
- [Branch Naming Conventions](references/branch-conventions.md)
- [ClawHub Skill Page](https://clawhub.ai/urbantech/skills/ainative-git-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Git and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commit messages, PR descriptions, branch names, review checklists, and Git history-editing commands.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
