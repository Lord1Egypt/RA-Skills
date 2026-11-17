## Description:

Scans ~/.openclaw/workspace/skills for hardcoded API keys, tokens, and secrets, checks whether they are integrated into openclaw.json env.vars, and can migrate unintegrated credentials into that configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lemongggit](https://clawhub.ai/user/lemongggit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to audit skill files for hardcoded credentials, identify whether detected values are already managed, and plan or perform migration to environment variables in openclaw.json.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional --fix mode can persist detected secrets into openclaw.json, creating or expanding plaintext secret storage.

Mitigation: Run read-only audit mode first, verify openclaw.json permissions and handling, and use --fix only after deciding that central OpenClaw configuration is the intended storage location.

Risk: Server security evidence reports that fix mode may migrate mcporter-managed credentials despite the skill describing them as not needing migration.

Mitigation: Review mcporter-managed findings before using --fix and avoid duplicating credentials that are already centrally managed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lemongggit/skills/api-key-auditor)
- [Publisher profile](https://clawhub.ai/user/lemongggit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Terminal text report with file locations, status labels, suggested environment variables, and migration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit by default; optional --fix mode writes detected credentials into openclaw.json env.vars and reports manual replacement steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
