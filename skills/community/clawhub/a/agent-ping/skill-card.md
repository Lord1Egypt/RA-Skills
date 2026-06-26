## Description: <br>
Agent Ping discovers OADP agent-discovery signals on a target domain across HTTP headers, well-known metadata, robots.txt, DNS TXT records, HTML metadata, and hub ping responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Agent Ping to scan domains they own or are authorized to test for OADP agent-discovery signals, then review suggested registration or install commands when a hub is found. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanning domains without authorization can create policy, privacy, or abuse-reporting risk because the skill makes outbound HTTP and DNS requests. <br>
Mitigation: Use the skill only on domains you own or are authorized to test, and expect network traffic to the target domain. <br>
Risk: A discovered hub may receive a ping request and the skill may print registration, AGENTS.md append, or follow-on install commands. <br>
Mitigation: Review discovered hub URLs and any generated registration, file-append, or install commands before running them. <br>


## Reference(s): <br>
- [Agent Ping on ClawHub](https://clawhub.ai/imaflytok/agent-ping) <br>
- [OADP Protocol](https://onlyflies.buzz/clawswarm/PROTOCOL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Terminal text with suggested shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a domain input; results depend on live network responses from the target domain and discovered hub endpoints.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
