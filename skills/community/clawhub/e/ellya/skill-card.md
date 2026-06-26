## Description: <br>
OpenClaw virtual companion skill that bootstraps character setup, learns and stores visual styles from uploaded photos, generates selfies from prompts or saved styles, and creates multi-image photo series. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laogiant](https://clawhub.ai/user/laogiant) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and skill handlers use Ellya to set up a virtual companion persona, collect user-provided appearance and style references, generate personalized images, and send generated media back through the OpenClaw runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded photos, generated images, base appearance files, and saved style notes may contain sensitive or identifying information. <br>
Mitigation: Use only photos the user is comfortable storing locally, avoid private or identifying images, and add clear retention and deletion steps before deployment. <br>
Risk: Photo analysis prompts ask for detailed body and identifying visual characteristics. <br>
Mitigation: Obtain explicit user consent before analyzing personal photos and limit analysis to style details needed for the requested generation. <br>
Risk: Selected photos and prompts are sent to Google GenAI for analysis and generation. <br>
Mitigation: Disclose this external processing path to users and avoid submitting sensitive photos or prompts unless the user accepts that handling. <br>
Risk: Generated media can be sent through OpenClaw to a channel and target. <br>
Mitigation: Confirm the recipient context before sending generated images and provide a fallback when the OpenClaw CLI is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laogiant/ellya) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Analysis prompt](artifact/ANALYSIS_PROMPT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved under output/ and learned style notes are saved under styles/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
