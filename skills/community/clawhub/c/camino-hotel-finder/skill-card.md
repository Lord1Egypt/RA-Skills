## Description: <br>
Search for hotels, hostels, and lodging near landmarks, conference venues, or neighborhoods using Camino AI's location intelligence with AI-powered ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find hotels, hostels, and lodging near landmarks, venues, neighborhoods, airports, or cities. It sends the lodging search to Camino AI and returns ranked location results with a human-readable answer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lodging searches may include addresses, itinerary details, or other travel context that is sent to Camino AI. <br>
Mitigation: Avoid submitting confidential addresses, private itineraries, or sensitive travel plans unless the user is comfortable sharing them with Camino AI. <br>
Risk: The skill requires a Camino API key and calls an external Camino API endpoint. <br>
Mitigation: Use a dedicated Camino API key where possible, keep it private, and review the command before execution. <br>
Risk: Installing the full Camino skill suite expands the amount of code and behavior in scope. <br>
Mitigation: Install the specific hotel-finder skill unless the other Camino skills have also been reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/james-southendsolutions/camino-hotel-finder) <br>
- [Camino API Key Activation](https://app.getcamino.ai/skills/activate) <br>
- [x402 Payment Protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands] <br>
**Output Format:** [JSON lodging search results with an answer field] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAMINO_API_KEY plus curl and jq; accepts a JSON query with optional latitude, longitude, radius, and limit.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
