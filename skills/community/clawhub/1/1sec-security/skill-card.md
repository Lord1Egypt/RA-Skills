## Description: <br>
Installs, configures, and manages the 1-SEC all-in-one cybersecurity platform on Linux servers and VPS instances, covering security monitoring, intrusion detection, endpoint defense, enforcement presets, alert management, and ongoing operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cutmob](https://clawhub.ai/user/cutmob) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and operators use this skill to install and operate 1-SEC on Linux servers, VPS instances, and AI agent hosts for local security monitoring, intrusion detection, and controlled enforcement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live enforcement can automatically block IPs, kill processes, quarantine files, or otherwise affect host behavior. <br>
Mitigation: Start with dry-run or the safe preset, monitor enforcement history, and enable live or vps-agent enforcement only after reviewing expected actions. <br>
Risk: Configured webhooks, cloud management, or Gemini correlation can send alert metadata or anonymized alert context off host. <br>
Mitigation: Keep optional integrations disabled unless needed, configure destinations deliberately, and review what each integration sends before enabling it. <br>
Risk: Full enforcement requires administrative privileges on the Linux host. <br>
Mitigation: Install only on systems you administer, verify the downloaded release and checksum, and use unprivileged or log-only operation when full enforcement is not required. <br>


## Reference(s): <br>
- [1-SEC Source Repository](https://github.com/1sec-security/1sec) <br>
- [1-SEC Security Policy](https://github.com/1sec-security/1sec/blob/main/SECURITY.md) <br>
- [1-SEC Configuration Reference](references/config-reference.md) <br>
- [1-SEC Operations Runbook](references/operations-runbook.md) <br>
- [VPS Agent Deployment Guide](references/vps-agent-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cutmob/1sec-security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include operational commands, configuration snippets, and risk notes; operators decide before execution.] <br>

## Skill Version(s): <br>
0.4.15 (source: server release metadata; artifact frontmatter reports 0.4.11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
