## Description:

Full jetlag intelligence suite with award search, comparison, recovery plans, and itinerary analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:


## Use Case:

External travelers and travel-planning agents use this skill to query Aerobase for jetlag-scored flight options, award availability, route intelligence, recovery plans, and itinerary risk analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends API keys and travel details, including itineraries and arrival commitments, to the Aerobase service.

Mitigation: Install only when that data sharing is acceptable, keep the API key scoped and private, and avoid submitting sensitive commitment details unless needed.

Risk: The artifact describes automatic recurring deal checks without clear opt-in, frequency, or stop controls.

Mitigation: Use deal monitoring only with explicit user consent, a stated check frequency, and a clear way to disable further checks.

## Reference(s):

- [Aerobase API](https://aerobase.app/api)
- [ClawHub Skill Page](https://clawhub.ai/kurosh87/skills/aerobase-travel-pro)
- [Publisher Profile](https://clawhub.ai/user/kurosh87)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and summarized API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an Aerobase API key and returns jetlag scores, recovery estimates, route or itinerary analysis, award search details, and travel recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
