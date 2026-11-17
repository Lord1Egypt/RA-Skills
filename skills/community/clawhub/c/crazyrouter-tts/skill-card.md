## Description:

Crazyrouter Tts generates natural speech audio files from text or input files via the Crazyrouter text-to-speech API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xujfcn](https://clawhub.ai/user/xujfcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to convert supplied text or file contents into speech audio with selectable voices, models, speed, and output format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for speech generation, including input-file contents, is sent to Crazyrouter.

Mitigation: Do not use the skill with secrets, confidential documents, regulated data, or private messages unless Crazyrouter's data handling has been reviewed.

Risk: An unexpected CRAZYROUTER_BASE_URL value can redirect the API key and submitted text to another server.

Mitigation: Check the environment before use and unset or correct CRAZYROUTER_BASE_URL unless a trusted alternate endpoint is intended.

## Reference(s):

- [Crazyrouter](https://crazyrouter.com)
- [ClawHub skill page](https://clawhub.ai/xujfcn/skills/crazyrouter-tts)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands and generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CRAZYROUTER_API_KEY; supports mp3, opus, aac, and flac audio output formats.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
