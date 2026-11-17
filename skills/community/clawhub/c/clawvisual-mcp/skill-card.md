## Description:

URL or long-form text to social carousel generator via local CLI + MCP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suinia](https://clawhub.ai/user/suinia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Clawvisual to turn URLs or long-form text into social carousel content through a local CLI and MCP workflow, then poll, revise, or regenerate generated jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The global npm CLI can start a local web/MCP service and store API keys on disk.

Mitigation: Install only in approved environments, secure or remove ~/.clawvisual/config.json, and rotate exposed keys.

Risk: User content and API keys may be transmitted to the configured LLM or MCP service.

Mitigation: Use approved endpoints, keep CLAWVISUAL_MCP_URL on localhost or HTTPS, and avoid submitting sensitive or proprietary content unless the service is approved.

Risk: The raw MCP call command can invoke broad tool access.

Mitigation: Treat raw MCP calls as developer-level access and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suinia/skills/clawvisual-mcp)
- [Publisher profile](https://clawhub.ai/user/suinia)
- [npm package: clawvisual](https://www.npmjs.com/package/clawvisual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [JSON responses from CLI and MCP calls, with human-facing Markdown guidance for setup and workflow use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are designed for deterministic stdout parsing by upstream agents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
