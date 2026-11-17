## Description:

Generates matching scene sound effects from text prompts or video frames using Kling SFX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agents use this skill to generate sound effects or background music from text prompts or a single reference video through the dLazy Kling SFX workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a third-party CLI and hosted API, so prompts and selected media may leave the local environment.

Mitigation: Only submit prompts and files suitable for upload to dLazy, and review the dLazy service terms for the intended use case.

Risk: A persistent global CLI install can increase exposure if the package or local environment is compromised.

Mitigation: Prefer per-run npx or a local install when practical, and use the pinned @dlazy/cli version identified by the release evidence.

Risk: The skill requires a dLazy API key stored in local configuration or supplied through an environment variable.

Mitigation: Protect the API key, limit access to local config files, and rotate or revoke the key if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dlazyai/skills/dlazy-keling-sfx)
- [dLazy CLI Source](https://github.com/dlazyai/cli)
- [@dlazy/cli npm Package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy Homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The invoked CLI returns JSON containing generated output URLs or an asynchronous task identifier.]

## Skill Version(s):

1.3.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
