## Description: <br>
Creates talking-head and lip-sync avatar videos through the RunComfy CLI, routing requests across OmniHuman, Wan 2-7, HappyHorse, Seedance v2 Pro, and Wan 2-2 Animate based on the user's inputs and intent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to choose an appropriate RunComfy avatar-video route and produce documented `runcomfy run` commands for talking-head, lip-sync, virtual-presenter, and stylized-character video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Avatar and lip-sync workflows can misuse a person's likeness or voice. <br>
Mitigation: Use only portraits, voices, and reference media the user has permission to process, and refuse requests involving real people without consent or harmful synthetic media. <br>
Risk: The RUNCOMFY_TOKEN credential can grant access to RunComfy services if exposed. <br>
Mitigation: Keep RUNCOMFY_TOKEN private, prefer secure environment or config storage, and avoid printing or committing token values. <br>
Risk: Generated runcomfy commands may upload face, voice, or reference media to external RunComfy endpoints. <br>
Mitigation: Review generated commands before execution and confirm the media, URLs, and output paths match the user's intent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/ai-avatar-video-runcomfy) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy) <br>
- [RunComfy lip-sync feature](https://www.runcomfy.com/models/feature/lip-sync?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy) <br>
- [OmniHuman model page](https://www.runcomfy.com/models/bytedance/omnihuman/api?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy) <br>
- [Wan 2-7 model page](https://www.runcomfy.com/models/wan-ai/wan-2-7?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy) <br>
- [Wan 2-2 Animate model page](https://www.runcomfy.com/models/community/wan-2-2-animate/api?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy) <br>
- [RunComfy character-swap feature](https://www.runcomfy.com/models/feature/character-swap?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy) <br>
- [RunComfy video models](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON input snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces RunComfy model-selection guidance and CLI invocations; the generated video files are produced by RunComfy services outside the skill.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
