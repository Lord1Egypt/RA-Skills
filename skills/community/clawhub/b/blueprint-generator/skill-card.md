## Description:

Blueprint Generator helps agents generate Unreal Engine blueprint and material node graphs from natural language descriptions, screenshots, or imported JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical artists use this skill to create or inspect Unreal Engine blueprint and material node graphs from natural language descriptions, uploaded screenshots, or imported JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests may be sent to MiniMax for generation, including uploaded screenshots or blueprint details.

Mitigation: Avoid submitting private screenshots, proprietary blueprint details, secrets, or other sensitive inputs unless MiniMax provider and key usage are acceptable.

Risk: Generated Unreal Engine blueprint or material node structures may be incomplete or unsuitable for a project.

Mitigation: Review generated node graphs and JSON in Unreal Engine before using them in production content.

Risk: MiniMax service load, rate limits, or malformed generation output can interrupt generation.

Mitigation: Retry after a delay, reduce request frequency, or simplify the prompt when service or parsing errors occur.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/blueprint-generator)
- [MiniMax-hosted deployment](https://ncvbhgghna86.space.minimaxi.com)
- [MiniMax API gateway](https://api.minimaxi.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with inline commands and JSON node-graph structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Unreal Engine blueprint or material node rules, MiniMax model configuration notes, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog body state 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
