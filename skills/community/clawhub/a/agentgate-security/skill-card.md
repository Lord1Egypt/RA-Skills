## Description: <br>
Enforces regex-based, real-time authorization policies on OpenClaw agents' tool calls, blocking, allowing, or requiring approval before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wiserautomation](https://clawhub.ai/user/wiserautomation) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security teams use this skill to add policy checks, audit logging, and approval gates before OpenClaw agents execute tool calls such as shell commands, web automation, filesystem access, outbound fetches, email actions, or payment API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service sends each agent tool call and its arguments to a hosted third-party service with limited data-handling detail in the release evidence. <br>
Mitigation: Install only if the publisher and npm package are trusted, protect AGENTGATE_API_KEY, and confirm audit-log retention, operator access, and data-handling terms before using sensitive workflows. <br>
Risk: Regex-based policies can over-match or under-match tool arguments, causing unintended blocks or missed risky actions. <br>
Mitigation: Test policies on representative tool calls, review audit logs, and use approval rules for high-impact actions before relying on automatic allow or deny behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wiserautomation/agentgate-security) <br>
- [AgentGate dashboard and service](https://agent-gate-rho.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include npm install commands, JavaScript integration snippets, regex policy examples, and operational guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
