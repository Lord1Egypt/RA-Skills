## Description: <br>
Transforms text briefs or public HTTPS images into short gothic ritual-style videos with low-key lighting, candles, smoke, and black-gold-crimson styling using WeryAI Seedance 2.0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to expand short briefs into cinematic gothic prompts, submit text-to-video or single-image-to-video jobs to WeryAI Seedance 2.0, and return playable Markdown video links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, or other submitted assets are sent to the external WeryAI API. <br>
Mitigation: Do not submit secrets, private URLs, personal data, or confidential assets unless the user accepts sending them to WeryAI. <br>
Risk: Generation requests can consume paid WeryAI credits. <br>
Mitigation: Show the full prompt, model, duration, aspect ratio, resolution, audio setting, and image URL before submission and wait for user confirmation. <br>
Risk: The bundled CLI requires the caller to choose the intended model and does not enforce the skill's model lock by itself. <br>
Mitigation: Confirm that every request JSON uses model SEEDANCE_2_0 before approving execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/dark-ritual-transform-video-gen-seedance2-0) <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>
- [WeryAI video API host](https://api.weryai.com) <br>
- [WeryAI models registry host](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline video links, shell commands, and JSON status or error details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns WeryAI video URLs after polling; requires WERYAI_API_KEY, Node.js 18+, and public HTTPS image URLs for image-to-video.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
