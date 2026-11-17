## Description:

Query vehicle location and condition information, including lock, door, window, and air-conditioning status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouzidan](https://clawhub.ai/user/zhouzidan)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Tika Digital Key-equipped vehicles use this skill to query current vehicle location and vehicle condition after App binding and API-key setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve sensitive vehicle location and physical-status data.

Mitigation: Install only when the user trusts the Tika/OpenAPI service, and confirm each request is intended before querying or sharing results.

Risk: API keys may be exposed through agent conversation, shell history, or local credential cache.

Mitigation: Prefer TIKA_API_KEY set outside the agent conversation, avoid --apikey in command history, and clear ~/.skill_carkey_cache.json when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouzidan/skills/car-key)
- [Tika official website](https://www.tikakey.com/)
- [Chengqu official website](https://www.chengqukey.com/)
- [Tika OpenAPI condition endpoint](https://openapi.nokeeu.com/iot/v1/condition)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with CLI commands and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese or English CLI output and position-only, condition-only, summary, detail, and raw JSON modes.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
