## Description: <br>
Python-only integration of Claw Code harness engineering project with OpenClaw, providing offline access to mirrored tools and commands for security analysis, code quality, development workflows, and agent orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devita3323](https://clawhub.ai/user/devita3323) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route local prompts to a Python harness that lists, inspects, and executes mirrored Claw Code tools and commands for code review, security checks, workflow support, and agent orchestration patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, payloads, or session details may be retained in local logs. <br>
Mitigation: Avoid entering secrets or sensitive data unless local retention is acceptable, and review or disable event logging paths before use. <br>
Risk: The mirrored capability inventory may overstate real tool behavior. <br>
Mitigation: Treat tool and command results as local harness output and verify important findings with the underlying source files or independent tools. <br>
Risk: Bundled verification scripts are smoke tests rather than formal assurance. <br>
Mitigation: Run local review and security scanning before deployment, especially after modifying the artifact. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/devita3323/claw-code-suite-clean) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with shell command examples and structured JSON results from the local harness] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python execution; requires python3; command output may be capped by the harness.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, package.json, CHANGELOG, released 2026-04-06) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
