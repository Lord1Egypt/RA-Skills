## Description: <br>
Manage and interpret ClawSec Monitor v3.0, a proxy that inspects AI agent HTTP/HTTPS traffic, detects threats, and logs suspicious activity in real time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhc1991](https://clawhub.ai/user/zhc1991) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security-minded operators use this skill to start, configure, and troubleshoot ClawSec Monitor and interpret proxy threat logs for AI-agent traffic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad HTTPS interception and trusting a local CA can expose plaintext traffic beyond the intended agent scope. <br>
Mitigation: Prefer --no-mitm or per-process CA variables over system-wide CA trust, and route only the intended agent traffic through the proxy. <br>
Risk: Threat logs may contain secrets or sensitive request and response snippets. <br>
Mitigation: Treat ClawSec log files and Docker volumes as sensitive, restrict access, and remove the trusted CA and persisted volume when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhc1991/clawsec-bak) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that affect proxy routing, Docker services, CA trust, and local log files; review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
