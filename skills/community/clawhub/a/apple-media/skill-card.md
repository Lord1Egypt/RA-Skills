## Description:

Control Apple TV, HomePod, and AirPlay devices via pyatv (scan, stream, playback, volume, navigation).

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronn](https://clawhub.ai/user/aaronn)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to generate command-line guidance for discovering, pairing, targeting, and controlling authorized Apple TV, HomePod, and AirPlay devices on a local network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to control Apple media devices discovered on the local network.

Mitigation: Only target devices the operator is authorized to use, and prefer known device IPs when possible.

Risk: Pairing credentials may be stored in ~/.pyatv.conf after setup.

Mitigation: Protect or remove ~/.pyatv.conf when device control should no longer persist.

Risk: The install command accepts the latest pyatv release rather than a pinned reviewed version.

Mitigation: For stricter supply-chain control, install a reviewed pinned pyatv version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaronn/skills/apple-media)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires atvremote from pyatv and authorized access to Apple media devices on the local network.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
