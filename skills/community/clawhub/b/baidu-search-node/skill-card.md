## Description:

Baidu Search Node is a Node.js command-line skill that queries Baidu web search and returns ranked result titles, summaries, and links without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsh66660](https://clawhub.ai/user/wsh66660)

### License/Terms of Use:

ISC

## Use Case:

Developers and agents use this skill to run Baidu web searches from Node.js workflows and receive a small ranked set of titles, summaries, and links. It is useful when Baidu search coverage is needed without configuring a Baidu API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented integration example can turn a search query into local shell command execution when copied directly.

Mitigation: Use spawn or execFile with argument arrays, validate the requested result count, and avoid interpolating user search text into shell commands.

Risk: Search queries are sent to Baidu and may expose secrets or sensitive personal data.

Mitigation: Do not submit secrets, credentials, confidential content, or sensitive personal data as search queries.

Risk: Dependency resolution uses package-lock entries from cnpm registry mirrors.

Mitigation: Regenerate the lockfile from the canonical npm registry or review dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wsh66660/skills/baidu-search-node)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Plain text search results with Markdown documentation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result count is configurable with the -n option; debug logging is configurable with the -d option.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
