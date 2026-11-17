## Description:

Guides agents through DingTalk knowledge base and document management tasks, including workspace listing, document creation, document reading and writing, deletion, and member permission management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breath57](https://clawhub.ai/user/breath57)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent work with DingTalk workspaces and documents through documented API calls and helper-driven credential setup. It supports knowledge base discovery, document creation, content reads and writes, and document member permission changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper stores DingTalk app secrets and access tokens persistently.

Mitigation: Use only after secrets are protected with owner-only permissions or a credential store, and avoid real DingTalk app secrets until that storage is fixed.

Risk: The configuration-writing helper can enable local command execution from crafted input.

Mitigation: Validate allowed configuration keys, reject control characters, and avoid sed interpolation before deployment.

Risk: The skill can delete documents, overwrite content, and change member permissions when used with sufficiently privileged accounts.

Mitigation: Use least-privilege DingTalk applications and review proposed destructive or permission-changing operations before execution.

## Reference(s):

- [DingTalk Document API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Markdown]

**Output Format:** [Markdown guidance with bash commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
