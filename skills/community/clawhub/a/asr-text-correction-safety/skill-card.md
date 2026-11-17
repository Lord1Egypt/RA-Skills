## Description:

Guides developers in reviewing and auditing ASR, OCR, and other text-correction layers to prevent silent changes to already-correct text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[y16689540962-cloud](https://clawhub.ai/user/y16689540962-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design and review transcription or OCR post-processing so that corrections do not silently alter the user's meaning. An optional local audit helper checks dictionary-word changes, idempotence, and common-word collisions in a correction module.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local audit helper executes the correction module supplied for testing.

Mitigation: Audit only correction modules you already trust to run locally.

## Reference(s):

- [Related project (skill homepage)](https://github.com/y16689540962-cloud/dsh-voice-personal)
- [Text-correction design notes](https://github.com/y16689540962-cloud/dsh-voice-personal/blob/main/docs/DESIGN.md)
- [Adversarial audit findings](https://github.com/y16689540962-cloud/dsh-voice-personal/blob/main/docs/ADVERSARIAL.md)
- [Host integration pitfalls](https://github.com/y16689540962-cloud/dsh-voice-personal/blob/main/docs/PITFALLS.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with JavaScript and shell examples; optional plain-text audit results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local audit requires Node.js and a correction module; the dictionary check requires a system word list.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
