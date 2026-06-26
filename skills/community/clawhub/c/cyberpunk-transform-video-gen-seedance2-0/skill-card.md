## Description: <br>
Re-skins everyday clip concepts into neon-drenched, high-tech urban future videos using WeryAI Seedance 2.0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to transform text briefs or public HTTPS image URLs into cyberpunk-styled short videos through WeryAI Seedance 2.0. The skill expands prompts, confirms generation parameters, runs the bundled CLI, and returns playable video links or clear failure details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a WeryAI API key and paid generation authority. <br>
Mitigation: Install it only when the publisher is trusted, keep WERYAI_API_KEY in the runtime environment rather than files, and use a scoped or isolated account where possible. <br>
Risk: Generation calls may consume credits, and re-running the wait command creates new paid tasks. <br>
Mitigation: Review the confirmation table before each run and confirm duration, resolution, audio, prompt, and image URL before submitting. <br>
Risk: Prompts and public image URLs are sent to WeryAI and may contain sensitive or proprietary content. <br>
Mitigation: Do not include secrets, private URLs, personal data, or proprietary media unless sharing that content with WeryAI is authorized. <br>
Risk: The bundled script requires a model parameter but does not enforce this skill's allowed model. <br>
Mitigation: Set and confirm "model":"SEEDANCE_2_0" for every generation request. <br>


## Reference(s): <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/cyberpunk-transform-video-gen-seedance2-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline links, confirmation tables, and shell commands using JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, paid network access to WeryAI, public HTTPS image URLs for image-to-video, and SEEDANCE_2_0 as the confirmed model.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
