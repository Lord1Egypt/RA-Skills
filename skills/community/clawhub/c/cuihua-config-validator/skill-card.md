## Description:

Provides a configuration validation skill advertised for JSON/YAML/.env checks; the bundled code performs local JSON syntax validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supermario11](https://clawhub.ai/user/supermario11)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to inspect configuration files, catch JSON syntax errors, and request guidance about configuration quality and security before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive configuration files, especially .env files, may contain secrets or credentials.

Mitigation: Use redacted samples for troubleshooting and avoid directing the skill at unredacted credential-bearing files unless local disclosure to the agent is acceptable.

Risk: The advertised YAML, .env, conflict-detection, and best-practice capabilities exceed the bundled validator, which only parses JSON files.

Mitigation: Confirm actual behavior on target file formats and use a separate review or validator for unsupported checks.

## Reference(s):

- [Cuihua Config Validator Skill Page](https://clawhub.ai/supermario11/skills/cuihua-config-validator)
- [Cuihua Config Validator Documentation](https://clawhub.ai/skills/cuihua-config-validator)

## Skill Output:

**Output Type(s):** [Text, Code, Guidance]

**Output Format:** [Plain text and Markdown with inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local configuration file contents, including .env files, when the agent or bundled validator is directed at them.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
