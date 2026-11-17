## Description:

Apply modern web development best practices for security, compatibility, code quality, and coding standards. Covers KISS/DRY/YAGNI principles, TypeScript/JavaScript standards, React patterns, write-time quality enforcement, and comprehensive code review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huamu668](https://clawhub.ai/user/huamu668)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to have an agent apply web development standards for TypeScript, React, security, browser compatibility, performance, and code review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated sites may load mutable third-party JavaScript for polyfills.

Mitigation: Review examples before use and prefer locally bundled or pinned polyfills with integrity controls.

Risk: Broad error telemetry guidance could expose sensitive data if copied without controls.

Mitigation: Use approved telemetry providers and redact sensitive data before capture.

Risk: Copying pre-commit or agent hook examples into a project can run commands automatically.

Mitigation: Review hook configuration before enabling it in a project.

## Reference(s):

- [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Web Quality Audit](../web-quality-audit/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no API calls or files are produced unless an agent applies the guidance in a project.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
