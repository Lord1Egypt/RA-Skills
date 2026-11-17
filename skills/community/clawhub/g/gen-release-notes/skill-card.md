## Description:

Generate release notes for changes since a given tag.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to inspect repository changes since a prior tag, categorize user-visible changes, suggest a Semantic Versioning bump, and update CHANGELOG.md using Keep a Changelog structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads repository history and PR metadata and edits CHANGELOG.md, so an incorrect or untrusted tag can produce misleading release notes or incorrect compare links.

Mitigation: Use a trusted existing tag such as v1.2.3, avoid option-like or whitespace-containing tag values until validation is hardened, and review the generated changelog before committing it.

## Reference(s):

- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and changelog entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit CHANGELOG.md and relies on a valid previous git tag; PR metadata is used when the GitHub CLI is available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
