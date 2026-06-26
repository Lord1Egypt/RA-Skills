## Description: <br>
Routes agents through Chanjing workflows for credentials, TTS, voice cloning, digital-human video, lip-sync, AI image and video generation, customized-person training, one-click video assembly, and cartoon video creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binkes](https://clawhub.ai/user/binkes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create Chanjing media assets and videos through routed product and orchestration workflows. It is intended for Chanjing-backed content creation tasks such as speech synthesis, digital-human video, image/video generation, and short-video assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Chanjing APP_ID and SECRET_KEY values for authenticated media and account operations. <br>
Mitigation: Install only in trusted workspaces and keep credentials scoped to the intended process or project environment. <br>
Risk: Changing the Chanjing API base could redirect credentialed requests away from the official service. <br>
Mitigation: Keep CHANJING_API_BASE pointed at the official Chanjing API unless a trusted operator has explicitly approved another endpoint. <br>
Risk: Media workflows can write local outputs that may contain generated assets, account data, or user-provided content. <br>
Mitigation: Review output directories before sharing or syncing generated files. <br>
Risk: Some operations can delete custom digital people or start costly/non-interactive render jobs. <br>
Mitigation: Require explicit user confirmation before destructive account actions or expensive render workflows. <br>


## Reference(s): <br>
- [Chanjing Documentation](https://doc.chanjing.cc) <br>
- [ClawHub Skill Page](https://clawhub.ai/binkes/chanjing-content-creation-skill) <br>
- [Top-Level Runtime Contract](references/top-level-runtime-contract.md) <br>
- [Orchestration Contract](orchestration/orchestration-contract.md) <br>
- [One-Click Video Workflow Orchestration](orchestration/chanjing-one-click-video-creation/references/workflow-orchestration.md) <br>
- [One-Click Video Constraints and Limits](orchestration/chanjing-one-click-video-creation/references/constraints-and-limits.md) <br>
- [Chanjing Avatar Create Video API](products/chanjing-avatar/references/create-video-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls, files] <br>
**Output Format:** [Markdown guidance with JSON inputs, shell command invocations, API task results, URLs, and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference generated media, downloaded assets, workflow state files, and rendered video outputs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
