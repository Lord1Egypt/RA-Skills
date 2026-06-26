## Description: <br>
Diagnoses OpenClaw issues through staged triage, documentation and issue search, validation, repair guidance, and diagnostic report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikewongonline](https://clawhub.ai/user/mikewongonline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to troubleshoot OpenClaw bugs, configuration drift, tool failures, and feature implementation questions. It helps collect context, compare evidence, propose fixes, validate outcomes, and produce diagnostic reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local profile or session context and persist troubleshooting history or diagnostic reports. <br>
Mitigation: Review what local context and logs will be read or saved, redact secrets from command output, and avoid persistent reports when their contents are not safe to store. <br>
Risk: Repair guidance may include exec, write, fix, or doctor commands that modify the user's environment. <br>
Mitigation: Require explicit approval before running modifying commands, confirm the target environment, and provide a rollback command before execution. <br>
Risk: Diagnostic reports and error summaries can include raw command output that may contain credentials or private project details. <br>
Mitigation: Mask API keys, tokens, user identifiers, internal project names, and other sensitive values before displaying or saving reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikewongonline/autofix-theclaw) <br>
- [Skill control document](artifact/SKILL.md) <br>
- [Quick Start v5.0](artifact/docs/tutorials/QUICK_START_v5.0.md) <br>
- [Diagnosis report enhancements](artifact/docs/enhancement/MODULE_03_Enhancement_Reports.md) <br>
- [v5.0 changes](artifact/docs/reports/CHANGES_v5.0.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command suggestions, diagnostic summaries, JSON-like analysis, and generated HTML reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save troubleshooting history or diagnostic reports; command-based repair flows should require explicit user approval.] <br>

## Skill Version(s): <br>
5.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
