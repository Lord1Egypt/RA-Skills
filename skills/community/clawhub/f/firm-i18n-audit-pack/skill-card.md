## Description:

Internationalization audit pack for scanning JSON and YAML locale files to detect missing translation keys, inconsistent key structures across languages, and untranslated strings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and localization maintainers use this skill to audit application locale files for missing translation keys, inconsistent key structures, and untranslated strings before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit scope depends on the user-provided configuration path.

Mitigation: Review the config path before running the tool so it inspects only intended locale files.

Risk: The skill depends on the referenced OpenClaw extension package.

Mitigation: Confirm the extension package is trusted before installing or using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/skills/firm-i18n-audit-pack)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown or text audit findings produced by the OpenClaw i18n audit tool.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audits are scoped by the user-provided configuration path and locale files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
