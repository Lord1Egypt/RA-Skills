## Description:

Generate images using Draw Things app via dt-skill CLI or MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mijuu](https://clawhub.ai/user/mijuu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to generate Draw Things images through the preferred MCP generate_image tool or the dt-skill CLI fallback, including prompt, model, resolution, and upscaling parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install an unpinned global third-party npm package if the helper CLI is missing.

Mitigation: Review or pin the package version before installation and avoid sudo or administrator-level installation.

Risk: The skill can ask agents to change local Draw Things paths or start long-running upscaling jobs.

Mitigation: Confirm path changes and long upscaling jobs with the user before execution, and use explicit timeouts for heavy runs.

## Reference(s):

- [Drawthings Agent ClawHub page](https://clawhub.ai/mijuu/skills/drawthings-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and tool-call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for local Draw Things server and model paths; image generation can take up to 600 seconds by default or 1200 seconds for heavy 4x upscales.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
