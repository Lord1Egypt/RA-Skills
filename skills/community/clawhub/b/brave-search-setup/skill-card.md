## Description:

Configure Brave Search API and troubleshoot network/proxy issues for web_search functionality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingliu1617-art](https://clawhub.ai/user/qingliu1617-art)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to configure Brave Search API access, diagnose web_search or web_fetch fetch failures, and set proxy configuration on macOS when local networking requires it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to configure API keys, which can expose secrets if pasted into shell history, logs, or shared configuration files.

Mitigation: Use secret-entry or protected configuration methods, avoid pasting real keys into commands saved by shell history, and review file permissions on local OpenClaw configuration.

Risk: The skill includes persistent proxy changes and a sudo proxychains configuration path that can affect local networking beyond a single command.

Mitigation: Prefer temporary session-scoped proxy settings first, review each command before execution, and prepare a rollback plan before changing shell profiles or system-wide proxychains configuration.

## Reference(s):

- [Brave Search API Docs](https://api.search.brave.com/app/docs)
- [OpenClaw Config](https://docs.openclaw.ai/config)
- [Clash Verge](https://github.com/clash-verge-rev/clash-verge-rev)
- [ClawHub Skill Page](https://clawhub.ai/qingliu1617-art/skills/brave-search-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes configuration steps, diagnostic commands, proxy setup guidance, and verification checks.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
