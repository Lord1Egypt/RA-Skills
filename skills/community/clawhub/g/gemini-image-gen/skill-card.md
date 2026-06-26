## Description: <br>
Generate and edit images via the Google Gemini API with Gemini native generation, Imagen 3, style presets, batch runs, and an HTML gallery output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IISweetHeartII](https://clawhub.ai/user/IISweetHeartII) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and creative agents use this skill to generate, edit, batch, and review images from text prompts or input images using a Gemini API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected edit images are sent to Google using the user's Gemini API key. <br>
Mitigation: Avoid confidential prompts or files, restrict edit inputs to intended image paths, and use an API key with appropriate account and budget controls. <br>
Risk: Heartbeat guidance encourages optional social posting, avatar changes, and memory saving without explicit approval controls. <br>
Mitigation: Require explicit user approval, account scope, budget limits, and retention rules before enabling posting, avatar updates, or memory persistence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/IISweetHeartII/gemini-image-gen) <br>
- [Google AI Studio API key setup](https://aistudio.google.com/apikey) <br>
- [OpenClaw](https://openclaw.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Files, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; generated runs produce PNG files, prompts.json, and an HTML gallery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and GEMINI_API_KEY; image editing sends the selected input image and prompt to Google Gemini APIs.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
