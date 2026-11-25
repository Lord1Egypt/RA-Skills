## Description:

Locate elementary schools, high schools, and universities near any address using Camino AI's location intelligence with AI-powered ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find nearby schools, high schools, colleges, and universities from an address, city, or coordinates through Camino AI location search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location searches are sent to Camino's remote API and may include sensitive home or child-related locations.

Mitigation: Avoid sending highly sensitive exact locations unless necessary and treat the skill as a remote API client.

Risk: The skill requires a Camino API key for authenticated requests.

Mitigation: Keep the API key scoped, revocable, and out of shared prompts, logs, and committed configuration.

Risk: Installation examples reference an unpinned source.

Mitigation: Install the specific school-finder skill from a version or commit the user trusts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/james-southendsolutions/skills/camino-school-finder)
- [Camino API Activation](https://app.getcamino.ai/skills/activate)
- [x402](https://x402.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and a CAMINO_API_KEY environment variable.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
