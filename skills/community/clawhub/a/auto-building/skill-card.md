## Description:

基于 AUTO-BUILDING 源码，生成定制化信息采集管理系统。用户指定栏目、分类、数据源后，系统自动采集、审核、发布内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to configure and launch a custom content aggregation system with selected categories, collection rules, and data sources. It is intended for workflows such as news digests, product monitoring, industry information collection, and resource directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to clone and run an unpinned external Node.js project whose executable code is outside the reviewed skill package.

Mitigation: Pin the repository to a reviewed commit, inspect package scripts and dependencies, and run it with minimal credentials in a sandbox or disposable environment.

Risk: Configured data sources may include content that has collection, republication, privacy, or copyright restrictions.

Mitigation: Confirm source terms and applicable rules before collection, and use the documented review workflow before publishing collected content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/addogiavara-tech/skills/auto-building)
- [Project homepage](https://sora.wboke.com/)
- [AUTO-BUILDING source repository referenced by install metadata](https://github.com/hasd52636-a11y/Auto_Building_new)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON, TypeScript, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to edit configuration files, run local Node.js commands, and direct the user through review and publishing steps.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, CHANGELOG, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
