## Description:

Fetches and analyzes Concept2 Logbook workout data via API with heart-rate zone analysis, weekly trend tracking, workout summaries, and training recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katla50](https://clawhub.ai/user/katla50)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and fitness-focused users use this skill to let an agent retrieve Concept2 Logbook workouts, summarize recent training, analyze heart-rate zones and trends, and generate recommendations from authenticated workout data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Concept2 Logbook API token and can expose personal profile and workout data.

Mitigation: Run it only on trusted machines, treat the token like a password, avoid logging or sharing token-bearing commands, and rotate the token if it is exposed.

Risk: JSON exports and summaries may contain personal fitness data.

Mitigation: Store exports only in appropriate locations, limit sharing, and delete generated files when they are no longer needed.

Risk: The broader API reference includes endpoints that can modify or delete Logbook records.

Mitigation: Use read-only workout retrieval unless the user explicitly requests a modifying action and understands the effect.

## Reference(s):

- [Concept2 Logbook API Reference](artifact/references/api-reference.md)
- [Concept2 developer documentation](https://log.concept2.com/developers/documentation/)
- [Concept2 API keys](https://log.concept2.com/developers/keys)
- [Concept2 API validator](https://log.concept2.com/developers/validator)
- [ClawHub skill page](https://clawhub.ai/katla50/skills/concept2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with optional JSON exports and inline shell or Python snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Concept2 Logbook API token; output may include personal profile and workout data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
