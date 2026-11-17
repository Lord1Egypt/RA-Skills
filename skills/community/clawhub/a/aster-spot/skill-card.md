## Description:

Aster Spot request using the Aster API. Authentication requires API key and secret key (HMAC SHA256). Supports mainnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuandiaodiaodiao](https://clawhub.ai/user/yuandiaodiaodiao)

### License/Terms of Use:

MIT

## Use Case:

Developers and trading operators use this skill to query Aster Spot market, account, order, transfer, withdrawal, and API-key endpoints through authenticated Aster API requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead agents to store Aster API keys and secrets in plaintext workspace Markdown.

Mitigation: Use a dedicated secret store instead of project Markdown, and provide only narrowly scoped Aster keys.

Risk: The documented endpoints include trading, transfer, withdrawal, and API-key creation actions on mainnet.

Mitigation: Require explicit user confirmation for each order, transfer, withdrawal, or API-key creation request, and prefer keys without withdrawal permissions.

Risk: Broad market-data endpoints can return large responses when symbol and limit parameters are omitted.

Mitigation: Always provide a specific symbol where supported, set the smallest useful limit, and filter complete JSON with jq.

## Reference(s):

- [Aster Spot Authentication](references/authentication.md)
- [Aster Spot API mainnet base URL](https://sapi.asterdex.com)
- [Aster Spot ClawHub skill page](https://clawhub.ai/yuandiaodiaodiao/skills/aster-spot)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance, Configuration]

**Output Format:** [JSON responses with Markdown guidance and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated requests require HMAC SHA256 signing with an Aster API key and secret key.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter metadata.version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
