## Description:

Access public X (Twitter) posts, users, threads, trends, communities, and lists through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find and retrieve public X posts, account information, conversations, trends, community data, and list data through DataXAPI. It provides endpoint discovery and calling guidance through MCP, REST, or the command line, with per-call prices documented.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup terms and endpoint-discovery wording are sent to DataXAPI and may contain sensitive details.

Mitigation: Omit confidential details from lookup terms.

Risk: Paid data retrieval calls can add to account spending.

Mitigation: Set spending limits and use the documented per-call price caps.

Risk: The API key could be exposed while configuring or using a client.

Mitigation: Protect the key; do not print it, log it, or place it in a URL.

Risk: The external CLI package and service are outside the artifact review.

Mitigation: Prefer REST or hosted MCP, or use a reviewed, fixed CLI version.

## Reference(s):

- [DataXAPI Skills](https://dataxapi.com/skills/)
- [DataXAPI Agent Setup](https://dataxapi.com/agents.md)
- [DataXAPI X API Reference](https://dataxapi.com/apis/x/)
- [DataXAPI X Pricing](https://dataxapi.com/pricing/x/)
- [DataXAPI MCP Endpoint](https://api.dataxapi.com/mcp)

## Skill Output:

**Output Type(s):** [Text, API calls, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Text or Markdown, with JSON, shell, or REST request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public X data; data retrieval calls may incur the documented per-call charges.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
