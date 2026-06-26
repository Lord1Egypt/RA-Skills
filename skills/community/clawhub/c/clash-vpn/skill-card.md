## Description: <br>
Manage Clash VPN proxy service for accessing blocked websites like Google Play, including setup, configuration updates, service control, proxy testing, and proxy-based access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxnan](https://clawhub.ai/user/lxnan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage a Clash VPN proxy service, update its configuration, start or stop the service, inspect status, and test local HTTP or SOCKS proxy connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default configuration guidance may expose proxy, DNS, or controller listeners to the network. <br>
Mitigation: Bind controller and DNS listeners to localhost, disable LAN access unless required, and add controller authentication or firewall rules before remote use. <br>
Risk: The skill can overwrite the root Clash configuration used by a system-level service. <br>
Mitigation: Review supplied proxy configuration before update, keep the automatic backup, and validate the Clash configuration before restarting the service. <br>


## Reference(s): <br>
- [Clash VPN on ClawHub](https://clawhub.ai/lxnan/clash-vpn) <br>
- [Clash VPN Configuration Guide](references/config-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write system-level Clash configuration, manage the Clash process, and report proxy connectivity results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
