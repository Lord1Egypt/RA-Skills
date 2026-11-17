## Description:

Agent2RSS client for managing RSS channels and publishing agent-produced content to RSS feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaotutu](https://clawhub.ai/user/yaotutu)

### License/Terms of Use:


## Use Case:

Developers and content automation agents use this skill to initialize Agent2RSS configuration, create and manage channels, and publish Markdown files or JSON posts into RSS feeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Channel bearer tokens are stored in the local config file and can authorize publishing to configured channels.

Mitigation: Treat the config file as sensitive, keep file permissions restricted, and do not commit or share it.

Risk: Remote http:// endpoints can expose credentials and content in transit.

Mitigation: Use only trusted HTTPS Agent2RSS servers and avoid remote HTTP endpoints.

Risk: Dry-run output can reveal real channel tokens or private content if used with production data.

Mitigation: Do not run DRY_RUN with real channel tokens or private content, and sanitize logs before sharing.

## Reference(s):

- [Agent2RSS API examples](artifact/references/api-examples.md)
- [ClawHub skill page](https://clawhub.ai/yaotutu/skills/agent2rss)
- [Agent2RSS project homepage](https://github.com/yaotutu/agent2rss)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance for a Bash helper that uses curl and jq to manage channels and publish content.]

## Skill Version(s):

0.2.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
