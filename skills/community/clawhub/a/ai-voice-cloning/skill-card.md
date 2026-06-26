## Description: <br>
Ai Voice Cloning helps agents generate natural text-to-speech, voice synthesis, narration, conversations, voiceovers, audiobooks, podcasts, video narration, and accessibility audio through the inference.sh CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and operators use this skill to produce AI-generated speech for voiceovers, audiobooks, podcasts, e-learning, accessibility, IVR, localization, and video narration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice, text, portrait, video, or other media inputs may be sent to inference.sh during generation. <br>
Mitigation: Do not submit private scripts, regulated data, unconsented voice samples, portraits, or videos unless the user has permission and accepts the provider's data handling terms. <br>
Risk: The quick-start installer uses a remote shell script for CLI installation. <br>
Mitigation: Install only if the user trusts inference.sh, or review and manually install the CLI with checksum verification before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/okaris/ai-voice-cloning) <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI installer](https://cli.inference.sh) <br>
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides inference.sh CLI calls that may return generated audio or media URLs.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
