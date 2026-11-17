## Description:

Detect DFS radar events and reset Ubiquiti airOS devices to restore configured frequencies, managed by UISP NMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drodecker](https://clawhub.ai/user/drodecker)

### License/Terms of Use:

MIT-0

## Use Case:

WISP network operators and support engineers use this skill to inspect UISP-managed Ubiquiti airOS access points, identify DFS-related frequency shifts, audit client signal quality, and reboot an affected AP only after explicit operator confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reset can temporarily disconnect clients on the affected access point.

Mitigation: Require explicit operator confirmation, confirm device identity and customer impact before rebooting, and verify recovery with a follow-up DFS check.

Risk: AP, client, and signal audit outputs can expose sensitive operational network data.

Mitigation: Install only with a trusted MCP server and treat generated audits and telemetry summaries as restricted operational information.

Risk: Network-wide sweeps may return partial results when some APs are unreachable.

Mitigation: Report unreachable APs separately and avoid combining broad sweep actions with reset actions in one step.

## Reference(s):

- [DFS Reset Skill Page](https://clawhub.ai/drodecker/skills/dfs-reset)
- [Source project for the MCP server](https://github.com/wispnet/wisp-reset-airos-mcp/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown operator reports with MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AP frequency comparisons, device health summaries, client signal audits, reset confirmation prompts, and follow-up verification notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
