## Description:

Trigger an Agent Token Audit via Botlington's A2A endpoint to audit an AI agent's token efficiency, identify model waste, context bloat, tool mismatches, and redundant work, and return a score, findings, and a prioritized remediation plan with estimated euro savings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gary-botlington](https://clawhub.ai/user/gary-botlington)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to submit AI-agent configuration details to Botlington for a token-efficiency audit. The service returns scoring, findings, prioritized remediation actions, and estimated savings to guide agent optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends agent configuration, prompts, schedules, tool lists, and audit answers to Botlington's external service.

Mitigation: Review and redact internal identifiers, credentials, personal data, and regulated information before submitting an audit.

Risk: The Botlington API key is required for paid audit requests and could authorize credit-consuming actions if exposed.

Mitigation: Store the API key in an environment variable or secrets manager and avoid placing it in prompts, source files, logs, or shared transcripts.

Risk: Audit findings and savings estimates may influence production agent changes.

Mitigation: Review recommendations before implementation and test changes against representative workloads before deployment.

## Reference(s):

- [Botlington A2A Endpoint](https://botlington.com/a2a)
- [Botlington Agent Card](https://botlington.com/.well-known/agent.json)
- [Sample Botlington Audit](https://botlington.com/audits/stripe)
- [ClawHub Skill Page](https://clawhub.ai/gary-botlington/skills/botlington-audit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit responses include a score, findings, priority actions, and estimated savings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
