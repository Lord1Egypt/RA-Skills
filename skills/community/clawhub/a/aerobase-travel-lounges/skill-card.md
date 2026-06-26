## Description: <br>
Airport lounge access and recovery-support recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External travel agents and travel-planning assistants use this skill to find airport lounge options, compare amenities, and provide recovery-aware layover guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dedicated Aerobase API key and sends airport or lounge search details to Aerobase. <br>
Mitigation: Keep the API key in the agent environment, redact keys from output, and avoid sharing unrelated itinerary, account, password, OTP, cookie, or third-party login details. <br>
Risk: Frequent use may consume quota or incur billing on paid tiers. <br>
Mitigation: Monitor quota or billing and handle rate limits by explaining the free-tier cap and upgrade options. <br>


## Reference(s): <br>
- [Aerobase homepage](https://aerobase.app) <br>
- [Aerobase OpenClaw travel agent setup](https://aerobase.app/openclaw-travel-agent) <br>
- [ClawHub skill page](https://clawhub.ai/kurosh87/aerobase-travel-lounges) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kurosh87) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Concise recommendations with top lounge options first and one or two follow-up actions.] <br>

## Skill Version(s): <br>
3.3.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
