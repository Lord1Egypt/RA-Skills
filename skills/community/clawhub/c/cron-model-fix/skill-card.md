## Description: <br>
Diagnose and fix OpenClaw cron job model override issues. Use when cron jobs show "not allowed, falling back to agent defaults" in logs, experience unexpected cloud token burn, have slow run times, or models aren't being applied correctly. Fixes agent model allowlist configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mklue](https://clawhub.ai/user/mklue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw cron jobs whose configured model is rejected and to update the agent model allowlist so the intended model can run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Adding the wrong model to the OpenClaw allowlist can authorize unintended agent or cron model use. <br>
Mitigation: Confirm the model name before applying changes, run with --dry-run first, keep the generated backup, validate ~/.openclaw/openclaw.json, and restart the gateway only when ready for the policy change to take effect. <br>


## Reference(s): <br>
- [OpenClaw Model Configuration Layers](references/model-config-layers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to ~/.openclaw/openclaw.json and a gateway restart after validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
