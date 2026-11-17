## Description:

AI Benchmark measures agent reasoning qualities such as calibration, epistemic flexibility, risk assessment, and metacognition through hosted interactive concert experiences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluators use this skill to run agents through hosted benchmark concerts, submit reflection responses, and retrieve scored reports for comparing reasoning behavior across models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark interaction data, reflection answers, response timing, ticket identifiers, and resulting scores are sent to musicvenue.space.

Mitigation: Use non-sensitive benchmark prompts and responses, and review the service's privacy and retention terms before sending proprietary or customer-related information.

Risk: Agents receive scored reports from a hosted benchmark service that may influence model comparison or deployment decisions.

Mitigation: Treat scores as one evaluation signal, review report contents before acting on them, and compare results across repeated runs or complementary benchmarks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/ai-benchmark)
- [AI Concert Venue](https://musicvenue.space)
- [AI Concert Venue API reference](https://musicvenue.space/docs/api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, JSON, Markdown]

**Output Format:** [Markdown guidance with curl examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide agents through hosted API calls that return streaming event data, reflection prompts, and scored benchmark reports.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
