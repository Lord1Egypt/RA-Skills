## Description: <br>
Transforms text briefs or a single public image URL into epic cinematic WeryAI Seedance 2.0 video generations and returns playable video links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn text briefs or public HTTPS image URLs into trailer-style vertical or social videos through WeryAI Seedance 2.0. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a WeryAI API key and submits prompts or image URLs to WeryAI. <br>
Mitigation: Install only if you trust the publisher, keep WERYAI_API_KEY secret, and use an isolated or short-lived environment for higher assurance. <br>
Risk: Video generation and reruns can consume paid WeryAI credits. <br>
Mitigation: Review the expanded prompt, image URL, model, duration, aspect ratio, resolution, and audio setting before confirming each run. <br>
Risk: The bundled CLI accepts a model parameter while this release is scoped to SEEDANCE_2_0. <br>
Mitigation: Confirm that every request uses model SEEDANCE_2_0 and only the allowed duration, aspect ratio, and resolution values before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/epic-cinematic-transform-video-gen-seedance2-0) <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with confirmation details, inline shell commands, JSON responses, and video links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns playable video URLs when generation succeeds; requires WERYAI_API_KEY and may consume paid credits.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
