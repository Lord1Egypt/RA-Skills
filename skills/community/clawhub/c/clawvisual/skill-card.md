## Description:

URL or long-form text to social carousel generator via local CLI and MCP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suinia](https://clawhub.ai/user/suinia)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use Clawvisual to turn URLs or long-form text into social carousel content through a local CLI/MCP workflow with async job polling and optional revision commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running the npm CLI introduces supply-chain risk.

Mitigation: Install only a trusted or pinned reviewed version and prefer an isolated environment when possible.

Risk: The CLI requires an LLM API key for generation workflows.

Mitigation: Use scoped keys, avoid exposing local config files, and rotate keys if logs or workspaces are shared.

Risk: Raw tool invocation can pass untrusted tool names or arguments to the local service.

Mitigation: Avoid the raw call command with untrusted tool names or arguments; prefer the documented CLI commands.

## Reference(s):

- [Clawvisual ClawHub skill page](https://clawhub.ai/suinia/skills/clawvisual)
- [suinia ClawHub publisher profile](https://clawhub.ai/user/suinia)
- [clawvisual npm package](https://www.npmjs.com/package/clawvisual)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [JSON stdout from CLI commands plus concise markdown guidance for command workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Job-based asynchronous outputs are polled with status --job; generated carousel results are returned in command output.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
