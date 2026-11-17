## Description:

Generate, inpaint, and outpaint music with ACE Step on RunComfy via the runcomfy CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creative technologists, and external users use this skill to generate music from tags and lyrics, regenerate time ranges inside tracks, or extend existing tracks through RunComfy ACE Step endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned @runcomfy/cli install examples can introduce supply-chain uncertainty.

Mitigation: Prefer a pinned or lockfile-backed @runcomfy/cli version and avoid running npm as an administrator.

Risk: RUNCOMFY_TOKEN can expose account access if copied into prompts, logs, or committed files.

Mitigation: Keep RUNCOMFY_TOKEN out of prompts and logs, and use the configured RunComfy credential path or environment variable only where needed.

Risk: Inpaint and outpaint workflows depend on user-supplied audio URLs.

Mitigation: Use only audio URLs intentionally provided for the current task and treat unexpected output divergence as a reason to inspect the source audio.

## Reference(s):

- [ClawHub ACE Step skill page](https://clawhub.ai/permew/skills/ace-step)
- [RunComfy](https://www.runcomfy.com)
- [ACE Step text-to-audio](https://www.runcomfy.com/models/acestep-ai/ace-step/text-to-audio?utm_source=clawhub&utm_medium=skill&utm_campaign=ace-step)
- [ACE Step 1.5 text-to-audio](https://www.runcomfy.com/models/acestep-ai/ace-step-1.5/text-to-audio?utm_source=clawhub&utm_medium=skill&utm_campaign=ace-step)
- [ACE Step audio-inpaint](https://www.runcomfy.com/models/acestep-ai/ace-step/audio-inpaint?utm_source=clawhub&utm_medium=skill&utm_campaign=ace-step)
- [ACE Step audio-outpaint](https://www.runcomfy.com/models/acestep-ai/ace-step/audio-outpaint?utm_source=clawhub&utm_medium=skill&utm_campaign=ace-step)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=ace-step)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce RunComfy CLI commands that download generated audio files to the requested output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
