## Description:

Provides a checklist and migration guidance for upgrading EmpireCMS 7.5 sites to PHP 8 compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ebandao777-oss](https://clawhub.ai/user/ebandao777-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill when migrating EmpireCMS 7.5 from PHP 7.x to PHP 8, diagnosing PHP 8 fatal errors, and planning compatibility edits across legacy PHP code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad PHP compatibility edits can affect large parts of an EmpireCMS site.

Mitigation: Apply changes in a version-controlled copy or staging environment, review replacements manually, and run functional tests before deployment.

Risk: Migration guidance may not match customized EmpireCMS installations, plugins, encodings, or templates.

Mitigation: Validate behavior for admin login, content publishing, search, comments, member flows, mail, file upload, archive handling, template tags, and GBK-specific text handling where applicable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ebandao777-oss/skills/empirecms7-php8-upgrade)
- [Publisher profile](https://clawhub.ai/user/ebandao777-oss)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with PHP code examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only migration guidance; generated edits should be reviewed and tested before deployment.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
