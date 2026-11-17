## Description: <br>
面向开发者的网络诊断辅助工具,涵盖DNS解析调试、端口连通性测试、HTTP请求诊断与TLS证书检查。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to troubleshoot everyday network issues by checking DNS records, host and port connectivity, HTTP timing, TLS certificate details, and local DNS cache state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may cause an agent to run live outbound DNS, HTTP, TLS, ping, nc, curl, and openssl probes against named hosts or resolvers. <br>
Mitigation: Require operator confirmation for live probes, verify target hostnames and resolvers before execution, and avoid repeated timing requests against third-party services without authorization. <br>
Risk: The skill includes privileged local actions such as package installs, DNS cache flushing, and /etc/hosts edits. <br>
Mitigation: Require explicit confirmation before sudo, package-management, cache-flush, or hosts-file commands, and review command effects before applying local network changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dns-networking-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, YAML, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live network diagnostic command suggestions, configuration snippets, structured status data, logs, and remediation guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
