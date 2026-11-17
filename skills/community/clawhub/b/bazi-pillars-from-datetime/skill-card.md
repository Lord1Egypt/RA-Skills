## Description:

Use when a task involves deriving bazi chart data from Gregorian datetime and timezone, or generating a grounded user-language analysis from an existing chart JSON plus the local knowledge files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vastaq](https://clawhub.ai/user/vastaq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert Gregorian birth date, time, timezone, and location inputs into reproducible Bazi chart JSON, and to produce grounded user-language Markdown analysis from an existing chart and local knowledge files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location lookup can send user-provided location data to external geocoding providers.

Mitigation: Prefer supplying longitude and latitude directly, or force local-only lookup when external location disclosure is not acceptable.

Risk: Caller-controlled lookup and cache paths can cause writes to unintended writable files.

Mitigation: Run the skill with low filesystem privileges and restrict or remove caller-controlled cache_path and lookup_path support before deployment.

Risk: Geocoding provider API keys may be exposed if passed unnecessarily.

Mitigation: Avoid passing sensitive API keys unless online geocoding is required, and prefer local coordinates or local lookup for routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vastaq/skills/bazi-pillars-from-datetime)
- [Skill usage and contracts](artifact/SKILL.md)
- [Analysis prompt](artifact/prompt.md)
- [Bazi knowledge base](artifact/knowledge.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON for chart mode; Markdown for analysis mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chart mode returns structured success or error JSON; analysis mode follows the user's language and stays grounded in the supplied chart and local knowledge.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-03-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
