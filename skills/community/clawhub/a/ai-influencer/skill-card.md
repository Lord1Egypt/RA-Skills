## Description:

Create an AI clone video (talking head) from a single reference photo, a text script, and a cloned voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yadavabhijeet4](https://clawhub.ai/user/yadavabhijeet4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to ask an agent to run an AI influencer talking-head video workflow from a reference image, style prompt, script text, and voice ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script may report successful video generation without producing the claimed video artifact.

Mitigation: Review and correct the implementation before use, and verify that a real output file is created before relying on the result.

Risk: The workflow requests API keys, face images, voice material, and scripts for an implementation that has not been verified to perform the claimed processing.

Mitigation: Do not provide sensitive credentials or biometric media until privacy handling is documented and the implementation has been validated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yadavabhijeet4/skills/ai-influencer)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash commands and command-line arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires API-key environment variables and user-supplied image, prompt, text, and voice ID inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
