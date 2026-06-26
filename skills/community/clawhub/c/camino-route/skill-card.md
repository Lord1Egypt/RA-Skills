## Description: <br>
Get detailed routing between two points with distance, duration, and optional turn-by-turn directions. Use when you need navigation instructions or travel time estimates between locations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request point-to-point route data, travel time estimates, turn-by-turn directions, and optional route geometry or imagery parameters from Camino's route API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route requests send precise start and end coordinates, and optionally street-level imagery parameters, to Camino's external API. <br>
Mitigation: Avoid exact home, workplace, or sensitive travel locations unless that disclosure is acceptable. <br>
Risk: The skill requires a CAMINO_API_KEY credential for authenticated API calls. <br>
Mitigation: Store the key in the agent environment and avoid pasting it into prompts, command history, or shared logs. <br>


## Reference(s): <br>
- [ClawHub Route skill page](https://clawhub.ai/james-southendsolutions/camino-route) <br>
- [Camino API key activation](https://app.getcamino.ai/skills/activate) <br>
- [x402 payment protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with shell examples and JSON route responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and CAMINO_API_KEY; route requests include start and end coordinates with optional travel mode, geometry, and imagery flags.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
