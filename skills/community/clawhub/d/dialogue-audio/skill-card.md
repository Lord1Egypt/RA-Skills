## Description: <br>
Multi-speaker dialogue audio creation with Dia TTS, including speaker tags, emotion control, pacing, conversation flow, and post-production guidance for podcasts, audiobooks, explainers, character dialogue, and conversational content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and production teams use this skill to draft and run Dia TTS commands for two-speaker dialogue audio. It supports conversational audio workflows such as podcasts, explainers, audiobooks, character dialogue, and post-production assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on a third-party CLI installer and the falai Dia TTS cloud service. <br>
Mitigation: Install only if the provider is trusted, prefer the documented manual install path with checksum verification, and authenticate with the intended inference.sh account. <br>
Risk: Dialogue scripts may be sent to a third-party TTS service. <br>
Mitigation: Avoid submitting confidential scripts unless the provider's data handling practices are acceptable for the intended use. <br>


## Reference(s): <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI installer](https://cli.inference.sh) <br>
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt) <br>
- [ClawHub skill page](https://clawhub.ai/okaris/dialogue-audio) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Dia TTS prompt structures using [S1] and [S2] speaker tags, pacing and emotion cues, and optional media post-production command examples.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
