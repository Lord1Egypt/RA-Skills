## Description: <br>
AI agent self-portrait generator. Create avatars, profile pictures, and visual identity using Gemini image generation. Supports mood-based generation, seasonal themes, and automatic style evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IISweetHeartII](https://clawhub.ai/user/IISweetHeartII) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw agent operators use this skill to generate avatar, banner, and full-body visual identity assets from personality, mood, theme, and format settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Avatar prompts and personality or style details are sent to Gemini during image generation. <br>
Mitigation: Use non-sensitive personality inputs and avoid passing private files through --personality. <br>
Risk: The Gemini API key can be exposed if placed in public files or readable automation commands. <br>
Mitigation: Keep GEMINI_API_KEY in a private environment or secret store and avoid embedding it in shared cron lines. <br>
Risk: Generated images could be used to update a public account avatar without sufficient review. <br>
Mitigation: Require explicit approval before applying generated images to public profiles. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/IISweetHeartII/agent-selfie) <br>
- [Publisher profile](https://clawhub.ai/user/IISweetHeartII) <br>
- [Agent Selfie repository](https://github.com/IISweetHeartII/agent-selfie) <br>
- [Google AI Studio API key](https://aistudio.google.com/apikey) <br>
- [OpenClaw](https://openclaw.org) <br>


## Skill Output: <br>
**Output Type(s):** [files, images, text, shell commands, configuration] <br>
**Output Format:** [PNG images with prompts.json, an HTML gallery, and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and GEMINI_API_KEY; supports avatar, banner, and full-body formats plus mood and theme presets.] <br>

## Skill Version(s): <br>
1.2.1 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
