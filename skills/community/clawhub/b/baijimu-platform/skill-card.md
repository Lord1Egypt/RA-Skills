## Description:

通过 `baijimu` CLI 使用百积木企业 AI 操作系统，帮助代理进行认证、工作区与项目管理、Bundle 和 Module、Hosted Service、运行时服务、智能体、平台应用和本地 Connector 相关查询或操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[momoplan](https://clawhub.ai/user/momoplan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to work with the Baijimu platform through its official CLI and documentation, including authentication, workspace and project tasks, Bundle and Module workflows, Hosted Service management, runtime checks, agents, platform apps, and local Connectors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running an unintended Baijimu CLI package could route platform operations through the wrong tool.

Mitigation: Verify that @baijimu/cli is the intended official CLI before installation, and prefer a pinned or reviewed package version when supported.

Risk: Authenticated create, update, deploy, publish, delete, cost-incurring, or external-message operations can affect live Baijimu resources.

Mitigation: Use the least-privileged Baijimu account practical for the task, resolve exact targets before writes, and require user approval for destructive, cost-incurring, or externally visible actions.

Risk: Capability tokens, personal access tokens, model keys, service tokens, cookies, or full authentication responses could be exposed through prompts, logs, source files, artifacts, or chat.

Mitigation: Keep Capability Tokens only in the target Hosted Service Environment Secret and do not output authentication material or complete credential responses.

Risk: Documentation, CLI help, and runtime status can disagree, causing incorrect commands or stale assumptions.

Mitigation: Use official documentation, current CLI help, and authoritative runtime status as sources of truth, and report mismatches with the observed versions, commands, and errors.

## Reference(s):

- [Baijimu documentation](https://docs.baijimu.com/)
- [Baijimu LLM documentation index](https://docs.baijimu.com/llms.txt)
- [Baijimu documentation manifest](https://docs.baijimu.com/docs-manifest.json)
- [Hosted Service Capability documentation](https://docs.baijimu.com/development/bundle-development/hosted-service-capability.md)
- [Skill homepage](https://github.com/momoplan/baijimu-platform-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI-derived status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve actual CLI versions, commands, errors, target IDs, and verification results when reporting platform actions.]

## Skill Version(s):

2.0.1 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
