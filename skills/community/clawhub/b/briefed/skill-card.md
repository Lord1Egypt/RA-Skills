## Description:

Sets up a personal daily Gmail newsletter digest with AI summaries, a local web reader, notes, voting, and interest tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesnation](https://clawhub.ai/user/jamesnation)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users set up a daily newsletter digest from their read-only Gmail inbox, with AI-generated summaries and a local reader for saving, annotating, and ranking stories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Newsletter subjects, senders, and snippets are sent to the configured model provider.

Mitigation: Confirm the user accepts this data sharing before enabling summarization.

Risk: Newsletter bodies, notes, and votes are stored unencrypted in the OpenClaw workspace.

Mitigation: Restrict local file access and delete workspace data and revoke Google access on uninstall.

Risk: Remote reader access could expose private newsletter content.

Mitigation: Keep remote access token-protected over HTTPS or Tailscale; avoid plain-HTTP LAN exposure.

Risk: A daily cron job or login auto-start continues processing mail in the background.

Mitigation: Enable scheduled or persistent operation only with the user's consent.

## Reference(s):

- [Briefed on ClawHub](https://clawhub.ai/jamesnation/skills/briefed)
- [Project homepage (publisher metadata)](https://github.com/jamesnation/briefed)
- [Tailscale Serve documentation](https://tailscale.com/kb/1312/serve)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown with setup commands, configuration, and daily digest summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local newsletter data and a reader app when set up; optional daily notification.]

## Skill Version(s):

1.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
