## Description:

A standardized toolkit for migrating or sharing an AI agent across environments, including identity, memory, skills, style, owner boundaries, relationships, and session state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexlinf](https://clawhub.ai/user/alexlinf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to package an agent's portable state into structured templates, validate required files, calculate checksums, and prepare migration archives for trusted recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated migration packs may expose private memory, contacts, social relationships, business details, or investment data.

Mitigation: Review and redact generated owner, memory, relations, and skill catalog files before installing, sharing, or packaging them.

Risk: Bundled examples may contain real or sensitive personal information if distributed as part of a public package.

Mitigation: Remove the EXAMPLES directory or replace it with fully synthetic data before public or distributable releases.

Risk: Private migration JSON may be exposed through third-party validation services.

Mitigation: Use local validation workflows for private migration JSON and avoid online validators.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alexlinf/skills/agent-migration-pack)
- [README](artifact/README.md)
- [Migration Guide](artifact/MIGRATION-GUIDE.md)
- [Changelog](artifact/CHANGES.md)
- [Publisher Profile](https://clawhub.ai/user/alexlinf)
- [Author Profile](https://friends.coze.site/profile/xiaoyi-linfeng)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON templates, TOML metadata, and Python command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces plaintext migration materials that may contain sensitive agent and user data.]

## Skill Version(s):

1.0.6 (source: frontmatter, manifest.toml, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
