## Description:

Helps Chinese content teams turn product, brand, or campaign facts into platform-specific GEO articles, FAQs, Zhihu answers, social posts, image prompts, and optional AI-HIVE generation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External content teams, marketers, and developers use this skill to plan Chinese GEO content across Baidu, WeChat, Zhihu, Xiaohongshu, and websites from a shared fact base. It can also prepare runnable AI-HIVE commands for reviewed image generation workflows, including routing choice, price snapshot capture, task polling, and download records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an AI-HIVE API key locally and uses it for AI-HIVE API calls.

Mitigation: Install only if you trust AI-HIVE, keep the local key file permission-restricted, prefer environment variables for temporary use, and do not commit keys or include them in logs.

Risk: Custom base URLs could route credentials, uploads, task polling, or downloads through an unintended service.

Mitigation: Use the default AI-HIVE API endpoint unless you control and trust the alternative endpoint.

Risk: Image or video generation may incur cost and can upload sensitive, copyrighted, or unauthorized media.

Mitigation: Review prompts, routing mode, price snapshots, media rights, and batch size before submitting generation jobs; start with a small sample.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/geo-content-writer-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown responses with JSON files, shell command snippets, and optional downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a blueprint JSON file, AI-HIVE task records, price snapshots, status output, and downloaded image or video assets when the user approves generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
