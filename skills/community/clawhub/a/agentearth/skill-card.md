## Description:

External tool marketplace for discovering and executing AgentEarth API-backed tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanminghui](https://clawhub.ai/user/shanminghui)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use AgentEarth to discover task-relevant external API-backed tools, build validated execution parameters, and return concise summaries of live tool results when host policy permits external API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts and execution parameters may contain sensitive data that is sent to AgentEarth when the skill is used.

Mitigation: Use the skill only for tasks intended to use AgentEarth, prefer built-in or local tools for sensitive tasks, and avoid sending secrets unless the selected tool explicitly requires them.

Risk: The AgentEarth API key could be exposed if sent to an unvalidated endpoint or surfaced in logs.

Mitigation: Send the API key only to validated HTTPS AgentEarth endpoints and redact the key from user-visible output and logs.

Risk: A recommended tool may require concrete values such as URLs, IDs, tokens, code snippets, or schema-specific fields.

Mitigation: Validate required fields, types, enums, and unknown-field rules before Execute, and ask the user for missing real values instead of inventing parameters.

## Reference(s):

- [AgentEarth API Specification](references/api-specification.md)
- [AgentEarth Homepage](https://agentearth.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with HTTP, JSON, Bash, and PowerShell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENT_EARTH_API_KEY and may summarize live external tool results from AgentEarth.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
