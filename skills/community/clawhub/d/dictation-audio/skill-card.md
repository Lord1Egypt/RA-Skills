## Description:

Generates English dictation audio from word lists, reading each word twice with a one-second pause between readings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[effeceee](https://clawhub.ai/user/effeceee)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users, educators, and language-learning developers use this skill to generate MP3 dictation practice audio from English word lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned pip package and local edge-tts and ffmpeg binaries.

Mitigation: Install and run it only in environments where those dependencies are approved and maintained.

Risk: The generated audio is written to /tmp/dictation.mp3 and can overwrite an existing file at that path.

Mitigation: Check or move any existing /tmp/dictation.mp3 file before running the skill.

Risk: Sensitive words may be exposed on shared machines through generated audio output in /tmp.

Mitigation: Avoid processing sensitive word lists on shared systems or clean up the generated file immediately after use.

## Reference(s):

- [Dictation Audio ClawHub Skill Page](https://clawhub.ai/effeceee/skills/dictation-audio)
- [ClawHub Homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [MP3 audio file with brief terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the generated audio to /tmp/dictation.mp3.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
