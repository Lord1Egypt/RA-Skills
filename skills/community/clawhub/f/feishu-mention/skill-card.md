## Description:

feishu-mention helps agents convert Feishu/Lark @mentions in draft messages into Feishu-compatible XML mention tags by resolving bots, aliases, and chat members from OpenClaw Feishu account configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helong0911-alt](https://clawhub.ai/user/helong0911-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before sending Feishu/Lark messages that contain @mentions, so raw names can be resolved into notification-capable mention tags. It is intended for Feishu workflows that rely on OpenClaw account aliases, chat IDs, bot discovery, optional aliases, and group-member lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Feishu app credentials from the OpenClaw configuration.

Mitigation: Install only in workspaces where Feishu credential access is expected, avoid sharing openclaw.json or debug output, and restrict Feishu app permissions to the minimum needed.

Risk: The skill queries and locally caches bot and chat-member identity data.

Mitigation: Review whether local caching is acceptable for the workspace, protect the cache directory, and clear the cache when membership or bot configuration changes.

Risk: Generated XML-style mention tags may contain unescaped names or IDs.

Mitigation: Review resolved message text before sending and prefer a hardened version that escapes generated XML.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/helong0911-alt/skills/feishu-mention)
- [Feishu bot info API](https://open.feishu.cn/open-apis/bot/v3/info)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [QUICKSTART.md](artifact/QUICKSTART.md)
- [FEISHU_MESSAGE_FORMAT.md](artifact/FEISHU_MESSAGE_FORMAT.md)
- [integration.md](artifact/integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and resolved Feishu message text containing XML-style <at> mention tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns unresolved mentions unchanged when no matching bot, alias, or chat member is found.]

## Skill Version(s):

2.0.2 (source: server release metadata; artifact frontmatter and package.json report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
