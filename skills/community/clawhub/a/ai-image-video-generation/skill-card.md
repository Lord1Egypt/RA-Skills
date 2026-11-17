## Description:

Generate images and videos using the VibeVideo API for image or video creation, generation status checks, model selection, and credit cost calculation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytevirts](https://clawhub.ai/user/bytevirts)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to create AI images or videos through VibeVideo, check asynchronous generation status, cancel tasks, choose supported models, and estimate credit costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and referenced image URLs may be sent to VibeVideo with an API key.

Mitigation: Avoid secrets, sensitive content, and private URLs in prompts or generation options unless the user has approved sending them to VibeVideo.

Risk: Generation requests can consume paid VibeVideo credits.

Mitigation: Use the cost calculation workflow before generation when cost matters, and confirm expensive or repeated generation requests with the user.

Risk: Canceling a task is a state-changing API action.

Mitigation: Treat task cancellation as an explicit user-directed action and confirm the target task ID before issuing the DELETE request.

Risk: The skill requires a sensitive VIBEVIDEO_API_KEY environment variable.

Mitigation: Read the API key only from the environment and do not echo, log, or include it in generated output.

## Reference(s):

- [VibeVideo](https://vibevideo.app)
- [ClawHub skill page](https://clawhub.ai/bytevirts/skills/ai-image-video-generation)
- [Publisher profile](https://clawhub.ai/user/bytevirts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces VibeVideo API request guidance, task status interpretation, media URL reporting, and error handling advice.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
