## Description:

Automatically generates changelogs by analyzing git commit history, categorizing changes, and turning technical commits into user-friendly release notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

MIT

## Use Case:

Developers, release managers, and product teams use this skill to produce customer-facing changelogs, release notes, app store update text, and internal release summaries from git history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private repository commit history or optional style-guide content may contain internal names, issue IDs, or security-sensitive details.

Mitigation: Review generated release notes before publishing and avoid including confidential commit details in prompts or output.

Risk: Generated changelogs can misstate user impact when commit messages are ambiguous or overly technical.

Mitigation: Have a maintainer review categories, wording, and omissions against the actual release before publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guohongbin-git/skills/changelog-generator-cn)
- [Packaged Skill Homepage](https://clawhub.com/skills/changelog-generator-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown changelog or release notes with categorized entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May incorporate date ranges, target versions, and project-specific changelog style guidance supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
