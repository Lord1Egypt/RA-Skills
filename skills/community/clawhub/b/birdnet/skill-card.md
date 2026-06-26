## Description: <br>
Query BirdNET-Go bird detections. View recent birds, search by species, get detection details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rappo](https://clawhub.ai/user/rappo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query a BirdNET-Go instance for recent detections, species searches, detection details, species information, and daily bird activity summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Detection queries sent over plain HTTP can expose species, timestamps, weather, and query activity on the network path. <br>
Mitigation: Configure the BirdNET-Go URL to a trusted endpoint you control, preferring localhost or HTTPS where available. <br>
Risk: The skill reads bird detection records from the configured BirdNET-Go instance. <br>
Mitigation: Install and enable it only when the agent should have access to that local detection history. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; reads BirdNET-Go URL from ~/.clawdbot/credentials/birdnet/config.json when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
