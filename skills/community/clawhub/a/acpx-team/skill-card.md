## Description: <br>
The skill guides agents in using acpx and the Agent Client Protocol to delegate work, coordinate multi-agent councils, run deliberation workflows, and manage ACP-compatible coding-agent sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[csuwl](https://clawhub.ai/user/csuwl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to coordinate multiple ACP-compatible agents for code review, security audits, architecture review, implementation, testing, and consensus-building workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can normalize approval-bypassing or auto-approval agent modes during delegated coding work. <br>
Mitigation: Keep read-only, deny-all, or approval-gated modes as defaults, and reserve permission-bypass modes for tightly controlled automation. <br>
Risk: Delegated prompts and code context may be shared with external AI providers through configured agents. <br>
Mitigation: Avoid secrets and sensitive data, use clean branches or sandboxes, and confirm provider policies before sharing task content. <br>
Risk: Global npm installs and delegated agent commands can affect the local development environment. <br>
Mitigation: Pin and verify npm-installed tools where possible and run delegated work in isolated workspaces. <br>


## Reference(s): <br>
- [Collaboration Protocols](references/protocols.md) <br>
- [Role Definitions & Team Presets](references/roles.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include multi-agent workflow plans, role assignments, session-management commands, and approval-mode recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
