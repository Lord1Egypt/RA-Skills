## Description:

Verify real local environment facts before an agent uses machine-specific commands, runtimes, compilers, services, or startup scripts, then create or refresh environment baseline JSON and related environment policy, AGENTS, or skill documents from those verified facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zshtolors](https://clawhub.ai/user/zshtolors)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to verify local toolchains, runtime paths, environment variables, services, and startup scripts before running machine-specific commands. It helps create synchronized JSON baselines and Markdown policy snippets from verified machine facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Probe files can run arbitrary local commands.

Mitigation: Use only reviewed probe files from a trusted publisher and do not run probe definitions supplied by an untrusted source.

Risk: Generated baselines and Markdown can preserve sensitive machine details such as local paths, hostnames, PATH entries, and environment-derived secrets.

Mitigation: Review and redact generated JSON and Markdown before committing, publishing, or sharing them.

Risk: Environment-changing actions can modify local software or configuration when performed without review.

Mitigation: Require explicit approval before installing, upgrading, uninstalling, enabling, or reconfiguring software, and prefer user-managed installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zshtolors/skills/environment-security)
- [Document Contracts](artifact/references/document-contracts.md)
- [Probe File](artifact/references/probe-file.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command blocks, JSON environment baselines, and optional generated Markdown policy snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce environment-baseline.json, ENVIRONMENT_POLICY.md, AGENTS.environment.md, AGENTS.md sections, or SKILL.environment.md snippets; outputs can include local paths, hostnames, PATH entries, and environment-derived values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
