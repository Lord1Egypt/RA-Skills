## Description: <br>
Clinical Tempo helps agents find and use the Clinical Tempo repository context, troubleshooting notes, OpenClaw setup, MPP/x402 payment patterns, Tempo references, EVVM notes, and verification commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arunnadarasa](https://clawhub.ai/user/arunnadarasa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill while working on the Clinical Tempo HealthTech Protocol app to locate authoritative context, avoid known MPP, x402, Tempo, EVVM, OpenAPI, and port 8787 traps, and configure optional OpenClaw or editor reminders without exposing secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional hooks can add repeated context reminders outside the intended Clinical Tempo workflow if enabled too broadly. <br>
Mitigation: Keep activation scoped to the Clinical Tempo workspace and enable hooks only where bootstrap reminders are useful. <br>
Risk: Agent-proposed CLAWHUB.md entries could preserve inaccurate debugging notes or secret values. <br>
Mitigation: Review proposed entries for accuracy and ensure only non-secret environment names or public facts are recorded. <br>
Risk: The skill references a separate Anyway OpenClaw plugin that is not bundled with this release. <br>
Mitigation: Assess and install the external plugin separately according to the user's organizational trust path. <br>


## Reference(s): <br>
- [Clinical Tempo ClawHub listing](https://clawhub.ai/arunnadarasa/clinicaltempo) <br>
- [OpenClaw + Clinical Tempo](references/openclaw-clinical-tempo.md) <br>
- [OpenClaw integration guide](references/openclaw-integration.md) <br>
- [Concrete examples](references/examples.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Hooks setup](references/hooks-setup.md) <br>
- [EVVM protocol context](https://www.evvm.info/llms-full.txt) <br>
- [MPPScan discovery](https://www.mppscan.com/discovery) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline file paths and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose non-secret CLAWHUB.md entries, smoke-test commands, and OpenClaw or editor hook configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
