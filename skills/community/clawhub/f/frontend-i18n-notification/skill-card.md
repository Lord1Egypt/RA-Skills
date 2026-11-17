## Description:

Frontend theme engineer skill for i18n-compliant user text, translation files, and framework-safe user notification patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to keep Weline UI copy translatable and to replace browser-native dialogs with framework-safe notification and confirmation patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated UI changes could leave visible strings outside the intended translation mechanism.

Mitigation: Validate new or changed UI text against the repository's i18n files and conventions before release.

Risk: User prompts could retain blocking browser-native dialogs in modified frontend paths.

Mitigation: Replace alert, confirm, and prompt usage with framework toast or confirmation components and verify the affected screen.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiweline/skills/frontend-i18n-notification)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with code or configuration changes when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation evidence and notes about missing translation coverage or UX copy risks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
