## Description:

Turn incoming text (email/newsletter) into a short TTS podcast with chunking + ffmpeg concat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cerbug45](https://clawhub.ai/user/cerbug45)

### License/Terms of Use:


## Use Case:

Developers and content automation users can use this skill to convert newsletter or email text into a short audio briefing workflow. It parses text or HTML, chunks content for speech generation, and concatenates audio with ffmpeg.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate its TTS behavior because the bundled script contains a provider stub and currently generates placeholder audio unless a real TTS provider is wired in.

Mitigation: Review and implement the TTS provider integration before relying on the output as a real podcast workflow.

Risk: Unsafe temporary-file handling around ffmpeg can create avoidable file-safety risk when processing valuable or sensitive inputs.

Mitigation: Run the skill in a limited workspace without privileged accounts and fix the temporary-file handling before processing important files.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration guidance]

**Output Format:** [Markdown instructions with command-line examples and generated MP3 file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and ffmpeg; TTS provider integration must be supplied before real speech generation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
