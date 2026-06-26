## Description: <br>
Turn one Campus Copilot snapshot or MCP-backed current view into a plain-language what-to-do-first answer for a student. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, operators, and agent hosts use this skill to turn a Campus Copilot snapshot or read-only current view into one concrete next action with cited evidence and explicit trust gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Academic snapshot data may contain sensitive student information visible to the agent. <br>
Mitigation: Provide only snapshot or current-view data the student or operator is comfortable letting the agent read. <br>
Risk: Exporting a snapshot artifact creates a saved copy of the current-view evidence. <br>
Mitigation: Use export only when a saved proof artifact is needed and review where the artifact will be stored or shared. <br>
Risk: The optional Campus Copilot MCP setup runs a separate pnpm-based third-party project locally. <br>
Mitigation: Review the external MCP project and local configuration before launching it. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/xiaojiou176/current-view-triage) <br>
- [Campus Copilot Capability Map](references/CAPABILITIES.md) <br>
- [Campus Copilot MCP Setup](references/INSTALL.md) <br>
- [OpenHands / OpenClaw Demo Walkthrough](references/DEMO.md) <br>
- [Campus Copilot Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [Current View Input Shape](references/input-shape.md) <br>
- [Example Output](references/example-output.md) <br>
- [OpenHands MCP Configuration](references/OPENHANDS_MCP_CONFIG.json) <br>
- [OpenClaw MCP Configuration](references/OPENCLAW_MCP_CONFIG.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Plain-language Markdown with top_action, why_now, evidence_used, and trust_gaps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only, snapshot-scoped triage; does not claim live browser or session truth from snapshot-only evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
