## Description:

Generate 5-second cinematic AI videos using Kling via ComfyDeploy. Takes a character image, item image, and location image, then produces a character sheet, item sheet, and a short cinematic video showing them interacting. Use when creating short ads, film clips, music videos, or any scene where a character interacts with an item in a specific location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and production teams use this skill to turn character, item, and location images into short cinematic video concepts for ads, film clips, music videos, product demos, fashion scenes, and similar visual storytelling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented shell flow sources a local .env file as executable shell.

Mitigation: Provide COMFY_DEPLOY_API_KEY through a managed secret or existing environment variable, and avoid placing unrelated secrets in ~/clawd/.env.

Risk: User images and prompts are uploaded to ComfyDeploy and S3-backed storage.

Mitigation: Use only images and prompts that are acceptable to send to ComfyDeploy/S3 under the user's privacy, consent, and data-handling requirements.

Risk: Assigning character, item, and location images incorrectly can produce misleading or unusable video outputs.

Mitigation: Verify each supplied image with an image-identification tool before assigning character_base, item_base, and location_base.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pauldelavallaz/skills/cinematic-kling)
- [ComfyDeploy deployment queue API endpoint](https://api.comfydeploy.com/api/run/deployment/queue)
- [ComfyDeploy file upload API endpoint](https://api.comfydeploy.com/api/file/upload)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Code, Files]

**Output Format:** [Markdown guidance with shell and Python code blocks; generated image sheets and an MP4 video file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires COMFY_DEPLOY_API_KEY, uploads user-provided images and prompts to ComfyDeploy/S3, and typically takes about 3-5 minutes to produce results.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
