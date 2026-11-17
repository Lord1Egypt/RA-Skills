## Description:

Automatically creates user-facing changelogs from git commits by analyzing commit history, categorizing changes, and transforming technical commits into clear, customer-friendly release notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsuyungfeng](https://clawhub.ai/user/hsuyungfeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, release managers, and product teams use this skill to generate polished changelogs and release notes from repository commit history for product releases, app store submissions, customer updates, and internal release documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated changelog text may be inaccurate, incomplete, or less appropriate for the intended audience than a human-authored release note.

Mitigation: Review the generated changelog against the repository commit history before publishing.

Risk: The agent reads repository commit history where the skill is invoked.

Mitigation: Use the skill only in repositories whose commit history is appropriate for the agent environment to inspect.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hsuyungfeng/skills/changelog-generator-pro)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown changelog or release notes text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use user-specified date ranges, version ranges, and changelog style guidelines.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
