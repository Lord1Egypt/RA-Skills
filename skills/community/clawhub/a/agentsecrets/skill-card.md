## Description: <br>
Zero-knowledge secrets infrastructure - AI agents manage the complete credential lifecycle without ever seeing values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steppacodes](https://clawhub.ai/user/steppacodes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to manage secret names, synchronize credential state, make authenticated API calls through AgentSecrets, and configure MCP or OpenClaw secret-resolution workflows without exposing plaintext credential values to the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports credential workflows and authenticated calls, so misuse or misplaced trust in the AgentSecrets CLI or publisher could affect sensitive systems. <br>
Mitigation: Install only when the publisher and AgentSecrets CLI are trusted, review workspace allowlists and production password gates, and confirm MCP registration before allowing agent-driven authenticated operations. <br>
Risk: Environment-variable injection can expose credentials through child process logs, telemetry, crash dumps, or inherited environments. <br>
Mitigation: Prefer the AgentSecrets proxy call or MCP API-call flow when possible, and reserve environment injection for processes whose logging and runtime environment have been reviewed. <br>
Risk: Agent-triggered outbound requests can send data to external services. <br>
Mitigation: Use the documented workspace domain allowlist, SSRF protections, and audit-log review commands to constrain destinations and inspect request history. <br>


## Reference(s): <br>
- [ClawHub agentsecrets listing](https://clawhub.ai/steppacodes/agentsecrets) <br>
- [AgentSecrets official website](https://agentsecrets.theseventeen.co) <br>
- [AgentSecrets engineering blog](https://engineering.theseventeen.co/series/building-agentsecrets) <br>
- [AgentSecrets security documentation](https://github.com/The-17/agentsecrets/blob/main/docs/PROXY.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are operational instructions for using the AgentSecrets CLI or MCP server; the skill is designed to operate on secret names rather than plaintext secret values.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
