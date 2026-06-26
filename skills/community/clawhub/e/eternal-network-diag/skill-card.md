## Description: <br>
Perform network diagnostics including ping, DNS resolution, TCP port checks, and traceroute for specified hosts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eternal0404](https://clawhub.ai/user/eternal0404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support engineers use this skill to run local network connectivity checks, DNS lookups, TCP port tests, and traceroute diagnostics against hosts they are authorized to inspect. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends network traffic to user-provided hosts and can expose diagnostic output in the terminal. <br>
Mitigation: Use it only for systems where you have permission to test connectivity, and avoid sharing terminal output that contains sensitive hostnames or addresses. <br>
Risk: The reported connectivity, DNS, port, and route results are point-in-time observations and can be affected by local network policy, timeouts, or missing system tools. <br>
Mitigation: Confirm important findings with approved operational tooling before making production changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eternal0404/eternal-network-diag) <br>
- [Publisher profile](https://clawhub.ai/user/eternal0404) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text and Markdown-style command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Diagnostics run against a user-supplied host and optional port.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
