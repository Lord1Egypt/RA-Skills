## Description:

Generates multilingual ElevenLabs eleven_v3 speech from text with curated voices and adjustable stability, similarity, and style controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can turn written scripts into multilingual speech for dubbing, audiobooks, and character dialogue, choosing a voice and adjusting stability, similarity, and style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises ElevenLabs speech generation but uses dLazy login and authentication commands, and the scan does not establish how that authentication relates to the advertised purpose.

Mitigation: Review the complete instructions and CLI help, and use the skill only if you trust dLazy and intend to authenticate through its account and API flow.

Risk: Prompts are sent to dLazy-hosted services, and local media supplied to the CLI is uploaded to dLazy media storage.

Mitigation: Do not submit sensitive text or files unless they are appropriate to share with dLazy; use only content you are authorized to provide.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-elevenlabs-tts)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Audio, JSON]

**Output Format:** [Generated speech audio with JSON result metadata and hosted asset URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return an asynchronous task ID or save a generated asset to a local path.]

## Skill Version(s):

1.3.42 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
