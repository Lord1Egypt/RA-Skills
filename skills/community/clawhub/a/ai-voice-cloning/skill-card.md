## Description:

AI voice generation, text-to-speech, and voice synthesis via inference.sh CLI for natural speech, narration, conversations, podcasts, video voiceovers, and accessibility workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers, creators, and content teams use this skill to generate speech, narration, multi-voice dialogue, and voiceovers through inference.sh CLI examples and model guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and related skill commands rely on mutable remote code without independent verification.

Mitigation: Use pinned, versioned artifacts where possible, review checksums before installing, and review related npx skill installs as separate dependencies.

Risk: Voice-generation workflows may process sensitive text, private media, or likeness-related inputs through external services.

Mitigation: Avoid submitting sensitive text or private media unless the provider's data handling, consent, and retention terms are acceptable for the intended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/okaris/skills/ai-voice-cloning)
- [inference.sh](https://inference.sh)
- [inference.sh CLI installer](https://cli.inference.sh)
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON CLI inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CLI commands that generate audio, video voiceover, avatar, or media-merging outputs through external inference.sh applications.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
