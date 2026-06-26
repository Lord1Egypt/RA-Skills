## Description: <br>
Detect DFS radar events and reset Ubiquiti airOS devices to restore configured frequencies, managed by UISP NMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drodecker](https://clawhub.ai/user/drodecker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
WISP operators and network engineers use this skill to inspect UISP-managed Ubiquiti airOS access points for DFS channel shifts, AP health issues, connected-client signal quality, and operator-approved resets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: reset_device can disrupt service for clients connected to the selected access point. <br>
Mitigation: Confirm the exact AP identity and expected client disruption with the operator before approving any reset. <br>
Risk: A reset may be used for non-DFS symptoms without enough diagnosis. <br>
Mitigation: Check DFS status, AP health, and client impact first, then verify recovery with a follow-up detect_dfs call after the reset. <br>
Risk: The skill depends on an external MCP server and UISP credentials. <br>
Mitigation: Install only with a trusted MCP server and least-privilege UISP credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drodecker/dfs-reset) <br>
- [Referenced MCP server project](https://github.com/wispnet/wisp-reset-airos-mcp/) <br>
- [DFS Detection & Reset Example](examples/dfs_investigation.md) <br>
- [Device Reset Workflow Example](examples/reboot_workflow.md) <br>
- [Signal Audit Example](examples/signal_audit.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted MCP endpoint, an initialized session, and operator confirmation before reset_device.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
