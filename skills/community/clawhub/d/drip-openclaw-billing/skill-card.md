## Description: <br>
Add usage metering and billing telemetry to OpenClaw agents using Drip. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-309](https://clawhub.ai/user/lucas-309) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to instrument OpenClaw agents with Drip run timelines, tool-call usage metering, and customer-level billing attribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telemetry metadata may expose sensitive prompts, outputs, credentials, personal data, or raw request data if integration code sends unsanitized fields. <br>
Mitigation: Use least-privilege telemetry keys and send only sanitized metadata; avoid raw prompts, model outputs, credentials, personal data, and raw request or response bodies. <br>
Risk: Billing records may duplicate or misstate usage under retries or incorrect meter configuration. <br>
Mitigation: Use stable idempotency keys and validate meters, run lifecycle events, and retry behavior in staging before production. <br>


## Reference(s): <br>
- [Drip OpenClaw Billing API Reference](references/API.md) <br>
- [ClawHub skill page](https://clawhub.ai/lucas-309/drip-openclaw-billing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, TypeScript, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance focuses on Drip telemetry setup, environment variables, API usage, idempotency, and privacy-safe metadata handling.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
