## Description:

Provides a CLI workflow for Baidu Maps development, account and API key management, map styles, and location tasks through Baidu Map Agent Plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-maps](https://clawhub.ai/user/baidu-maps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to set up Baidu Maps tools and manage accounts, API keys, and map styles. They can also use it to perform location search, route planning, geocoding, weather queries, and generate map integration code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP setup instructions reportedly expose credential-bearing configuration, according to the security assessment.

Mitigation: Avoid sharing full MCP configuration in conversations or logs; use secret-redacted review before installation.

Risk: The security scan was partial and does not establish that the skill is safe.

Mitigation: Treat the scan as inconclusive and review the skill and any credential-bearing configuration before installation.

## Reference(s):

- [Baidu Maps JavaScript API endpoint (V4.0)](https://api.map.baidu.com/api?v=4.0&ak=YOUR_AK)
- [Baidu Map CLI ClawHub release page](https://clawhub.ai/baidu-maps/skills/bmap-cli)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with shell commands, configuration examples, code samples, and map task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable setup guidance and account-sensitive configuration examples.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
