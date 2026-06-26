## Description: <br>
Locate parking garages, lots, and street parking near your destination using Camino AI's location intelligence with AI-powered ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find parking garages, lots, and street parking near destinations or coordinates through Camino's location API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided parking searches, destinations, and optional coordinates to Camino's API. <br>
Mitigation: Avoid sending precise destinations or coordinates unless the user is comfortable sharing that location data with Camino. <br>
Risk: The skill requires a Camino API key and can use paid Camino endpoints. <br>
Mitigation: Use a Camino API key with spending and usage limits that match the deployment's risk tolerance. <br>
Risk: The skill depends on local shell execution with curl and jq. <br>
Mitigation: Install and run it only in environments where those binaries and outbound requests to Camino are expected and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/camino-parking-finder) <br>
- [Camino API key activation](https://app.getcamino.ai/skills/activate) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and CAMINO_API_KEY; shell script returns JSON from Camino's query API.] <br>

## Skill Version(s): <br>
2.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
