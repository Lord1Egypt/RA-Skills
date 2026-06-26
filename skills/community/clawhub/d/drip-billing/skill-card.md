## Description: <br>
Track AI agent usage and costs with Drip metered billing for aggregate LLM usage, tool calls, agent runs, and other metered usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-309](https://clawhub.ai/user/lucas-309) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to add Drip usage tracking to AI agents, LLM calls, tool invocations, API requests, and customer or workflow billing attribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends usage and billing telemetry to Drip, which may be inappropriate for environments that should not emit metered agent activity. <br>
Mitigation: Install only when billing telemetry is intended, and scope emitted meters, customers, workflows, and run events to the operational data required. <br>
Risk: Metadata fields are transmitted as provided and could expose raw prompts, secrets, PII, source code, or request bodies if misused. <br>
Mitigation: Use a strict metadata allowlist and redaction policy, and send only sanitized operational context such as model names, tool names, status codes, latency, and hashed identifiers. <br>
Risk: Over-privileged Drip API keys or an untrusted API base URL could broaden the impact of misuse. <br>
Mitigation: Prefer pk_test_ or pk_live_ keys, avoid sk_ keys unless admin operations are required, and keep DRIP_BASE_URL pointed at a trusted Drip endpoint. <br>


## Reference(s): <br>
- [Drip SDK API Reference](references/API.md) <br>
- [@drip-sdk/node npm package](https://www.npmjs.com/package/@drip-sdk/node) <br>
- [ClawHub release page](https://clawhub.ai/lucas-309/drip-billing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline TypeScript, Python, JSON, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DRIP_API_KEY and a trusted DRIP_BASE_URL for telemetry emission.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
