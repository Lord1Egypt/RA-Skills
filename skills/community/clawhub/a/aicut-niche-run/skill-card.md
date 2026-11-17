## Description:

Make a video from a ready-made trend format (a niche) with the aicut CLI: find a format, read its inputs, fill them in, price it and run it in one command. Use when the user wants a viral or trending video template, names an aicut niche, or asks what formats are available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simrunbot](https://clawhub.ai/user/simrunbot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to select a ready-made aicut trend format, supply its inputs, review the quoted cost, authorize a run, and receive the generated video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video, image, or audio generation can consume the user's token balance.

Mitigation: Estimate each purchase, state what the quoted price covers, and wait for explicit approval before spending; obtain new approval if settings change or a retry is needed.

Risk: Selected media may be uploaded, and a persistent CLI login can retain account access.

Mitigation: Make uploads clear to the user, use only media they are authorized to share, and log out and revoke CLI access when finished if continued access is not wanted.

## Reference(s):

- [Setup and exit codes](artifact/references/setup.md)
- [The spend guard](artifact/references/spend.md)
- [ClawHub skill page](https://clawhub.ai/simrunbot/skills/aicut-niche-run)

## Skill Output:

**Output Type(s):** [Video, Shell commands, Guidance]

**Output Format:** [Generated video asset with a concise status message and video URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A single video run; generation has a quoted token cost and requires explicit user approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
