## Description:

Generate high-quality English and multilingual MP3 audio with Microsoft Edge TTS for pronunciation, read-aloud, and language-learning requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davydenkovm](https://clawhub.ai/user/davydenkovm)

### License/Terms of Use:


## Use Case:

External users, employees, and developers use this skill to convert supplied text into spoken MP3 audio with selectable American or British English voices for pronunciation practice, read-aloud requests, and language learning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audio script can write output to an unrestricted local path and uses a shared predictable temporary file.

Mitigation: Use a dedicated private output directory, avoid caller-selected output paths, and prefer unique temporary files before relying on generated audio.

Risk: Sensitive text passed for speech synthesis may be handled by the agent and the Edge TTS tool.

Mitigation: Review the skill before installation in environments that handle sensitive text or run with broad filesystem permissions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown instructions with inline bash commands and MP3 audio file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires edge-tts installed via pipx; default output path is /tmp/edge_tts_output.mp3.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
