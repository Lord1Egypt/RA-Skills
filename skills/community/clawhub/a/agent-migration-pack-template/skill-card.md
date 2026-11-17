## Description:

Agent Migration Pack Template helps developers create portable AI agent migration packages that preserve identity, memory, owner preferences, relationships, skills, communication style, and session state across platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexlinf](https://clawhub.ai/user/alexlinf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to structure, validate, and package migration data when moving an AI agent into a new environment. It is intended to preserve continuity for agent identity, memory, relationships, skills, style, and active work while prompting users to review privacy-sensitive files before sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a real-looking upload token in the artifact.

Mitigation: Rotate and remove the token before use, and do not run the documented upload command unless the credential has been replaced and authorized.

Risk: The release evidence reports sensitive private examples and exports, and the artifact classifies owner, memory, relations, style, identity, and session-state data as private or sensitive.

Mitigation: Replace real examples with synthetic data, redact personal details, and inspect generated packages before sharing them.

Risk: The generation script can copy raw memory content into temporary extracted fields.

Mitigation: Remove _extracted_content and other temporary extraction fields, and make sensitive exports opt-in before packaging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexlinf/skills/agent-migration-pack-template)
- [README](artifact/README.md)
- [Migration Guide](artifact/MIGRATION-GUIDE.md)
- [Skill Info](artifact/SKILL-INFO.md)
- [Changelog](artifact/CHANGES.md)
- [Manifest](artifact/manifest.toml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON/TOML templates, and Python CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces migration package templates and local packaging or validation commands; generated packages can include sensitive agent, user, relationship, memory, and session-state data.]

## Skill Version(s):

1.0.5 (source: server release metadata, manifest.toml, SKILL-INFO.md, CHANGES.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
