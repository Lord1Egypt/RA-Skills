## Description:

AIEOS helps agents load, validate, apply, export, and summarize portable persona schemas so identity and behavior files remain consistent across environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeglin](https://clawhub.ai/user/zeglin)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to manage AIEOS persona schemas, update OpenClaw identity files, export identity data, and generate human-facing bio pages from persona data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Imported local or URL-based schema content can be persisted into agent identity and behavior files.

Mitigation: Apply schemas only from trusted sources, review the dry-run output before using --apply, and keep recoverable copies of identity files.

Risk: Generated bio pages may expose or embed untrusted persona data.

Mitigation: Inspect and sanitize generated HTML before publishing it, especially when the persona data came from a URL or another untrusted source.

Risk: Weak validation can allow malformed or misleading persona data to shape agent behavior.

Mitigation: Validate schemas before applying them and manually review important identity, psychology, and linguistics fields for accuracy.

## Reference(s):

- [AIEOS schema v1](https://aieos.org/schema/v1/aieos.schema.json)
- [ClawHub skill page](https://clawhub.ai/zeglin/skills/aieos)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, json, markdown, code]

**Output Format:** [Markdown guidance with inline shell commands; generated files may be JSON, Markdown, or HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The apply command defaults to a dry run and only writes identity files when invoked with --apply.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
