## Description: <br>
Provides a local Python helper to send minimal review payloads to a trusted AANA HTTP bridge for policy guidance inside the skill package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route redacted action-review summaries to a trusted local AANA bridge before acting on sensitive or policy-relevant work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payloads may contain secrets or unnecessary private records. <br>
Mitigation: Use redacted summaries only, avoid secrets and raw private records, and rely on the helper's secret-like key checks before sending a payload. <br>
Risk: Bridge recommendations may be treated as authoritative without review. <br>
Mitigation: Treat bridge output as guidance unless the bridge and policy have been separately reviewed and trusted. <br>
Risk: A missing or untrusted local bridge could lead to unreliable guardrail decisions. <br>
Mitigation: Use the helper only with a trusted localhost AANA bridge; otherwise perform manual review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-guardrail-bundled) <br>
- [README](README.md) <br>
- [Review payload schema](schemas/review-payload.schema.json) <br>
- [Redacted review payload example](examples/redacted-review-payload.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown instructions and JSON bridge responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires redacted JSON payloads and a user-approved localhost AANA bridge.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
