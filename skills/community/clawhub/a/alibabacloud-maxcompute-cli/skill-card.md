## Description:

Supports operational Alibaba Cloud MaxCompute or ODPS data-plane work and static diagnosis with `aliyun maxc` across SQL/query/cost/explain, metadata/partitions, sample/profile/transfer, jobs, authentication, permissions, sessions, namespaces, quotas, connectivity, and errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan, execute, or diagnose concrete MaxCompute CLI data-plane tasks through Alibaba Cloud CLI. It is also used for static analysis of supplied MaxCompute command plans or JSON/error envelopes when execution is disallowed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent operate Alibaba Cloud MaxCompute through the local CLI, including cloud-data and authentication actions.

Mitigation: Install it only when that authority is intended, and review requested login, project/session change, package install, upload, overwrite, DDL/DML, job cancel, or credential-helper actions before approving them.

Risk: CLI installation or upgrade steps can change the local execution environment.

Mitigation: Prefer pinned or isolated CLI installation where possible and require explicit user approval before package installation or upgrades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-maxcompute-cli)
- [Bootstrap flow](references/bootstrap-flow.md)
- [MaxCompute authentication and context](references/bootstrap-auth.md)
- [`aliyun maxc` command patterns](references/command-patterns.md)
- [JSON output format](references/json-output-format.md)
- [MaxCompute SELECT guide](references/maxcompute-select-guide.md)
- [MaxCompute SQL notes](references/maxcompute-sql-notes.md)
- [Partition guide](references/partition-guide.md)
- [RAM policies](references/ram-policies.md)
- [Red lines](references/red-lines.md)
- [Setup and install](references/setup-install.md)
- [SQL common errors](references/sql-common-errors.md)
- [MaxCompute SQL common pattern templates](references/sql-query-patterns.md)
- [Text2SQL general generation principles](references/text2sql-principles.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, SQL, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command plans, CLI invocations, SQL snippets, JSON-envelope diagnosis, and required final-result fields.]

## Skill Version(s):

0.0.1 (source: server release evidence and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
