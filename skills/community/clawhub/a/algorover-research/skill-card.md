## Description:

Discover AlgoRover Research strategies, preview and run historical backtests, inspect or cancel jobs, and download research reports through the hosted MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[algorover](https://clawhub.ai/user/algorover)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and strategy analysts use this skill to discover available strategies, prepare and review historical backtests, monitor or cancel jobs, and download reports through AlgoRover Research. Historical results do not establish future returns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command uses the latest ClawHub CLI, which is not pinned to a reviewed version.

Mitigation: Review the CLI version and package before installing or running it.

Risk: Research data can be deleted, including all Research data when the service confirmation value is supplied.

Mitigation: Delete only a selected result after an explicit request; require a separate explicit request and service confirmation before deleting all Research data.

Risk: Strategy discovery may default to English when the user expects Chinese results.

Mitigation: Set the requested locale explicitly and preserve it in subsequent tool calls.

Risk: Personal research inputs are sent to the hosted service and associated with the signed-in account.

Mitigation: Use the client's browser authorization flow and review the service privacy information before sending sensitive research inputs.

## Reference(s):

- [AlgoRover Research service](https://research.algorover.ai/)
- [OpenClaw MCP documentation](https://docs.openclaw.ai/tools/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Natural-language summaries and Markdown, with service-returned status, metrics, configuration details, and report links when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the hosted service and the user's authorization; historical backtest results do not establish future returns.]

## Skill Version(s):

0.1.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
