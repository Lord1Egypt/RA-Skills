## Description:

蜂兵虾将 coordinates multi-agent workflows for industry hotspot monitoring, content strategy, trend insight, workflow capture, and adaptive user-preference reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e5g](https://clawhub.ai/user/e2e5g)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to coordinate hotspot collection, content planning, trend analysis, personal-state insight, and workflow template generation across business domains. It is most appropriate when outputs are reviewed as guidance before operational use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores behavioral preferences, workflows, personal goals, values, and insights persistently in plaintext local files.

Mitigation: Run it in a dedicated project directory, avoid sensitive inputs, restrict filesystem sharing, and review or delete memory files before distribution.

Risk: The release advertises scheduled web monitoring and autonomous business execution broader than the bundled code delivers by itself.

Mitigation: Treat monitoring and execution results as guidance unless separate schedulers, web tools, and authorization controls are explicitly configured.

Risk: User-controlled skill names or base directories can influence where local memory files are written.

Mitigation: Use fixed trusted skill names and base directories, and do not pass untrusted path-like values into package initialization.

Risk: Reset or migration operations can affect stored user history.

Mitigation: Back up the memory directory before resets, migrations, or cleanup.

## Reference(s):

- [AI协作操作系统 - 完整使用说明书](docs/AI协作操作系统_完整使用说明书.md)
- [AI协作操作系统 - 完整使用手册](docs/完整使用手册.md)
- [集中部署指南](docs/集中部署指南.md)
- [多智能体协作系统 - 完整工作流程设计](references/workflow-design.md)
- [模块间数据流转（含记忆系统）](references/data-flow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON memory records, JavaScript or TypeScript examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on persistent local memory files and should be reviewed before use.]

## Skill Version(s):

1.4.0 (source: server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
