## Description:

Personalized GitHub digest - tracks activity from people you follow, GitHub Trending, and hot new projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miraclemin](https://clawhub.ai/user/miraclemin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and GitHub users use this skill to configure a local agent that fetches public GitHub activity, GitHub Trending, and new high-growth repositories, then remixes the results into daily, weekly, or on-demand digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores GitHub, Telegram, and Resend credentials in local dotfiles.

Mitigation: Use narrowly scoped expiring tokens, restrict permissions on ~/.follow-github, and remove unused delivery keys.

Risk: The skill can install scheduled local jobs that run Node scripts.

Mitigation: Review cron or OpenClaw cron entries before enabling scheduled delivery and remove jobs when no longer needed.

Risk: The skill can load remote prompt files when prompts.remoteUrl is configured.

Mitigation: Keep prompts.remoteUrl unset unless the URL is trusted and controlled; prefer bundled or local prompts.

Risk: Digest content can be sent to external delivery services when Telegram or email delivery is configured.

Mitigation: Confirm the configured chat ID or email address and avoid sending sensitive content through delivery channels you do not control.

## Reference(s):

- [Follow Github ClawHub listing](https://clawhub.ai/miraclemin/skills/follow-github)
- [README](README.md)
- [Skill instructions](SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown digest text, JSON fetch output, setup guidance, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a GitHub token; optional Telegram or Resend credentials enable scheduled delivery.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
