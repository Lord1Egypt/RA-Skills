## Description: <br>
aaPanel/BT-Panel server monitoring and administration skill for OpenClaw, covering system resources, sites, services, SSL certificates, SSH logs, cron jobs, files, databases, firewall rules, FTP, and PHP version switching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[social5h3ll](https://clawhub.ai/user/social5h3ll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, sysadmins, and homelab operators use this skill to connect OpenClaw to aaPanel/BT-Panel servers and run monitoring, configuration, and administrative CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive aaPanel credentials and stores server tokens in a local OpenClaw configuration file. <br>
Mitigation: Use dedicated least-privilege aaPanel tokens where possible, restrict permissions on ~/.openclaw/bt-skills.yaml, and avoid exposing config output in shared logs. <br>
Risk: The skill can perform destructive or high-impact production-server actions such as deleting sites or databases, changing firewall rules, revoking certificates, changing passwords, downloading remote URLs, overwriting files, and applying recursive permissions. <br>
Mitigation: Manually review proposed commands before execution and run high-impact actions only against the intended server and path. <br>
Risk: SSL verification can be disabled for self-signed panels, increasing exposure to man-in-the-middle attacks. <br>
Mitigation: Keep SSL verification enabled whenever possible and disable it only for controlled environments where the panel endpoint is otherwise trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/social5h3ll/aapanel-5h3ll) <br>
- [aaPanel GitHub](https://github.com/aaPanel) <br>
- [OpenClaw Project](https://github.com/openclaw/openclaw) <br>
- [Publisher Profile](https://clawhub.ai/user/social5h3ll) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands; scripts emit JSON, tables, and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.10+ and configured aaPanel API tokens.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence, artifact metadata, README, and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
