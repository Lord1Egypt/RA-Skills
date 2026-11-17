## Description:

Generate, create, or scaffold Ansible playbooks, roles, tasks, handlers, inventory, vars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq280948982](https://clawhub.ai/user/qq280948982)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to generate Ansible playbooks, roles, tasks, inventories, and project configuration with idempotency, module-selection, and validation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Ansible content can intentionally change remote systems if run without review.

Mitigation: Review generated playbooks, roles, tasks, inventories, and variables before running them against managed hosts.

Risk: Generated Ansible files may require environment-specific validation before production use.

Mitigation: Run syntax, lint, and applicable Ansible validation checks, or use the skill's documented manual static checks when tools are unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq280948982/skills/ansible-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML snippets, shell commands, and validation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Ansible content should be reviewed before execution; validation may be manual when tooling is unavailable.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
