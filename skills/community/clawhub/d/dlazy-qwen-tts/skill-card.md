## Description:

Generates speech from text with Alibaba Bailian qwen3-tts using system voices or a custom voice description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other dLazy users can turn provided text into speech using a curated system voice or a voice described in natural language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text prompts are sent to the hosted dLazy API for speech generation.

Mitigation: Avoid submitting confidential or personal text unless its use with the service is approved.

Risk: The skill invokes `dlazy login`, which stores an API key locally; the security scan could not determine the CLI's credential handling, and reference checks were incomplete.

Mitigation: Review the CLI credential flow before logging in, and rotate or revoke the key if it may have been exposed.

## Reference(s):

- [dLazy service](https://dlazy.com)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Audio files, JSON]

**Output Format:** [Generated audio asset returned by URL in a JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return an asynchronous task identifier when requested.]

## Skill Version(s):

1.3.44 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
