## Description: <br>
Provides 48-zodiac personality analysis and two-person compatibility readings from month-day birthdate inputs or 48-Zodiac IDs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niukesi](https://clawhub.ai/user/niukesi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve astrology-style 48-zodiac profile readings and compatibility reports while collecting only the month and day needed for lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Month-day birthday inputs are sent to the skill's remote API. <br>
Mitigation: Ask only for month and day, avoid birth year or unrelated personal data, and do not submit another person's birthday without permission. <br>
Risk: Remote API retention, logging, and sharing practices are not documented in the supplied evidence. <br>
Mitigation: Do not treat submitted birthdate inputs as private unless the publisher documents those practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/niukesi/48-zodiac-cyber-reader) <br>
- [Publisher profile](https://clawhub.ai/user/niukesi) <br>
- [Artifact README](artifact/README.md) <br>
- [OpenAPI specification](artifact/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown conversational responses grounded in JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated from remote zodiac profile or pairing lookups using month-day birthdate strings or 48-Zodiac IDs.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
