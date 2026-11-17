## Description:

Jetlag recovery optimization - score flights, generate recovery plans, optimize travel timing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:

MIT

## Use Case:

External users and travel-focused agents use this skill to score flight jetlag impact, generate recovery plans, and choose timing or routine adjustments for same-day travel recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends relevant travel and recovery-planning details to the Aerobase API.

Mitigation: Use it only when sharing those details with Aerobase is acceptable, and provide only the information needed for flight scoring or recovery planning.

Risk: API keys or unrelated credentials could be exposed if users provide secrets directly.

Mitigation: Use the AEROBASE_API_KEY environment variable, redact API keys in output, and do not provide passwords, OTPs, cookies, or third-party login sessions.

Risk: Recovery advice could be mistaken for medical or dosing guidance.

Mitigation: Keep recommendations practical and travel-oriented, and avoid unsafe medical or dosing instructions.

## Reference(s):

- [Aerobase homepage](https://aerobase.app)
- [Aerobase OpenClaw travel agent setup](https://aerobase.app/openclaw-travel-agent)
- [ClawHub skill page](https://clawhub.ai/kurosh87/skills/aerobase-jetlag)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown]

**Output Format:** [Markdown with concise travel scoring and recovery guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AEROBASE_API_KEY and Aerobase API endpoints for flight scoring and recovery planning.]

## Skill Version(s):

3.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
