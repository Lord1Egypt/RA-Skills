## Description: <br>
Generate images and media using fal.ai API (Flux, Gemini image, etc.). Use when asked to generate images, run AI image models, create visuals, or anything involving fal.ai. Handles queue-based requests with automatic polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sxela](https://clawhub.ai/user/Sxela) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to submit fal.ai image, image-editing, and video-transformation jobs, validate model inputs, poll queued requests, and retrieve generated media results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images, videos, URLs, and possible audio selected by the user are sent to fal.ai for processing. <br>
Mitigation: Avoid submitting private, regulated, or sensitive media unless provider handling is acceptable for the use case. <br>
Risk: The skill requires a fal.ai API key and can read it from environment or local tool configuration. <br>
Mitigation: Use a revocable API key, prefer environment-based configuration, and avoid committing local tool configuration files. <br>
Risk: Asynchronous jobs may leave request metadata in local pending queue state. <br>
Mitigation: Clear fal-pending.json after sensitive jobs or when queued request tracking is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sxela/falai) <br>
- [Publisher profile](https://clawhub.ai/user/Sxela) <br>
- [Model schemas](references/models.json) <br>
- [fal.ai API keys](https://fal.ai/dashboard/keys) <br>
- [fal.ai queue API](https://queue.fal.run) <br>
- [fal.ai storage upload endpoint](https://fal.ai/api/storage/upload/initiate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, JSON request and response examples, and generated media URLs returned by fal.ai.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save local pending request state in fal-pending.json while asynchronous fal.ai jobs are in progress.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
