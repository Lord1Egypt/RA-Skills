## Description:

Transforms everyday text prompts or one public HTTPS image into fantasy-style vertical videos using WeryAI Seedance 2.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn short scene briefs or a single reference image into magical, ritual-rich short videos. The agent expands the prompt, confirms Seedance 2.0 parameters, runs the WeryAI video CLI, and returns playable video links or clear failure details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the bundled CLI can perform broader paid WeryAI API actions than the Seedance-only fantasy workflow advertises.

Mitigation: Review the confirmation table before execution and verify the request uses model SEEDANCE_2_0 with the documented duration, aspect ratio, resolution, and audio settings.

Risk: Generation requires WERYAI_API_KEY and may consume WeryAI credits for submitted jobs.

Mitigation: Keep WERYAI_API_KEY out of files, use a scoped or short-lived environment when possible, and confirm generation settings before submitting a paid task.

Risk: Prompts and image inputs are sent to WeryAI, and image inputs must be public HTTPS URLs.

Mitigation: Use only non-sensitive prompts and public image URLs that are acceptable to share with the service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zoucdr/skills/fantasy-transform-video-gen-seedance2-0)
- [WeryAI Video API Reference](artifact/resources/WERYAI_VIDEO_API.md)
- [WeryAI Video Task API Host](https://api.weryai.com)
- [WeryAI Models Registry API Host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown with inline video links, confirmation tables, shell commands, and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns playable video URLs when generation completes; otherwise returns structured failure details from the WeryAI CLI.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
