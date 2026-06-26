## Description: <br>
Adds download tasks through Aria2 RPC and monitors download progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ingress007](https://clawhub.ai/user/Ingress007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to add HTTP, FTP, M3U8, and related download tasks to an Aria2 RPC service and inspect task status or progress from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aria2 RPC access can expose download control if the endpoint is reachable by untrusted clients or protected by a weak secret. <br>
Mitigation: Use the skill only with an Aria2 RPC server you control, keep RPC bound to localhost unless remote access is intentionally protected, and configure a strong unique secret. <br>
Risk: Progress and watch behavior relies on parsing responses from the Aria2 RPC server, which evidence flags as unsafe with untrusted or compromised servers. <br>
Mitigation: Treat progress and watch commands as unsafe for untrusted Aria2 servers until response parsing handles JSON strictly as data. <br>
Risk: Plain HTTP RPC endpoints can expose Aria2 RPC traffic when used across a network. <br>
Mitigation: Avoid plain HTTP for remote RPC endpoints; use local-only access or a protected transport when remote access is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ingress007/aria2-download) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Command-line output and JSON status responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Aria2 RPC URL, secret, and download directory configuration from environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
