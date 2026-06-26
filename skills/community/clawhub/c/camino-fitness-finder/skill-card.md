## Description: <br>
Search for gyms, yoga studios, swimming pools, and sports facilities using Camino AI's location intelligence with AI-powered ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find nearby fitness facilities such as gyms, yoga studios, swimming pools, and sports venues from natural-language or coordinate-based searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fitness search terms and any provided latitude or longitude are sent to Camino. <br>
Mitigation: Use the skill only when sharing the search and location details with Camino is acceptable. <br>
Risk: The skill requires a Camino API key and consumes the user's Camino API quota. <br>
Mitigation: Keep CAMINO_API_KEY private, scope access to trusted environments, and monitor quota usage. <br>
Risk: The broader Camino suite includes companion skills beyond this fitness search workflow. <br>
Mitigation: Install the specific fitness-finder skill unless the companion skills are needed and have been reviewed. <br>


## Reference(s): <br>
- [ClawHub Fitness Finder release page](https://clawhub.ai/james-southendsolutions/camino-fitness-finder) <br>
- [Camino API activation](https://app.getcamino.ai/skills/activate) <br>
- [x402 payment protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON location-search results returned by a shell script or curl command, with Markdown usage guidance in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAMINO_API_KEY, curl, and jq; sends fitness search queries and optional coordinates to Camino.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
