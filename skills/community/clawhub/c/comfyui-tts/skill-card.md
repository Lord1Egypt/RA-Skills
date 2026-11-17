## Description:

Generate speech audio using ComfyUI Qwen-TTS service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhsi5358](https://clawhub.ai/user/yhsi5358)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to submit text-to-speech jobs to a configured ComfyUI Qwen-TTS service and retrieve generated audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unescaped option values can alter the ComfyUI workflow submitted by the script.

Mitigation: Review option values before execution and harden the script by JSON-encoding all workflow values and validating numeric parameters.

Risk: Text submitted to a remote ComfyUI host may travel over plain HTTP.

Mitigation: Keep ComfyUI bound to localhost when possible, avoid sending secrets or private text, and require HTTPS or another protected channel for remote hosts.

Risk: The skill relies on a trusted ComfyUI service and local command-line dependencies.

Mitigation: Install only when the configured ComfyUI service is trusted and confirm curl and jq are available before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yhsi5358/skills/comfyui-tts)
- [Publisher profile](https://clawhub.ai/user/yhsi5358)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal output and file paths for generated audio, with optional downloaded audio file output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and access to a configured ComfyUI service.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
