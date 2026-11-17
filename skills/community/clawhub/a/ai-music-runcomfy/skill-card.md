## Description:

Generates and edits AI music through the RunComfy CLI by routing user intent to ElevenLabs Music or ACE Step text-to-audio, inpaint, and outpaint endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, creators, and agent operators use this skill to generate new music or edit existing tracks with RunComfy-hosted audio models. It helps select a suitable model route, prepare the required JSON inputs, and produce CLI-ready commands for vocal, instrumental, multilingual, inpaint, and outpaint workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or run an unpinned external RunComfy CLI that handles account tokens and can make billable network calls.

Mitigation: Use a pinned, reviewed CLI version where possible, avoid unattended `npx -y` execution, limit file and environment access to what the run needs, and confirm cost-sensitive jobs before execution.

Risk: Prompts, lyrics, audio URLs, and generated outputs are processed through RunComfy and may include sensitive or rights-managed material.

Mitigation: Submit only content the user is authorized to use, keep `RUNCOMFY_TOKEN` out of prompts and logs, and use only task-specific user-provided audio URLs for edit workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/ai-music-runcomfy)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-music-runcomfy)
- [RunComfy audio model catalog](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-music-runcomfy)
- [ElevenLabs Music Generation on RunComfy](https://www.runcomfy.com/models/elevenlabs/elevenlabs/music-generation?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-music-runcomfy)
- [ACE Step text-to-audio on RunComfy](https://www.runcomfy.com/models/acestep-ai/ace-step/text-to-audio?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-music-runcomfy)
- [ACE Step 1.5 text-to-audio on RunComfy](https://www.runcomfy.com/models/acestep-ai/ace-step-1.5/text-to-audio?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-music-runcomfy)
- [ACE Step audio-inpaint on RunComfy](https://www.runcomfy.com/models/acestep-ai/ace-step/audio-inpaint?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-music-runcomfy)
- [ACE Step audio-outpaint on RunComfy](https://www.runcomfy.com/models/acestep-ai/ace-step/audio-outpaint?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-music-runcomfy)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with bash commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include RunComfy model IDs, prompt fields, output directories, and operational cautions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
