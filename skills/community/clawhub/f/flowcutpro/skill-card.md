## Description: <br>
AI-powered cinematic video production using Google Veo 3 as the renderer and OpenClaw's configured LLM for shot planning, prompt engineering, style consistency, and quality review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windseeker1111](https://clawhub.ai/user/windseeker1111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and content-production teams use FlowCutPro to turn a text concept into a multi-shot cinematic video workflow with planned shots, Veo 3 prompts, rendered clips, and ffmpeg stitching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The evidence security summary reports an embedded API key and material credential-handling concerns. <br>
Mitigation: Remove the embedded key before installing or running the skill, then configure a restricted VEO_API_KEY through a secure environment or secret manager. <br>
Risk: The skill sends prompts and generated shot details to external AI providers. <br>
Mitigation: Avoid confidential, regulated, or unreleased concepts unless the operator has approved use of the relevant external providers and data flows. <br>
Risk: The evidence security verdict is suspicious because provider and credential-handling risks are under-disclosed. <br>
Mitigation: Review the skill carefully before installation, document external-service dependencies for users, and run only after credential handling is corrected. <br>


## Reference(s): <br>
- [FlowCutPro ClawHub listing](https://clawhub.ai/windseeker1111/flowcutpro) <br>
- [Publisher profile](https://clawhub.ai/user/windseeker1111) <br>
- [Google AI Studio API keys](https://aistudio.google.com/apikeys) <br>
- [Google Generative Language Veo endpoint](https://generativelanguage.googleapis.com/v1beta/models/veo-3.1-generate-preview:predictLongRunning) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance, JSON shot plans, shell commands, and generated MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include per-shot MP4 clips and a stitched final video in the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
