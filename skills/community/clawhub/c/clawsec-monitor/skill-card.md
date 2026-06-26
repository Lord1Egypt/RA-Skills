## Description: <br>
Clawsec Monitor helps agents configure and operate a local HTTP/HTTPS inspection proxy for monitoring AI-agent traffic and detecting secret leakage, sensitive file access, and command-injection patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[funsaized](https://clawhub.ai/user/funsaized) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to inspect AI-agent network traffic, review detected threats, configure per-process proxy and CA settings, and clean up local monitoring state after use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local proxy can inspect sensitive AI-agent HTTP and HTTPS traffic, which creates privacy and credential-exposure risk if used too broadly. <br>
Mitigation: Use per-process proxy and CA trust settings, avoid system-wide CA trust on production machines, and run the monitor only for agents intentionally being inspected. <br>
Risk: Docker or proxy exposure beyond localhost could allow unintended clients to route traffic through the monitor. <br>
Mitigation: Restrict Docker and proxy bindings to localhost unless broader access is explicitly required. <br>
Risk: Generated CA material and threat logs remain under /tmp/clawsec after use. <br>
Mitigation: Delete /tmp/clawsec and remove any trusted CA when monitoring is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/funsaized/clawsec-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/funsaized) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with shell commands, configuration examples, and threat interpretation notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include commands that start or stop a local proxy, configure environment variables, inspect JSONL threat logs, or remove local CA material.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
