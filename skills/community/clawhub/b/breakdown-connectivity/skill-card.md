## Description:

Diagnoses connectivity failures with Breakdown on macOS and helps agents use or configure Breakdown's local MCP server for network evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breakdown](https://clawhub.ai/user/breakdown)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to diagnose Internet, DNS, Wi-Fi, packet loss, latency, endpoint reachability, browser, API, upload, download, MCP, and cloud-tool failures. It is also used to install Breakdown, connect its local MCP bridge, and identify the Breakdown evidence tools available to an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup commands can install a persistent local Breakdown app and add a persistent MCP client entry.

Mitigation: Review install and configure commands before running them, confirm macOS 13 or later, and configure only the intended Codex or Claude Code scope.

Risk: Installer or app trust depends on the expected macOS signature and publisher identity checks succeeding.

Mitigation: Use the bundled verification steps before opening the installer, launching the app, or adding the MCP bridge to a client.

Risk: Historical retained issues can be mistaken for current connectivity failures.

Mitigation: Compare issue timestamps with the reported failure and use focused time windows and bounded result counts.

## Reference(s):

- [Breakdown MCP tools](references/mcp-tools.md)
- [Breakdown for Agents](https://breakdown.live/for-agents/)
- [Breakdown macOS Download](https://breakdown.live/download/mac)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and MCP tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local setup commands, MCP client configuration, and references to Breakdown evidence tools.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
