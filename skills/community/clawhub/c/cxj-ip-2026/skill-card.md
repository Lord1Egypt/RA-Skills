## Description: <br>
Get both public (external) and local (internal) IP addresses using simple shell commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenxinjie005](https://clawhub.ai/user/chenxinjie005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to find public and local IP addresses for firewall allowlists, VPN setup, LAN troubleshooting, port forwarding, and routing checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public IP lookup services may receive a request from the user's network. <br>
Mitigation: Use an organization-approved endpoint in sensitive environments. <br>
Risk: Local IP commands vary by operating system and shell environment. <br>
Mitigation: Use the operating-system-specific command shown by the skill and verify results before applying network configuration changes. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/chenxinjie005/cxj-ip-2026) <br>
- [ifconfig.me public IP endpoint](https://ifconfig.me) <br>
- [ipify public IP API](https://api.ipify.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may contact public IP lookup services and print network addresses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
