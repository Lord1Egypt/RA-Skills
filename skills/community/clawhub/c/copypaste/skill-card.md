## Description:

Read and create pastes on copy-paste.cloud. Fetch recent public pastes, retrieve a paste by ID, or publish new content via the public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orti99](https://clawhub.ai/user/orti99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch recent public pastes, retrieve known paste IDs, and publish text or code snippets to copy-paste.cloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected paste content and COPYPASTE_API_KEY are sent to copy-paste.cloud, a third-party service.

Mitigation: Use the skill only for content you are comfortable sending to that service and keep API keys scoped and rotated according to local policy.

Risk: Non-private pastes should be treated as public and may expose sensitive material.

Mitigation: Do not paste credentials, tokens, private source code, regulated data, or sensitive internal material.

Risk: Password-protected paste retrieval places the password in the request URL.

Mitigation: Avoid using password-protected paste retrieval for secrets until password-in-URL handling is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/orti99/skills/copypaste)
- [Publisher profile](https://clawhub.ai/user/orti99)
- [copy-paste.cloud](https://copy-paste.cloud)
- [copy-paste.cloud developer API key page](https://copy-paste.cloud/developer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and plain-text paste results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires COPYPASTE_API_KEY for recent-paste listing and paste creation; uses curl, jq, and python3 for script execution.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
