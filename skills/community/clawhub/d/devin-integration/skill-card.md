## Description:

Delegate coding tasks to Devin AI agent. Create PRs, fix bugs, build features, and manage GitHub repos through Devin's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianalloway](https://clawhub.ai/user/ianalloway)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to prepare coding tasks for Devin, including repository context, requested changes, acceptance criteria, and suggested checks. It is intended for bug fixes, features, refactoring, repository maintenance, and related pull request work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A delegated task may include repository or project information that was not intended to be shared with Devin.

Mitigation: Share only the task information needed for the work.

Risk: Devin's repository access may permit changes beyond the intended task, and generated pull requests may need correction.

Mitigation: Configure repository permissions separately and review pull requests before merging.

## Reference(s):

- [Devin](https://app.devin.ai)
- [Skill homepage](https://github.com/ianalloway/openclaw-skills)
- [ClawHub skill page](https://clawhub.ai/ianalloway/skills/devin-integration)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown task briefs with repository details, requested work, acceptance criteria, and suggested test or lint commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
