## Description:

按关键词或指定抖音账号读取公开作品样本，生成不复制原文的竞品矩阵、钩子结构、可见证据、差异机会和选题建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

Douyin creators and content strategists use this skill to study publicly visible posts from selected accounts or search terms, then review a sample-based competitor matrix and testable content ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An invalid request or failed collection run may silently remove earlier research files from the output directory.

Mitigation: Copy earlier reports to a safe location and use a dedicated output folder before collecting; review run-diagnostic.json after a failed run.

## Reference(s):

- [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)
- [EasyBR official download page](https://www.ebrower.com/down.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, HTML]

**Output Format:** [JSON, Markdown, and HTML research reports; a JSON diagnostic when collection fails]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports summarize selected public page samples and do not store or reproduce original post text.]

## Skill Version(s):

1.0.2 (source: package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
