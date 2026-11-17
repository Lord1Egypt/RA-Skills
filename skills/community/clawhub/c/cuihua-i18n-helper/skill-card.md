## Description:

Cuihua i18n Helper supports internationalization workflows by extracting translatable UI strings, generating locale JSON files, checking translation coverage, and guiding translation-provider use for modern web applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supermario11](https://clawhub.ai/user/supermario11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and localization engineers use this skill to find hardcoded UI text, create and maintain locale files, and review missing or unused translations in JavaScript, React, Vue, Angular, and related web projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read project UI source files and write locale JSON files during extraction or checks.

Mitigation: Run it only from a clean working tree with explicit source and locales paths, then review generated file changes before committing.

Risk: Project strings may be sent to third-party translation providers if cloud translation is enabled.

Mitigation: Do not allow cloud translation for sensitive strings until the provider, credentials, and data-handling terms have been approved.

Risk: The documentation claims broad AI translation capabilities that are not fully supported by the bundled helper script.

Mitigation: Treat automated translation claims as requiring review and verify actual outputs against the generated locale files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supermario11/skills/cuihua-i18n-helper)
- [Publisher profile](https://clawhub.ai/user/supermario11)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, code examples, and locale JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; may read project UI source files and write locale JSON files.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
