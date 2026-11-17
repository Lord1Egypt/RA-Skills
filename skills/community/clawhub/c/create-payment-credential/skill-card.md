## Description:

Gets secure, one-time-use payment credentials such as cards and tokens from a Link wallet so agents can complete purchases on behalf of users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danhill-stripe](https://clawhub.ai/user/danhill-stripe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill when an agent needs to authenticate with Link, evaluate a merchant checkout, create a user-approved spend request, and retrieve the correct one-time payment credential for a purchase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable real payment actions and handles payment credentials, payment methods, and shipping addresses.

Mitigation: Require explicit user confirmation before merchant, amount, item, payment method, shipping address, or domain changes; mask sensitive values unless the user directly requests disclosure.

Risk: The skill relies on broad package execution and mutable CLI installation paths.

Mitigation: Prefer a pinned and reviewed @stripe/link-cli version, avoid global installs where possible, and review the CLI before enabling it for agent use.

Risk: Persistent authentication files and retrieved card/SPT data could leak through shared workspaces, transcripts, or logs.

Mitigation: Store auth files outside shared workspaces with restricted permissions and use output-file handling for credential retrieval so stdout remains redacted.

## Reference(s):

- [Create Payment Credential on ClawHub](https://clawhub.ai/danhill-stripe/skills/create-payment-credential)
- [Link Agents](https://link.com/agents)
- [Link](https://link.com)
- [MPP/x402 Protocol](https://mpp.dev/protocol.md)
- [MPP HTTP 402 Protocol](https://mpp.dev/protocol/http-402.md)
- [MPP Challenges](https://mpp.dev/protocol/challenges.md)
- [Link App](https://app.link.com)
- [Link Support](https://support.link.com/topics/about-link)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Text]

**Output Format:** [Markdown guidance with inline shell commands, JSON/MCP configuration snippets, and CLI output references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output may be toon, JSON, Markdown, YAML, or local files; sensitive payment credentials should be redacted in stdout or written to restricted-permission files.]

## Skill Version(s):

0.6.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
