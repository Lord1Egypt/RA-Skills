## Description: <br>
Find cheap flights, monitor prices, and alert on price drops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and travel-focused agents use this skill to search Aerobase flight deal data, compare fare value, and create route price-watch alerts for meaningful price drops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creating alerts may set up ongoing route monitoring through Aerobase. <br>
Mitigation: Confirm route, date, price, and alert criteria before creating watches, and periodically list or remove alerts that are no longer needed. <br>
Risk: The skill requires an Aerobase API key. <br>
Mitigation: Install only when comfortable giving the agent an Aerobase API key, and redact raw keys from agent output. <br>


## Reference(s): <br>
- [Aerobase Homepage](https://aerobase.app) <br>
- [Aerobase OpenClaw Travel Agent](https://aerobase.app/openclaw-travel-agent) <br>
- [ClawHub Skill Page](https://clawhub.ai/kurosh87/aerobase-flight-deals) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, guidance] <br>
**Output Format:** [Concise Markdown summaries with route, travel window, fare, airline, jetlag score, recovery guidance, and follow-up actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AEROBASE_API_KEY for Aerobase API calls; agents should redact raw API keys in output.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release metadata; artifact frontmatter says 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
