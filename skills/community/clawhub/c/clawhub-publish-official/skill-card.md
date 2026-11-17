## Description:

Publish agent skills to ClawHub marketplace. Search, install, update, and publish skills from clawhub.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to work with the ClawHub CLI for marketplace search, installation, updates, authentication, and publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The global CLI install command does not pin a package version.

Mitigation: Install only from a trusted npm package source and prefer pinning the ClawHub CLI version for repeatable releases.

Risk: Bulk forced updates can change installed skills without interactive review.

Mitigation: Avoid unattended forced updates unless operating in a controlled environment; review changelogs and pin skill versions when stability matters.

Risk: Publishing a local skill directory could expose secrets or private files.

Mitigation: Review and scan skill directories for secrets before publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/clawhub-publish-official)
- [ClawHub Registry](https://clawhub.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ClawHub CLI binary.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
