## Description: <br>
Locate elementary schools, high schools, and universities near any address using Camino AI's location intelligence with AI-powered ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find nearby elementary schools, high schools, colleges, and universities from an address, coordinates, or school-type query. It is useful for neighborhood research, school proximity checks, and combining school search results with other Camino location workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: School searches may include home addresses, precise coordinates, or child-related location context sent to an external API. <br>
Mitigation: Review inputs before execution, avoid unnecessary personal or child-identifying details, and confirm Camino's privacy handling before using sensitive locations. <br>
Risk: The skill requires a CAMINO_API_KEY and performs network requests with curl. <br>
Mitigation: Store the API key in the agent environment rather than prompts or logs, restrict who can run the skill, and review outbound requests before deployment. <br>


## Reference(s): <br>
- [School Finder on ClawHub](https://clawhub.ai/james-southendsolutions/camino-school-finder) <br>
- [Camino API key activation](https://app.getcamino.ai/skills/activate) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses from the Camino API, with Markdown usage examples and shell commands in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAMINO_API_KEY plus curl and jq. Sends school-search queries, coordinates, radius, and limit parameters to the external Camino API.] <br>

## Skill Version(s): <br>
2.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
