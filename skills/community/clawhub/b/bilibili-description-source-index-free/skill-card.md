## Description:

从指定的 1–3 个 B 站视频简介中整理可见的公开资料链接、用途、访问状态和缺项，生成可核对的索引草稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users use this skill to organize public learning, tool, and reference links visible in 1–3 specified Bilibili video descriptions. It produces a traceable draft with source videos, visible purposes, access results, and gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External browser installers and dependencies require review.

Mitigation: Review the external installer and browser dependencies before installation.

Risk: Offline parser results do not establish that a link was visibly provided by the author.

Mitigation: Treat offline parser results as unverified links and confirm them against the visible page.

Risk: Browser actions could affect an unintended environment or draft destination.

Mitigation: Bind operations to the chosen browserId and explicitly name any authorized draft destination.

## Reference(s):

- [Easy WebBridge](https://github.com/aiispower/easy-webbridge)
- [EasyBR AI operation guide](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)
- [EasyBR downloads](https://www.ebrower.com/down.html)
- [OpenCLI Bilibili adapter notes](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/bilibili.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown]

**Output Format:** [JSON or Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 100 link rows, with source, visible purpose, access status, evidence, and gaps.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
