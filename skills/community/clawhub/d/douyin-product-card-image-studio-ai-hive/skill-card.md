## Description:

Creates Chinese Douyin product-card image workflows, prompts, runnable AI-HIVE commands, and review checklists for product-card, Douyin shop, Qianchuan ad, and e-commerce creative teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce, advertising, and marketing teams use this skill to turn product facts, authorized media, promotion rules, audience details, and target dimensions into Douyin-ready product-card image plans, AI-HIVE generation commands, content variants, and acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be persisted and forwarded when the AI-HIVE helper script is configured.

Mitigation: Use a scoped, revocable AI-HIVE key, keep it out of logs and repositories, and review local configuration before sharing the environment.

Risk: The helper script can target a custom base URL through command-line or environment configuration.

Mitigation: Use the official AI-HIVE endpoint unless the alternate endpoint is fully trusted and reviewed.

Risk: Reference media can be uploaded to AI-HIVE during generation workflows.

Mitigation: Upload only images, video, audio, logos, and other media that the user is authorized to share with AI-HIVE.

Risk: Generation tasks may incur cost or create commercial claims that need review.

Mitigation: Confirm prompts, routing mode, model choice, price snapshot, and factual claims before submitting generation tasks; use small batches first.

Risk: Script dependencies and downloaded outputs run in the user's local environment.

Mitigation: Install dependencies in an isolated environment and review generated files before reuse or publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/douyin-product-card-image-studio-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON files and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run AI-HIVE commands that upload authorized media, poll asynchronous tasks, and download generated image or video files after user confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
