## Description:

Control Apple Music on macOS via the `clawtunes` CLI for playback, search, catalog lookup, AirPlay, volume, shuffle, repeat, and playlist management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forketyfork](https://clawhub.ai/user/forketyfork)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent operate Apple Music on macOS through shell commands for playback, search, volume, playlist, AirPlay, and catalog tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing from a third-party Homebrew tap requires trusting that tap.

Mitigation: Install only if you trust the forketyfork/tap Homebrew source and are comfortable using it for clawtunes.

Risk: Apple Music control may require macOS Automation access.

Mitigation: Grant Automation permission only when Apple Music control is intended.

Risk: The skill is specific to Apple Music rather than generic music or audio tasks.

Mitigation: Use it only when Apple Music is the intended music application.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forketyfork/skills/clawtunes)
- [clawtunes project homepage](https://github.com/forketyfork/clawtunes)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target macOS Apple Music through the clawtunes CLI; use non-interactive mode when choosing media.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
