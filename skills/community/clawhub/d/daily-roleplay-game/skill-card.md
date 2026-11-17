## Description:

Daily Roleplay Game sets up a Chinese-language adult OpenClaw roleplay workspace with daily character generation, hidden kink guessing, achievement tracking, scheduled messages, and optional image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nannyu](https://clawhub.ai/user/nannyu)

### License/Terms of Use:

Private use; do not redistribute without permission

## Use Case:

External users and developers use this skill to install and run a private OpenClaw roleplay agent that generates daily characters, manages guess progress, sends scheduled roleplay messages, and archives generated state and images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a disclosed adult roleplay workspace with persistent agent behavior and recurring messages or images.

Mitigation: Install only when the user intentionally wants a Chinese-language adult roleplay workspace.

Risk: Recurring messages may be sent to an unintended destination if the message channel is left as last.

Mitigation: Configure a fixed private message channel before enabling scheduled roleplay messages.

Risk: Heartbeat configuration under global agent defaults can affect agents beyond the roleplay workspace.

Mitigation: Avoid placing the heartbeat under agents.defaults unless the user explicitly wants that global behavior.

Risk: Calendar, memory, or todo summaries can expose private context through generated roleplay messages.

Mitigation: Disable calendar and memory todo summaries unless the user explicitly wants that data used and sent.

Risk: Scheduled archive behavior can retain generated images and roleplay state in local archives.

Mitigation: Review or patch wrapup.sh before scheduling it, and decide how archives should be deleted or protected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nannyu/skills/daily-roleplay-game)
- [Project homepage](https://github.com/nannyu/openclaw-role-play-skill)
- [OpenClaw setup guide](docs/OPENCLAW_SETUP.md)
- [Cron configuration](docs/CRON_CONFIG.md)
- [Daily roleplay design document](docs/daily-roleplay-game.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and YAML/JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent workspace files and may trigger recurring messages and generated images when configured.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
