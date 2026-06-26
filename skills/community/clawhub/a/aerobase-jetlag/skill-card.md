## Description: <br>
Jetlag recovery optimization - score flights, generate recovery plans, optimize travel timing <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and travel-planning agents use this skill to score flight jetlag impact, generate recovery plans, and choose practical timing or itinerary adjustments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Aerobase API key, which could be exposed if pasted into chat or printed in responses. <br>
Mitigation: Store the key in AEROBASE_API_KEY, do not ask users to paste secrets, and redact any displayed key material. <br>
Risk: Jetlag scoring and recovery plans require sending travel details to Aerobase. <br>
Mitigation: Use the skill only when users are comfortable sharing the needed itinerary details with Aerobase. <br>
Risk: Advertised Pro Gmail import and calendar sync features may request account permissions beyond basic API scoring. <br>
Mitigation: Review requested permissions, privacy policy, and data retention controls before enabling Gmail import or calendar sync. <br>
Risk: Recovery advice could be mistaken for medical or dosing guidance. <br>
Mitigation: Keep plans practical and avoid unsafe medical or dosing recommendations. <br>


## Reference(s): <br>
- [Aerobase homepage](https://aerobase.app) <br>
- [Aerobase OpenClaw travel agent setup](https://aerobase.app/openclaw-travel-agent) <br>
- [ClawHub skill page](https://clawhub.ai/kurosh87/aerobase-jetlag) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls] <br>
**Output Format:** [Markdown text with API request guidance and concise action lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the AEROBASE_API_KEY environment variable and should redact raw API keys in output.] <br>

## Skill Version(s): <br>
3.3.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
