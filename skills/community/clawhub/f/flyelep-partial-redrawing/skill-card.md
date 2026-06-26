## Description: <br>
Uses the Flyelep AI Tool API to partially redraw an image from a source image URL, a natural-language edit prompt, and an optional replacement reference image URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyelepai](https://clawhub.ai/user/flyelepai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to call Flyelep's partial image redrawing API for localized image edits, background replacement, or reference-guided region replacement while preserving the main subject. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends image URLs, edit prompts, optional reference image URLs, and a Flyelep API key to Flyelep. <br>
Mitigation: Avoid sensitive or private images unless third-party processing is acceptable, and provide the API key only at runtime. <br>
Risk: Saving the Flyelep secret key in shared files or examples could expose credentials. <br>
Mitigation: Keep the secret key out of skill files, repositories, and persistent configuration. <br>


## Reference(s): <br>
- [Flyelep partial redrawing API endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/partialRedrawing) <br>
- [Flyelep controlboard](https://www.flyelep.cn/controlboard) <br>
- [ClawHub skill page](https://clawhub.ai/flyelepai/flyelep-partial-redrawing) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API request guidance and returns or presents the redrawn image URL from Flyelep.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
