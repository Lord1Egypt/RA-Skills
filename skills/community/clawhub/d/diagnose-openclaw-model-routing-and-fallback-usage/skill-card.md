## Description: <br>
Diagnoses OpenClaw provider/model routing, fallback behavior, and ClaudeCodeCLI interruptions by correlating agent configuration with runtime logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[can4hou6joeng4](https://clawhub.ai/user/can4hou6joeng4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose whether OpenClaw agents are using the expected provider, model, and fallback chain, and to separate routing evidence from ClaudeCodeCLI execution failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic shell commands may search outside the intended project or service scope. <br>
Mitigation: Review proposed commands before execution and keep searches scoped to the relevant OpenClaw configuration or log paths. <br>
Risk: Temporary diagnostic output files may capture secrets or sensitive operational logs. <br>
Mitigation: Avoid writing secrets to /tmp output files, redact sensitive log content, and clean up diagnostic files when finished. <br>
Risk: Routing and fallback conclusions can be overstated when logs lack standard candidate decision fields. <br>
Mitigation: Treat missing fallback decision logs as incomplete evidence and separate confirmed provider/model calls from inferred fallback behavior. <br>


## Reference(s): <br>
- [ClaudeCodeCLI exit code 143 / SIGTERM reference](references/claudecodecli-exit-code-143-sigterm-reference.md) <br>
- [OpenClaw fallback log interpretation reference](references/openclaw-fallback-log-interpretation-reference.md) <br>
- [ClawHub skill release page](https://clawhub.ai/can4hou6joeng4/diagnose-openclaw-model-routing-and-fallback-usage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and diagnostic conclusions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on evidence boundaries, command review, and scoped local diagnostics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
