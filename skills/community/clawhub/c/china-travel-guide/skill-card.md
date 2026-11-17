## Description:

China Travel Guide is a travel assistant for foreign visitors to China, covering trip preparation, visa guidance, transportation, payment support, translation, itinerary planning, and emergency help.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1970168137](https://clawhub.ai/user/1970168137)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to prepare China trips, troubleshoot payments and transportation, generate practical translation cards, and find emergency guidance while in China.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contains time-sensitive travel data, including visa rules, transport prices, emergency contacts, hospital details, and app or payment limits.

Mitigation: Verify those details with official or current sources before travel or before presenting them as final operational guidance.

Risk: Broad triggers such as help, emergency, or translate this could cause the skill to be used outside its intended China travel scope.

Mitigation: Confirm the user is asking about China-specific travel needs before relying on this skill.

Risk: The security evidence says the skill is not a general emergency, navigation, or translation skill.

Mitigation: Use it as a China-specific travel assistant and escalate emergencies, navigation, and legal or consular questions to current official resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1970168137/skills/china-travel-guide)
- [Visa policies data](data/visa-policies.json)
- [Emergency contacts data](data/emergency-contacts.json)
- [Travel phrases data](data/phrases.json)
- [Signature routes data](data/routes.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown travel guidance with checklists, tables, dialogue cards, and concise action steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on web search and image analysis tools when available; time-sensitive travel information should be verified against official or current sources.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
