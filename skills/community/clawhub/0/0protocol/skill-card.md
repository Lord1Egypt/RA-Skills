## Description: <br>
Agents can sign plugins, rotate credentials without losing identity, and publicly attest to behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0isone](https://clawhub.ai/user/0isone) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use 0.protocol to configure agents for signed identity claims, plugin behavior attestations, and authenticated handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Claim and transfer payloads may become durable, public, and identity-linked records. <br>
Mitigation: Avoid including secrets, private task context, or sensitive identifiers in signed claims or handoffs, especially when visibility is public. <br>
Risk: The skill configures agents to use a remote MCP service for signed identity claims and handoffs. <br>
Mitigation: Install it only when the agent is expected to use 0protocol's remote MCP service for those workflows. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/0isone/0protocol) <br>
- [README / Spec](https://github.com/0isone/0protocol) <br>
- [API Reference](https://github.com/0isone/0protocol/blob/main/API.md) <br>
- [Migration Guide](https://github.com/0isone/0protocol/blob/main/migration.md) <br>
- [Why](https://github.com/0isone/0protocol/blob/main/WHY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter for the recommended setup path.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
