## Description: <br>
Retrieves decision-maker LinkedIn profiles and business email contacts for ecommerce store domains through the EcCompass API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roger52027](https://clawhub.ai/user/roger52027) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, sales teams, marketers, and ecommerce researchers use this skill to look up contact leads for a single store domain and review related EcCompass ecommerce intelligence when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is described as a contact lookup tool but the artifact also exposes broader ecommerce search, domain analytics, historical data, and installed-app queries. <br>
Mitigation: Review the schema and examples before installation and treat the skill as a broader EcCompass ecommerce intelligence API client. <br>
Risk: Returned contact information may include personal or business contact data used for prospecting. <br>
Mitigation: Use returned data only in compliance with applicable privacy, marketing, and platform rules, and avoid bulk or abusive outreach. <br>
Risk: The required APEX_TOKEN credential grants access to the EcCompass API. <br>
Mitigation: Store the token securely, avoid exposing it in logs or shared shell history, and rotate it if it may have been disclosed. <br>


## Reference(s): <br>
- [API Schema](references/schema.md) <br>
- [Usage Examples](references/examples.md) <br>
- [EcCompass AI](https://eccompass.ai) <br>
- [ClawHub Release Page](https://clawhub.ai/roger52027/ecommerce-lead-contacts) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and API-derived text or optional JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to api.eccompass.ai and an APEX_TOKEN credential.] <br>

## Skill Version(s): <br>
1.0.9 (source: frontmatter, claw.json, changelog, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
