## Description:

Searches the web through the CSTCloud Web Search API and returns concise search results for OpenClaw users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shcw0405](https://clawhub.ai/user/shcw0405)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to run web searches through CSTCloud from chat or command-line workflows, especially when they prefer a domestic Chinese search API provider. It requires a configured CSTCloud API key and returns titles, URLs, sources, and summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to CSTCloud along with authentication for the configured account.

Mitigation: Avoid searching for secrets, credentials, or confidential internal text, and use an API key scoped for this skill where possible.

Risk: Installing an unpinned or unverified package can increase supply-chain exposure.

Mitigation: Prefer a verified or pinned ClawHub installer and run the skill under a non-administrative account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shcw0405/skills/cstcloud-web-search)
- [ClawHub publisher profile](https://clawhub.ai/user/shcw0405)
- [CSTCloud Uni-API web-search endpoint](https://uni-api.cstcloud.cn/v1/web-search)
- [Referenced OpenClaw bailian-web-search skill](https://github.com/openclaw/skills/tree/main/skills/krisyejh/bailian-web-search)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text search results and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, jq, and the CSTCLOUD_API_KEY environment variable; accepts a search query and an optional result count from 1 to 10.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
