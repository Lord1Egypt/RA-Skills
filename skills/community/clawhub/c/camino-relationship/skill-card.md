## Description: <br>
Calculate spatial relationships between two points including distance, direction, travel time, and human-readable descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit two latitude and longitude points to Camino and receive distance, direction, travel-time estimates, and a human-readable relationship summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided location pairs to Camino together with a Camino API key. <br>
Mitigation: Avoid submitting sensitive home, work, or personal-location pairs unless Camino processing is acceptable, and keep CAMINO_API_KEY protected. <br>
Risk: Installing the full Camino companion suite increases the reviewed surface beyond this relationship helper. <br>
Mitigation: Install only camino-relationship unless the companion skills have also been reviewed for the intended environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/camino-relationship) <br>
- [Camino API key activation](https://app.getcamino.ai/skills/activate) <br>
- [Camino relationship API endpoint](https://api.getcamino.ai/relationship) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [JSON API responses and Markdown usage guidance with bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and CAMINO_API_KEY; sends user-provided location pairs to Camino.] <br>

## Skill Version(s): <br>
2.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
