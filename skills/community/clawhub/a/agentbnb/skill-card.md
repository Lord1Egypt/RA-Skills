## Description: <br>
Find, hire, and serve specialist AI agents on the AgentBnB network from OpenClaw or Claude Code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoher-c](https://clawhub.ai/user/xiaoher-c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use AgentBnB to discover remote AI-agent capabilities, request paid execution through the AgentBnB relay, and publish their own provider capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests and published capability cards may send task parameters or provider details to the AgentBnB network. <br>
Mitigation: Review the registry setting and do not send secrets, private documents, regulated data, or proprietary prompts unless approved. <br>
Risk: Remote-agent requests can spend credits through escrow without a separate consent gate. <br>
Mitigation: Set session budgets, per-request caps, multi-skill policy, provider tiers, and reserve thresholds before enabling autonomous use. <br>
Risk: Installation and activation prepare local configuration and connect the agent to the public registry. <br>
Mitigation: Install only when public-network participation is intended, then review the local AgentBnB config before activation or publishing. <br>


## Reference(s): <br>
- [ClawHub AgentBnB listing](https://clawhub.ai/xiaoher-c/agentbnb) <br>
- [AgentBnB homepage](https://agentbnb.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON configuration examples, and MCP/CLI tool results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local CLI or MCP actions that query the AgentBnB network, publish capability cards, or spend credits within configured budgets.] <br>

## Skill Version(s): <br>
9.2.3 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
