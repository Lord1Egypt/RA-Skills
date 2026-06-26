## Description: <br>
Comprehensive bug audit for Node.js web projects that guides an agent to dissect code into project-specific audit tables, verify each item, and supplement with security, reliability, and regression checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abczsl520](https://clawhub.ai/user/abczsl520) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to audit Node.js web projects for security, logic, data-flow, concurrency, reliability, and regression issues. It is intended for authorized reviews of owned projects or systems where testing scope is clear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit workflow may encourage disruptive load, brute-force, replay, upload, or mutation testing if scope is not set before execution. <br>
Mitigation: Use the skill only on owned or explicitly authorized systems, and keep disruptive validation in local or staging environments unless production testing is specifically approved. <br>
Risk: The reference material includes a debug-log endpoint pattern that would be unsafe if copied into production without controls. <br>
Mitigation: Require authentication, redaction, retention limits, and environment gating for any debug logging endpoint, and remove or disable it outside approved debugging sessions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abczsl520/bug-audit) <br>
- [Audit Modules](references/modules.md) <br>
- [Pitfall Lookup Table](references/pitfalls.md) <br>
- [Red Team / Blue Team Playbook](references/redblue.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown audit report with tables, findings, fixes, and verification notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed tests or shell commands for authorized local or staging validation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
