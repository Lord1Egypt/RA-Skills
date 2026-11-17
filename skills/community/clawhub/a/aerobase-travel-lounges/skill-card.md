## Description:

Airport lounge access and recovery-support recommendations

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:

MIT

## Use Case:

External users and travel agents use this skill to find airport lounge options, compare amenities, and plan recovery-aware layovers using Aerobase API data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends airport lounge requests to Aerobase using a user-provided API key.

Mitigation: Set AEROBASE_API_KEY only in the agent environment, use the documented Authorization bearer header, and redact raw keys in output.

Risk: Users may provide passwords, OTPs, cookies, or third-party login details when asking for travel help.

Mitigation: Do not collect or request passwords, OTPs, cookies, or third-party logins; route users to Aerobase setup or account pages when authentication is needed.

Risk: Quota limits or API errors can prevent complete lounge results.

Mitigation: Explain 401, 403, 429, timeout, and 5xx conditions clearly, retry once on transient failures, and return partial guidance with next steps when needed.

## Reference(s):

- [Aerobase homepage](https://aerobase.app)
- [Aerobase OpenClaw travel agent setup](https://aerobase.app/openclaw-travel-agent)
- [ClawHub skill page](https://clawhub.ai/kurosh87/skills/aerobase-travel-lounges)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown recommendations with concise airport lounge options, amenities, recovery guidance, and API error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AEROBASE_API_KEY; free usage is capped at 5 requests/day.]

## Skill Version(s):

3.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
