## Description:

Provides real-time A-share stock and index quote lookups for Shanghai and Shenzhen stock codes using a free finance data endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ra1nzzz](https://clawhub.ai/user/ra1nzzz)

### License/Terms of Use:


## Use Case:

Developers and agent users can query current A-share stock and index prices by providing Shanghai or Shenzhen ticker symbols. The skill is useful for quick market lookups and simple quote checks from an agent or command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional installation step can create or overwrite a global /usr/local/bin/a-stock symlink with sudo.

Mitigation: Prefer running the script directly unless a global command is needed, and verify the symlink target before creating it.

Risk: Ticker symbols entered by the user are sent to Tencent Finance over the network.

Mitigation: Treat queried symbols as shared with the external data provider and avoid using the skill for sensitive or confidential watchlists.

Risk: The artifact documentation and metadata do not consistently name the market data provider.

Mitigation: Verify the data source disclosure before release or before relying on provider-specific behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ra1nzzz/skills/a-stock-market)
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text quote output with command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports one or more stock or index symbols per invocation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
