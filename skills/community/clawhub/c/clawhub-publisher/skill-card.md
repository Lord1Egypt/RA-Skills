## Description:

Automates ClawHub skill publishing with version management, changelog generation, asset bundling, metadata validation, and deployment workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shepherd217](https://clawhub.ai/user/shepherd217)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill publishers use this skill to package, validate, version, and publish agent skills to ClawHub, including batch publishing and rollback workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may operate with ClawHub publishing credentials and account-changing authority.

Mitigation: Use least-privilege short-lived tokens, pass credentials through protected environment or secret-manager mechanisms, and avoid command-line flags for secrets.

Risk: Installation examples reference external packages that were not validated by the Skill Card generator.

Mitigation: Use an isolated environment, avoid global installation where possible, and pin and verify the publisher package before use.

Risk: Publishing or rollback workflows could change public skill releases.

Mitigation: Run dry-run or validation first and review the skill directory for secrets before publishing or rollback.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shepherd217/skills/clawhub-publisher)
- [Publisher Documentation](https://docs.midas-skills.com/clawhub-publisher)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell, JavaScript, JSON, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce publishing configuration, changelog text, validation results, and ClawHub package URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
