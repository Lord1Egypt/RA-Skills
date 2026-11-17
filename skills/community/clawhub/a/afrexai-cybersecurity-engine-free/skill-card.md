## Description: <br>
Afrexai Cybersecurity Engine Free helps agents perform authorized cybersecurity assessments, including security posture review, STRIDE threat modeling, OWASP Top 10 application review, and infrastructure hardening guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and automation teams use this skill to scope and document authorized security assessments across code repositories, application designs, web applications, containers, cloud configuration, and infrastructure. It produces prioritized findings, checklists, and remediation guidance for review by responsible security owners. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide security assessment activity using broad read and command-execution capability. <br>
Mitigation: Use it only on systems you are authorized to assess, define the approved target scope before use, and review proposed shell commands before execution. <br>
Risk: Assessment outputs and scanner-style findings may be incomplete or require validation. <br>
Mitigation: Have a qualified security owner review findings, prioritize remediation, and verify fixes before relying on the results. <br>
Risk: Examples and configuration guidance may involve API keys or sensitive operational details. <br>
Mitigation: Store secrets in environment variables or managed secret stores, avoid committing keys to repositories, and redact sensitive data from shared reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/afrexai-cybersecurity-engine-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown reports, checklists, tables, remediation guidance, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed by a human security owner before acting on findings or running proposed commands.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
