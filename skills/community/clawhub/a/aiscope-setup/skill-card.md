## Description:

Installs AIScope and its agent skills, verifies the executable, and runs a first noninteractive instruction audit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayanth-mkv](https://clawhub.ai/user/jayanth-mkv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can install AIScope, verify that it runs, and check a project's agent instructions with a first noninteractive scan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned standalone skills CLI can introduce supply-chain changes.

Mitigation: Review or pin the installer; prefer a checksum-verified AIScope release or the pinned aiscope-cli@0.1.2 package.

## Reference(s):

- [AIScope release downloads](https://github.com/Jayanth-MKV/aiscope/releases/latest)
- [AIScope Setup on ClawHub](https://clawhub.ai/jayanth-mkv/skills/aiscope-setup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Scan findings]

**Output Format:** [Text and shell commands; JSON scan results when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Confirms the scanned project root and explains any instruction conflicts without modifying instruction files unless requested.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
