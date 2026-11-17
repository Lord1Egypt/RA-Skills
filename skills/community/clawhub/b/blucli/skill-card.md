## Description:

Blucli provides guidance for using the BluOS blu CLI for discovery, playback, grouping, and volume control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steipete](https://clawhub.ai/user/steipete)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to install or operate the blu command-line tool when discovering and controlling Bluesound/NAD BluOS players.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install metadata uses an unpinned Go module version for the upstream blu CLI.

Mitigation: Review the upstream project or prefer a pinned release before installing, as recommended by the server security guidance.

Risk: Playback and grouping commands can change the state of real Bluesound/NAD devices.

Mitigation: Confirm the target device before changing playback, volume, or grouping.

## Reference(s):

- [Blucli homepage](https://blucli.sh)
- [Blucli ClawHub skill page](https://clawhub.ai/steipete/skills/blucli)
- [blu Go module documentation](https://pkg.go.dev/github.com/steipete/blucli/cmd/blu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented CLI guidance when scripts should prefer blu --json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
