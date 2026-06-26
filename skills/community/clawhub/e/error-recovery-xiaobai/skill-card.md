## Description: <br>
Systematic error recovery for AI agents that structures diagnosis, bounded retries, and reporting after tool failures to prevent silent failures, endless retries, and incorrect escalation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aptratcn](https://clawhub.ai/user/aptratcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when tool calls, shell commands, network requests, or file operations fail so the agent records the error, reasons about likely causes, tries bounded recovery, and reports the outcome. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers may activate the workflow more often than intended. <br>
Mitigation: Apply it only to clear tool, HTTP, filesystem, authentication, timeout, or process failures, and confirm relevance before starting recovery. <br>
Risk: Recovery suggestions can involve privileged commands, permission changes, repository pushes, API uploads, or credential handling. <br>
Mitigation: Require explicit user confirmation before any privileged or external side-effecting action. <br>
Risk: Error records and reports may capture credentials or sensitive operational details. <br>
Mitigation: Redact tokens, secrets, private paths, and sensitive request or response data before logging, reporting, or saving errors to memory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aptratcn/error-recovery-xiaobai) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [English README](artifact/README_EN.md) <br>
- [Error diagnostic script](artifact/scripts/error-diagnose.mjs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional local diagnostic script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a 4R recovery flow and limits repeated recovery attempts to three changed attempts before reporting failure.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
