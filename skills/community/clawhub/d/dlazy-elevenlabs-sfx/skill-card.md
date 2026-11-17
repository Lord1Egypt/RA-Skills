## Description:

Generates 1–22 second sound effects from text descriptions using the ElevenLabs text-to-sound model, for foley, ambience, alerts, and game audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, audio designers, and game creators can generate short sound effects such as foley, ambience, alerts, and game audio from text prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The relationship between dLazy account setup and sound generation is unclear, and some references were unresolved in the security assessment.

Mitigation: Review the dLazy setup and linked service information before connecting an account; understand that prompts are sent to the hosted API and use an API key that can be rotated or revoked.

## Reference(s):


## Skill Output:

**Output Type(s):** [Audio files, JSON]

**Output Format:** [Generated sound effect audio asset, returned through a JSON result envelope as a hosted URL or an optionally saved file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sound effects are 1–22 seconds long; generation may be synchronous or asynchronous.]

## Skill Version(s):

1.3.42 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
