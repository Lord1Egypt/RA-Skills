## Description:

Agentic AI-native multi-tier routing routing, live packet tracing, and failover bypass engine for Pi-hole, Corerouting, routingdist, Unbound, Stubby, routingCrypt-Proxy, and VPN routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dedsecorg](https://clawhub.ai/user/dedsecorg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network operators use this skill to inspect routing service status, diagnose DNS/routing outages, trace packet flow, and prepare failover or enforcement commands for multi-tier routing infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose disruptive DNS or routing changes, including bypass, interception, packet-capture, database, REST API, and MCP actions.

Mitigation: Review commands before execution, require explicit confirmation for mutating actions, and document rollback procedures.

Risk: Running the skill against a broad environment could affect routing behavior beyond the intended scope.

Mitigation: Use least-privileged execution, verified absolute executable paths, and a pinned trusted install in environments where routing inspection or modification is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dedsecorg/skills/agentic-route)
- [Server-resolved GitHub provenance](https://github.com/dedsecorg/agentic-route/tree/master/skills/agentic-route)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that inspect or modify DNS and routing behavior.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
