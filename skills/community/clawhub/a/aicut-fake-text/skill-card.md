## Description:

Make a fake-text chat video with the aicut CLI: a phone conversation that types itself out over gameplay or a green screen, every line read aloud. Use when the user asks for a text-message story, a fake texts video, a chat story or a conversation video for TikTok or Shorts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simrunbot](https://clawhub.ai/user/simrunbot)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to draft and generate a fictional text-message conversation video for TikTok or Shorts with the aicut CLI. It has the user review the script and approve the quoted cost before generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted conversation text is processed by an external service.

Mitigation: Use fictional names and avoid sensitive conversations.

Risk: Video generation spends tokens from the user's balance.

Mitigation: Review the script and total price, then get explicit approval before generation; re-estimate if the request changes.

Risk: The CLI retains a local sign-in session.

Mitigation: Log out locally and revoke the CLI session when access is no longer needed.

## Reference(s):

- [Setup and exit codes](artifact/references/setup.md)
- [The spend guard](artifact/references/spend.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Video]

**Output Format:** [JSON chat script, shell commands, and a generated chat video]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation costs tokens; script and quoted price are reviewed before the user approves generation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
