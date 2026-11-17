## Description:

A Xiaohongshu/RedNote agent skill that uses Python Playwright to search and read content, manage login sessions, prepare and publish posts, and perform confirmed account interactions with JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deliciousbuding](https://clawhub.ai/user/deliciousbuding)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and agent users use this skill to automate Xiaohongshu content discovery, account-session checks, publishing preparation, confirmed posting, and engagement workflows through a JSON CLI. It is suited for agent-assisted social-media operations where write actions require explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change a real Xiaohongshu account through publishing, comments, replies, likes, collections, and logout.

Mitigation: Require fresh explicit user confirmation before every write action and show the target account, content, media, and operation type before execution.

Risk: Local browser profiles, cookies, QR codes, and session metadata can expose account state.

Mitigation: Use a dedicated account, keep local state private, avoid custom cookie paths, and do not upload or display authentication files, QR codes, or full security parameters.

Risk: Captcha, login, or security-verification pages can make automation unsafe or invalid.

Mitigation: Stop automation on these pages, switch to headed mode for user handling, and do not attempt bypasses or retry loops.

Risk: A submitted-but-unconfirmed publish result may already have created content, so automatic retries can duplicate posts.

Mitigation: Treat submitted_unconfirmed as requiring manual review and do not retry automatically.

Risk: The server security verdict is suspicious because real-account and local-file actions are under-scoped.

Mitigation: Install only after reviewing the security guidance, prefer pinned or provenance-checked installation, and inspect or remove ~/.xiaohongshu/stealth.js before use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/deliciousbuding/skills/chore-system-upgrade)
- [README_EN.md](README_EN.md)
- [CLI command reference](docs/API.md)
- [Installation guide](docs/INSTALL.md)
- [Security guide](docs/SECURITY.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Reference implementations](docs/REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [JSON CLI responses with text, Markdown, shell-command, configuration, and guidance content when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Standard output is JSON; diagnostics are written to standard error.]

## Skill Version(s):

1.5.0 (source: pyproject.toml and CHANGELOG, released 2026-08-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
