## Description: <br>
Config Diagnose helps troubleshoot environment variables, API keys, services, ports, files, and OpenClaw skill configuration, then returns findings and suggested fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongrebeccahhh-boop](https://clawhub.ai/user/dongrebeccahhh-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to diagnose broken email, API, service, file, and skill configuration. It produces shell-based checks, diagnostic status output, and remediation guidance for local configuration problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic output can expose sensitive local details or token fragments. <br>
Mitigation: Run it only in trusted environments, review output before sharing it, and patch API-key reporting to fully redact secrets. <br>
Risk: File-search diagnostics can scan broad local paths such as /root and reveal private file names or paths. <br>
Mitigation: Restrict searches to explicit user-approved directories and avoid running broad searches on shared systems. <br>
Risk: Heartbeat monitoring can repeatedly inspect local system state and generate proactive alerts. <br>
Mitigation: Keep heartbeat integration disabled unless it is deliberately configured, reviewed, and scoped to expected checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dongrebeccahhh-boop/config-diagnose) <br>
- [Publisher profile](https://clawhub.ai/user/dongrebeccahhh-boop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with diagnostic status lines and shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect local environment variables, processes, ports, paths, network reachability, and OpenClaw workspace state.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
