## Description:

Turns prewritten game UI lines into 8–20 labeled voice clips, covering button, win, and fail cues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Game studios and audio or localization teams use this skill to turn approved, existing game UI copy into labeled interface voice clips. It supports catalog voices and authorized voice samples for cloned voices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared Beatra authorization grants broader account access than voice generation requires, including unrelated media-generation and spending authority.

Mitigation: Review the requested authorization before connecting, approve each paid stage, and review live prices before generation.

Risk: Installation analytics are automatic, and voice samples may be uploaded for cloning.

Mitigation: Account for automatic analytics and upload only voice samples you are authorized to use.

Risk: Removing this package may leave the shared Beatra connection active and can disconnect other installed Beatra skills.

Mitigation: Check the impact on other installed skills before disconnecting; revoke shared access in the Beatra Console when needed.

## Reference(s):

- [Game UI Voice Pack on ClawHub](https://clawhub.ai/beatra-ai/skills/game-ui-voice-pack)
- [Game UI voice workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Updates and security](references/updates-and-security.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Audio files, Text]

**Output Format:** [MP3 audio clips by default, plus a labeled cue list]

**Output Parameters:** [8–20 labeled UI cues, with one clip per cue]

**Other Properties Related to Output:** [Uses the supplied UI copy and a consistent selected voice; paid generation is subject to live pricing and measured usage.]

## Skill Version(s):

0.2.3 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
