## Description:

Bitbucket Cloud wrapper optimized for Pull Request Code Analysis. Enables the agent to securely review Pull Requests, split large diffs by file, review code structure, and read specific repository files. Ideal for providing automated code reviews or debugging PRs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zan768616253](https://clawhub.ai/user/zan768616253)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to inspect Bitbucket Cloud pull requests, retrieve diffs and related metadata, and produce thorough PR review guidance. It can also browse repositories, branches, commits, files, and directory listings available to the configured Bitbucket token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read PR diffs, comments, commit metadata, repository files, and branch listings available to the configured Bitbucket token.

Mitigation: Use a narrowly scoped read-only Bitbucket token with only repository read and pull request read access.

Risk: Generated review Markdown may contain sensitive repository details and can be saved under the skill's reviews directory for email automation.

Mitigation: Review local review exports before distribution and avoid running the skill against repositories whose contents should not be persisted in local review files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zan768616253/skills/bitbucket-toolbox)
- [Skill Homepage](https://github.com/zan768616253/skill-bitbucket-toolbox)
- [Bitbucket Cloud REST API Endpoint](https://api.bitbucket.org/2.0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON and raw text from Bitbucket API wrapper commands, plus Markdown review guidance or review files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, python3, BITBUCKET_API_TOKEN, and BITBUCKET_WORKSPACE; commands use read-only HTTPS GET requests to Bitbucket Cloud.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
