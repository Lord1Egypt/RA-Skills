## Description:

Browse Bitbucket repositories, manage branches, review pull requests, and work with source code via the Bitbucket Cloud API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Bitbucket repository contents, manage branches, review pull requests, and coordinate code workflows from chat through ClawLink and the Bitbucket Cloud API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and persistently allowlists an unpinned external plugin with OAuth-backed repository write capabilities.

Mitigation: Verify the ClawLink plugin publisher, prefer a pinned and reviewed version when available, and remove the plugin allowlist if behavior does not match expectations.

Risk: Repository, branch, pull request, and issue write operations can change or delete Bitbucket resources accessible to the connected account.

Mitigation: Connect Bitbucket with the minimum scopes needed and review every preview before approving write operations.

Risk: OAuth access may remain active after installation.

Mitigation: Be prepared to revoke the OAuth integration if access is no longer needed or if any activity looks wrong.

## Reference(s):

- [Bitbucket Cloud REST API](https://developer.atlassian.com/cloud/bitbucket/rest/)
- [Bitbucket Repository API](https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/)
- [Bitbucket Pull Request API](https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pullrequests/)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/bitbucket-repos)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires review and explicit confirmation before write operations.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
