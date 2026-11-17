## Description:

Helps an agent administer an Emby media server running on a Linux NAS, including library refreshes, metadata operations, user and permission review, playback activity checks, and server health troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmd170629](https://clawhub.ai/user/gmd170629)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and NAS administrators use this skill to guide live Emby administration through API calls and Linux service checks while presenting results as concise tables or structured summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a powerful Emby API key for live server administration.

Mitigation: Use HTTPS where possible, avoid placing keys in shared logs or transcripts, and prefer a dedicated limited-scope key.

Risk: The skill can guide destructive or administrative actions such as deletes, user policy changes, restarts, firewall changes, and recursive permission commands.

Mitigation: Require explicit user confirmation before these actions and review proposed commands or API calls before execution.

Risk: The security verdict is suspicious because the skill suggests broad administrator commands without enough guardrails.

Mitigation: Install only after reviewing the skill for the target environment and keep operator approval in the loop for live server changes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/gmd170629/skills/emby-manager)
- [Emby API Quick Reference](references/api-guide.md)
- [Media Operations Guide](references/media-ops.md)
- [Troubleshooting Guide](references/troubleshoot.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Markdown]

**Output Format:** [Markdown with structured lists, tables, API endpoint examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Emby server URL and API key; destructive operations should be confirmed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-03-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
