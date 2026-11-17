## Description:

This skill helps beauty brands, creators, training teams, and ecommerce content teams turn beauty tutorial short-video requests into production briefs, step scripts, shot prompts, AI-HIVE video-generation commands, subtitles, product cards, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content developers use this skill to plan, generate, and check Chinese beauty tutorial short videos for ecommerce, advertising, marketing, social commerce, and training workflows. It emphasizes authorized source materials, one clear makeup goal per video, verifiable product steps, and review before any billable AI-HIVE generation task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a billable AI-HIVE API key and can submit generation tasks that may incur cost.

Mitigation: Use a dedicated AI-HIVE key with limited quota, keep the key out of files and logs, and require parameter review before submitting generation requests.

Risk: Changing the AI-HIVE base URL from an untrusted environment can redirect API-key-backed requests.

Mitigation: Keep the default AI-HIVE endpoint unless a trusted operator intentionally configures another endpoint.

Risk: Uploaded reference media may include copyrighted, trademarked, private, or otherwise unauthorized material.

Mitigation: Upload only media the user has rights to use and keep unsupported rights, product claims, medical claims, and platform assertions marked for human verification.

Risk: The public workflow depends on local Python packages and media tools.

Mitigation: Install dependencies in a virtual environment with pinned versions and review generated scripts before running them.

## Reference(s):

- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API Endpoint](https://ai-hive.iclip.cn/api)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/beauty-tutorial-short-video-ai-hive)
- [Publisher Profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with runnable shell command examples, JSON task records, scripts, prompts, subtitles, product-card copy, and checklist sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call AI-HIVE APIs for model lookup, media upload, price snapshots, asynchronous video-generation tasks, polling, and downloads after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
