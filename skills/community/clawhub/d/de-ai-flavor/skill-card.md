## Description:

Checks Chinese Markdown articles for AI-translation phrasing and edits wording to sound more natural.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryso](https://clawhub.ai/user/terryso)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and developers use this skill to review Chinese Markdown files for common AI-translation style patterns, apply targeted wording changes, and inspect the resulting diff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill edits the target Markdown file directly before showing a diff.

Mitigation: Run it on version-controlled or otherwise restorable files, then review the diff before keeping the changes.

Risk: Style edits may change wording that the author intentionally chose.

Mitigation: Limit acceptance to suggestions that preserve the article's meaning, technical terms, and original structure.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown issue report with direct file edits and git diff output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Edits the target Markdown file before presenting the diff for review.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
