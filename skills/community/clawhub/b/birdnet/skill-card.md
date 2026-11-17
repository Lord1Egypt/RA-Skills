## Description:

Query BirdNET-Go bird detections, view recent birds, search by species, and get detection details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rappo](https://clawhub.ai/user/rappo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query a trusted BirdNET-Go server for recent detections, species searches, detailed detection records, species information, and same-day activity summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries the BirdNET-Go server URL configured on the local machine.

Mitigation: Keep the configuration pointed at a trusted local BirdNET-Go instance before using the skill.

Risk: The configuration file may be treated as a place for connection details.

Mitigation: Do not store API keys or unrelated secrets in the BirdNET-Go config file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rappo/skills/birdnet)
- [Publisher profile](https://clawhub.ai/user/rappo)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with shell command examples and BirdNET-Go API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; reads BirdNET-Go server URL from ~/.clawdbot/credentials/birdnet/config.json and does not require an API key for local access.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
