## Description:

Guides agents through upgrading EmpireCMS 7.5 sites for PHP 8.x compatibility, including prioritized file repairs, code changes, and verification steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ebandao777-oss](https://clawhub.ai/user/ebandao777-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to migrate EmpireCMS 7.5 projects from PHP 7.x to PHP 8.x, fix fatal compatibility issues, and document and test each file-level change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to rewrite many CMS files, which can break a live site if applied broadly or without a recovery path.

Mitigation: Require restorable file and database backups, process one file or module at a time, and verify each completed change before continuing.

Risk: The security summary flags unsafe SQL rewrite examples that could preserve or introduce injection risk.

Mitigation: Do not apply SQL examples as written; require casts or prepared statements for IDs and class IDs, with human review before deployment.

Risk: The artifact includes environment-specific details such as hardcoded host and Windows path examples.

Mitigation: Treat those details as source-environment notes and replace them with values verified for the user's deployment.

## Reference(s):

- [Source repository (server-resolved GitHub import)](https://github.com/ebandao777-oss/empirecms7.5-upgrade-php8.x)
- [ClawHub skill page](https://clawhub.ai/ebandao777-oss/skills/empirecms7-5-upgrade-php8-x)
- [Publisher profile](https://clawhub.ai/user/ebandao777-oss)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline PHP code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be applied incrementally with backups, per-file verification, and human review for SQL changes.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
