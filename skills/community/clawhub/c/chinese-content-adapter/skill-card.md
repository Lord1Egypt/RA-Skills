## Description:

Adapts Chinese-language content for Juejin, Zhihu, Xiaohongshu, and WeChat MP with platform-specific formatting, SEO suggestions, tags, and posting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karmyweng](https://clawhub.ai/user/karmyweng)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-language creators, marketers, and developer advocates use this skill to transform one source article into platform-specific drafts for Juejin, Zhihu, Xiaohongshu, and WeChat MP. It also provides title, tag, image, SEO, and posting-time recommendations for preparing content before manual publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat output may include unsafe HTML when generated from untrusted Markdown or HTML input.

Mitigation: Review the generated WeChat HTML before pasting it into a source-mode editor, and sanitize untrusted third-party content before processing.

Risk: The skill is specialized for Chinese-platform content workflows and may produce irrelevant guidance outside that scope.

Mitigation: Use it only for Juejin, Zhihu, Xiaohongshu, and WeChat MP preparation workflows.

Risk: Installing the latest package without a pinned version can make future behavior depend on a newer release.

Mitigation: Prefer a pinned installer version when one is available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/karmyweng/skills/chinese-content-adapter)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Guidance, Configuration]

**Output Format:** [JSON-style dictionaries containing platform-adapted text, Markdown content, WeChat HTML, tags, image suggestions, SEO recommendations, and posting guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill does not publish content automatically; users review and publish the generated drafts themselves.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
