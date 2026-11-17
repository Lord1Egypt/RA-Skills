## Description:

Converts X (Twitter) tweets, threads, and articles to Markdown with YAML front matter using a disclosed reverse-engineered API flow that requires user consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to save X posts, threads, and articles as local Markdown files for review, archiving, or downstream writing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live X session cookies.

Mitigation: Use a dedicated X account or Chrome profile, avoid shared or synced cookie storage, and rotate or revoke X sessions after use.

Risk: Media downloads can fetch files from content the user did not author.

Mitigation: Avoid --download-media for untrusted content until URL allowlisting, download limits, and safer cookie storage are added.

Risk: The converter uses a reverse-engineered X API rather than an official API.

Mitigation: Require the documented consent flow before conversion and warn users that the API may break or affect account access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimliu/skills/baoyu-danger-x-to-markdown)
- [Baoyu skills homepage](https://github.com/JimLiu/baoyu-skills#baoyu-danger-x-to-markdown)
- [First-time setup reference](references/config/first-time-setup.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown files with YAML front matter, optional JSON status output, and shell commands for running the converter.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally download referenced media to local imgs/ and videos/ directories and rewrite Markdown links.]

## Skill Version(s):

1.117.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
