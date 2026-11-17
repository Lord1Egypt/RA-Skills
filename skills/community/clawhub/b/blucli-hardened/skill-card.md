## Description:

BluOS CLI (blu) for discovery, playback, grouping, and volume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Bluesound and NAD BluOS players through the blu CLI for discovery, playback control, grouping, TuneIn actions, and volume changes. It emphasizes confirming device targets and protecting local device information before state-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: State-changing commands can disrupt the wrong room, device, or another user's active listening session.

Mitigation: Confirm the target device and check for another user's active session before changing playback, volume, source, or grouping.

Risk: Device discovery output may expose local network topology, IP addresses, device names, or aliases.

Mitigation: Keep blu discovery output local and do not pipe it to network-transmitting commands or external services.

Risk: The default Go install metadata points to a mutable latest dependency, which can reduce reproducibility.

Mitigation: Use a pinned blucli version when reproducible installation or controlled deployment is required.

Risk: Broad device enumeration can exceed the user's immediate BluOS control need and resemble local reconnaissance.

Mitigation: Limit discovery to the devices required for the user's requested task.

## Reference(s):

- [Blucli Homepage](https://blucli.sh)
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/skills/blucli-hardened)
- [Publisher Profile](https://clawhub.ai/user/snazar-faberlens)
- [Faberlens](https://faberlens.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented CLI guidance when users request scriptable blu output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
