## Description: <br>
Scans submitted code for security issues such as hardcoded secrets and dangerous functions, then returns a confidence score and detailed findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crftsmnd](https://clawhub.ai/user/crftsmnd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and CI/CD workflows use this skill to request a paid pre-deploy code security scan and receive issue details with a confidence score. It is suited for quick static checks before shipping code, especially where local security tooling is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted code is sent to the service operator and may contain secrets or proprietary material. <br>
Mitigation: Redact secrets before use and avoid regulated or proprietary code unless approved. <br>
Risk: The service uses a paid scan flow and security evidence calls out payment verification concerns for self-hosted production use. <br>
Mitigation: Require explicit confirmation for paid scans and fix payment verification before relying on a self-hosted deployment in production. <br>
Risk: Temporary-file handling in the self-hosted scanner may leave sensitive submitted code exposed if failures occur. <br>
Mitigation: Harden temporary-file cleanup before production self-hosting and keep submitted code scoped to approved environments. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/crftsmnd/agentkilox-code-audit) <br>
- [Publisher profile](https://clawhub.ai/user/crftsmnd) <br>
- [A2A Code Audit endpoint](https://a2a-code-audit.cvapi.workers.dev/audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON API responses with confidence scores, issue lists, severities, and scan statistics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid scan flow; maximum submitted code size is 500KB; expected response time is under 5 seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
