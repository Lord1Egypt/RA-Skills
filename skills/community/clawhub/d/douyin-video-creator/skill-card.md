## Description:

抖音爆款视频分析与创作引导工具：根据抖音视频链接生成爆款分析报告，或根据主题和用户素材生成候选标题与完整的15秒短视频分镜脚本。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengrb111](https://clawhub.ai/user/zengrb111)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and social media operators use this skill to analyze Douyin viral-video patterns and turn their own topics or media assets into title options, content guidance, and 15-second storyboard scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends cloning and running third-party crawler or downloader tools to collect Douyin video data.

Mitigation: Review and sandbox those tools before use; prefer manual screenshots or user-provided metrics when automated collection is unnecessary.

Risk: Running external data tools can expose Douyin credentials, browser profiles, home directories, SSH keys, tokens, or unrelated files if configured broadly.

Mitigation: Do not enter Douyin credentials or expose sensitive local files unless the tools have been independently verified and isolated.

## Reference(s):

- [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)
- [TikTokDownloader](https://github.com/JoeanAmier/TikTokDownloader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis reports, candidate-title lists, and 15-second storyboard scripts with occasional inline shell commands for optional data tools.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose a Markdown report filename such as 爆款分析_视频ID_日期.md and asks users for screenshots, metrics, or media assets when automated data tools are unavailable.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
