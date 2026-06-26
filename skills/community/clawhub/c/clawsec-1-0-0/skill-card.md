## Description: <br>
Intercept and inspect AI agent HTTP/HTTPS traffic with a MITM proxy to detect and log exfiltration and injection threats in real time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shi8103312](https://clawhub.ai/user/shi8103312) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to operate ClawSec Monitor, route AI agent traffic through its proxy, interpret threat logs, troubleshoot HTTPS MITM setup, and configure Docker or local deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad HTTPS interception can expose sensitive traffic and requires trust-store changes. <br>
Mitigation: Use the monitor only where interception is authorized, prefer per-process CA settings over system-wide trust installation, and remove the CA when finished. <br>
Risk: Persistent threat and proxy logs may contain sensitive snippets or destinations. <br>
Mitigation: Protect log files, delete or rotate captured logs regularly, and remove persistent Docker volumes when no longer needed. <br>
Risk: The skill documents operation of a separate ClawSec Monitor codebase that is not included in the artifact. <br>
Mitigation: Separately review and trust the actual monitor code before installation or execution. <br>


## Reference(s): <br>
- [Clawsec 1.0.0 on ClawHub](https://clawhub.ai/shi8103312/clawsec-1-0-0) <br>
- [Publisher profile: shi8103312](https://clawhub.ai/user/shi8103312) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide users through proxy operation, HTTPS trust setup, Docker deployment, threat-log interpretation, and troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
