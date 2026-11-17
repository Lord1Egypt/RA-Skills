## Description:

Creates and saves original images, reference edits, transparent cutouts, upscales, and visual asset variations with DreamLayer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thedesignfounder](https://clawhub.ai/user/thedesignfounder)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to generate, edit, and download visual assets for product imagery, campaigns, print concepts, and game sprites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The DreamLayer server requires an API key.

Mitigation: Pass the key through the host's secret mechanism; do not put it in prompts or files.

Risk: Image generation consumes paid DreamLayer credits, including for large batches.

Mitigation: Confirm the budget and output count, check the live balance and price, and avoid automatic paid retries.

Risk: Generated images may contain incorrect details or be unsuitable for commercial publication.

Mitigation: Inspect saved assets and check applicable print specifications and legal clearances before publishing.

## Reference(s):

- [DreamLayer agent overview](https://dreamlayer.io/agent?utm_source=clawhub&utm_medium=agent_distribution&utm_campaign=agent_launch_202609)
- [DreamLayer Agent API reference](https://docs.dreamlayer.io/agent-api)
- [DreamLayer canonical workflows](https://github.com/TheDesignFounder/dreamlayer-agent-plugin)
- [DreamLayer workflow contract](https://github.com/TheDesignFounder/dreamlayer-agent-plugin/blob/main/docs/workflow-contract.md)

## Skill Output:

**Output Type(s):** [Files, Code, Guidance]

**Output Format:** [Downloaded image files or sprite sheets, with optional importer code and instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are saved to new paths in the working directory; generated assets need inspection before use.]

## Skill Version(s):

1.0.4 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
