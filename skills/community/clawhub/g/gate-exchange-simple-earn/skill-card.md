## Description: <br>
Gate Simple Earn management skill for flexible and fixed-term savings workflows, including product discovery, positions, interest, subscribe, redeem, and change-min-rate operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to manage Gate Simple Earn flexible and fixed-term products through an agent, including querying rates and positions and preparing confirmed subscribe, redeem, early-redeem, and min-rate-change actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real crypto Earn account actions such as subscribe, redeem, early redeem, and min-rate changes. <br>
Mitigation: Use narrowly scoped credentials and require a clear action draft plus explicit immediate confirmation before any write action. <br>
Risk: The skill relies on external Gate MCP setup and a mutable remote runtime-rules source. <br>
Mitigation: Verify the Gate MCP server and runtime-rules source before installation or release approval. <br>
Risk: Under-scoped action routing may route ambiguous Earn requests to account-changing operations. <br>
Mitigation: Ask clarifying questions for ambiguous requests and re-query account state after confirmed actions. <br>


## Reference(s): <br>
- [Gate Exchange Simple Earn ClawHub Listing](https://clawhub.ai/gate-exchange/gate-exchange-simple-earn) <br>
- [Gate SimpleEarn MCP Specification](references/mcp.md) <br>
- [Simple Earn Flexible (Uni) MCP Tools Reference](references/earn-uni-mcp-tools.md) <br>
- [Fixed Earn (Fixed-term) MCP Tools Reference](references/fixed-earn-mcp-tools.md) <br>
- [Simple Earn Scenarios and Prompt Examples](references/scenarios.md) <br>
- [Gate MCP Server](https://github.com/gate/gate-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown responses with action drafts, result summaries, and MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write actions require explicit user confirmation and post-action verification.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter version: 2026.3.23-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
