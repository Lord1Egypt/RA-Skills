## Description: <br>
Generate images, videos, and audio via fal.ai API (FLUX, SDXL, Whisper, etc.). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agmmnn](https://clawhub.ai/user/agmmnn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to submit fal.ai media generation and transcription jobs, poll queue status, and return generated media URLs or transcript results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a fal.ai API key and may consume paid credits when generation or transcription jobs are submitted. <br>
Mitigation: Use a dedicated or revocable key, monitor fal.ai credit usage, and configure credentials only in the intended environment. <br>
Risk: Prompts, image URLs, audio URLs, and generation parameters are sent to fal.ai for processing. <br>
Mitigation: Avoid submitting secrets, personal data, or regulated content unless fal.ai processing is acceptable for the deployment use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agmmnn/fal-ai) <br>
- [fal.ai API key dashboard](https://fal.ai/dashboard/keys) <br>
- [fal.ai queue API endpoint](https://queue.fal.run) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; runtime responses are JSON-derived text such as generated media URLs or transcript data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FAL_KEY and sends prompts, media URLs, and generation parameters to fal.ai.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
