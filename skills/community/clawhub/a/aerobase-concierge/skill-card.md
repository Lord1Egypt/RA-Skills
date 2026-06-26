## Description: <br>
Aerobase Concierge is an autonomous jetlag concierge that auto-scores flights, monitors deals, generates recovery plans, and guards itineraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External travelers and travel-focused agents use this skill to evaluate flight timing, monitor travel options, generate jetlag recovery plans, and present concise travel guidance with quantified tradeoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Aerobase API key and may share travel preferences or itinerary details with the Aerobase service. <br>
Mitigation: Use a revocable or scoped key where available, monitor API usage, and avoid sharing unnecessary loyalty or trip details. <br>
Risk: The skill can guide booking, purchase, cancellation, or account-change decisions. <br>
Mitigation: Require explicit user confirmation before any real booking, purchase, cancellation, or account change. <br>
Risk: Flight scores, deal monitoring, and recovery guidance may be incomplete or misleading if travel data is stale or user context is wrong. <br>
Mitigation: Review recommendations before acting and confirm itinerary, budget, loyalty, and chronotype details when the decision is material. <br>


## Reference(s): <br>
- [Aerobase Concierge on ClawHub](https://clawhub.ai/kurosh87/aerobase-concierge) <br>
- [Aerobase publisher profile](https://clawhub.ai/user/kurosh87) <br>
- [Aerobase API](https://aerobase.app/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell setup commands and structured JSON-render examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AEROBASE_API_KEY and may call the Aerobase API with travel context; responses can include structured data envelopes and rendered travel cards.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
