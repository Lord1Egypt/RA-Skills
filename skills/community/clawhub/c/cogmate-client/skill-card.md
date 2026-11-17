## Description:

Access Cogmate personal knowledge systems via API for knowledge retrieval, semantic search, and Q&A using a valid CogNexus access token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxiiwang](https://clawhub.ai/user/maxiiwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query a trusted Cogmate personal knowledge system, retrieve relevant facts, and ask Q&A-style questions through the Cogmate API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access tokens appear in URLs and command-line examples, which can expose private knowledge access through shell history, process listings, browser history, server logs, or proxy logs.

Mitigation: Use trusted Cogmate instances over HTTPS, prefer the lowest-scope and shortest-lived token available, avoid typing real tokens directly into helper-script command lines, and rotate any token already used in these examples.

## Reference(s):

- [Cogmate API Details](references/api-details.md)
- [CogNexus](https://github.com/MaxiiWang/CogNexus)
- [ClawHub Skill Page](https://clawhub.ai/maxiiwang/skills/cogmate-client)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Cogmate API endpoint and a valid access token.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
