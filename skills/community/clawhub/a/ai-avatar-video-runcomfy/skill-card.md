## Description:

This skill helps an agent route avatar, talking-head, and lip-sync video requests to RunComfy models and produce the matching RunComfy CLI commands, prompts, and input payloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and agents use this skill to turn portraits, scripts, voiceovers, and reference media into avatar or talking-head video workflows on RunComfy. It provides model selection guidance and ready-to-run CLI examples for lip-sync, script-to-video, cinematic monologues, and stylized character animation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned CLI installation can run a newer @runcomfy/cli version than the reviewer assessed.

Mitigation: Pin or review the @runcomfy/cli version before installation, avoid unattended npx -y execution, and run the workflow in a constrained environment.

Risk: RunComfy token exposure could allow unauthorized API use.

Mitigation: Limit access to RUNCOMFY_TOKEN and ~/.config/runcomfy, rotate tokens if exposure is suspected, and provide only the media files needed for the task.

Risk: Avatar and lip-sync generation can misuse a person's likeness or voice.

Mitigation: Use only portraits, voices, and reference media that the user has rights to use, and refuse requests involving non-consensual real-person impersonation or harmful synthetic media.

Risk: Reference media may steer generation away from the requested prompt.

Mitigation: Use only user-provided reference URLs and treat unexpected generation behavior as a reason to inspect or replace the reference asset.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/ai-avatar-video-runcomfy)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy)
- [RunComfy lip-sync feature](https://www.runcomfy.com/models/feature/lip-sync?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy)
- [ByteDance OmniHuman API](https://www.runcomfy.com/models/bytedance/omnihuman/api?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy)
- [Wan 2-7 model](https://www.runcomfy.com/models/wan-ai/wan-2-7?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy)
- [Wan 2-2 Animate API](https://www.runcomfy.com/models/community/wan-2-2-animate/api?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy)
- [HappyHorse 1.0 text-to-video](https://www.runcomfy.com/models/happyhorse/happyhorse-1-0/text-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy)
- [Seedance v2 Pro](https://www.runcomfy.com/models/bytedance/seedance-v2/pro?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy)
- [RunComfy video models](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar-video-runcomfy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs model-routing guidance, RunComfy CLI invocations, prompting patterns, and required environment/configuration notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
