## Description: <br>
防火墙配置工具包免费版 helps personal developers configure Linux server firewalls, manage UFW and iptables rules, inspect ports, and run basic security baseline checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate and review Linux firewall hardening guidance, UFW and iptables command examples, port checks, and baseline audit steps for personal servers or small projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privileged firewall resets, default-deny policies, and service changes can disrupt networking or lock administrators out of remote hosts. <br>
Mitigation: Review every command before execution, keep current rule backups, confirm management access allow rules, and use console access plus a tested rollback plan before applying changes. <br>
Risk: Hardening examples can restart SSH or install services, which may affect production, shared, or nonstandard-SSH hosts. <br>
Mitigation: Avoid running reset or hardening examples on remote, production, shared, or nonstandard-SSH systems unless the operating environment and recovery path are explicitly verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/firewall-toolkit-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command examples and JSON result structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes privileged Linux firewall administration examples that require review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
