## Description:

Polls Swedish Blocket.se through the blocket CLI on a schedule, deduplicates listings by ad ID, and sends new matches to Telegram through OpenClaw without invoking a hosted model on each poll.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x3r081](https://clawhub.ai/user/x3r081)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers can configure scheduled Blocket searches, deduplicate seen listing IDs, and send new listing alerts to a Telegram target. The skill is intended for personal classified-alert monitoring with locally managed configuration files.

### Deployment Geography for Use:

Sweden

## Known Risks and Mitigations:

Risk: The user-level systemd timer polls Blocket every hour and sends listing details, search terms, and optional configuration summaries to the configured Telegram chat.

Mitigation: Review the configured timer, run dry-run validation before enabling notifications, and configure only Telegram targets and searches that are acceptable to share through that channel.

Risk: config.json and seen.json can contain personal Telegram chat IDs and search preferences.

Mitigation: Keep config.json and seen.json private and do not publish real copies to public repositories or shared skill bundles.

Risk: Polling an external classified-listing service can conflict with service terms or rate limits if configured aggressively.

Mitigation: Respect Blocket's terms of use and rate limits, and keep polling frequency appropriate for personal monitoring.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/x3r081/skills/blocket-watch)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Blocket CLI](https://github.com/blocket-se/blocket)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell commands with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local configuration guidance and command examples for a Linux systemd timer workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog mention 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
