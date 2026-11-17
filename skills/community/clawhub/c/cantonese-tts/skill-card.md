## Description:

Converts Mandarin or Cantonese text into Cantonese-style speech and generates an MP3 with selectable tone and voice options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimpenn](https://clawhub.ai/user/jimpenn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to turn Mandarin or Cantonese text into spoken Cantonese MP3 output for narration, testing, or content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Speech generation uses edge-tts and may send submitted text to an external network-backed service.

Mitigation: Avoid submitting confidential, regulated, or credential-like text unless external processing is acceptable.

Risk: Dependency behavior can change when installing edge-tts without fixed versions.

Mitigation: Install dependencies in a virtual environment and pin versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimpenn/skills/cantonese-tts)
- [Publisher profile](https://clawhub.ai/user/jimpenn)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [CLI command guidance, console status text, and MP3 audio file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports normal, slow, fast, and angry tone settings with hiuMaan, hiuGaai, or wanLung voice selection.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
