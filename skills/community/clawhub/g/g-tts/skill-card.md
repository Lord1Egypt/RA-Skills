## Description:

High-definition generative speech synthesis using Google Cloud Chirp 3 HD voices with natural pacing and expressive prosody.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarar21](https://clawhub.ai/user/jarar21)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn requested text into MP3 speech through Google Cloud Chirp 3 HD voices, including optional pause tags and voice selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill auto-installs an unpinned npm dependency on first run.

Mitigation: Review before installing, run only where npm installation is acceptable, and prefer a pinned dependency with a lockfile.

Risk: The script can write output files outside the intended workspace when given an absolute output path.

Mitigation: Restrict filesystem permissions and direct output to a dedicated audio directory under the intended workspace.

Risk: Google Application Default Credentials may grant broader cloud access than the text-to-speech workflow needs.

Mitigation: Use credentials scoped to the intended Google Cloud project and least required permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jarar21/skills/g-tts)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration guidance]

**Output Format:** [Plain text status plus an MP3 audio file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, Google Application Default Credentials, network access for Google Cloud Text-to-Speech, and a controlled audio output directory.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
