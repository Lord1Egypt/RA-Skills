## Description: <br>
Debug DNS resolution and network connectivity. Use when troubleshooting DNS failures, testing port connectivity, diagnosing firewall rules, inspecting HTTP requests with curl verbose mode, configuring /etc/hosts, or debugging proxy and certificate issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose DNS, connectivity, HTTP, firewall, proxy, and certificate issues with practical command-line checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some examples can change persistent network behavior, including firewall rules, hosts-file overrides, global proxy settings, and certificate handling. <br>
Mitigation: Review these commands before use, run them only with explicit intent, and keep rollback steps available. <br>
Risk: Proxy examples can expose credentials if real usernames or passwords are placed directly in commands or shared logs. <br>
Mitigation: Avoid embedding real proxy credentials in command lines, shell history, tickets, or shared diagnostic output. <br>
Risk: Certificate-bypass examples can weaken TLS protections if reused outside temporary troubleshooting. <br>
Mitigation: Use certificate bypass only for short-lived diagnostics and restore normal certificate validation afterward. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples should be reviewed before execution, especially commands that alter system network settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
