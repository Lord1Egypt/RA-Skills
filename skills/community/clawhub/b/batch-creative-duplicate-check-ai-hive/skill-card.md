## Description:

This skill helps commerce, advertising, marketing, and content-production teams review batches of image and video assets for duplicate groups, near-duplicates, creative collisions, retention recommendations, and regeneration queues using AI-HIVE workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, commerce operators, content teams, and developers use this skill to turn batch creative duplicate-checking requests into review plans, runnable AI-HIVE commands, scripts, prompts, task records, and quality checklists. It is intended for authorized assets and reviewable workflows, not for copying protected content, making false product claims, or bypassing platform rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is framed as duplicate checking, but server security evidence says the shipped tools mainly generate, upload, and download AI media.

Mitigation: Review it as a media-generation and API-integration skill, and install it only when AI-HIVE media generation, uploads, downloads, and task polling are intended.

Risk: AI-HIVE calls may be billable and can involve media uploads and local downloads.

Mitigation: Confirm prompts, routing mode, model configuration, pricing snapshot, and download location before running generation commands; use small samples before batch work.

Risk: The scripts use a locally stored API key and allow a configurable API base URL.

Mitigation: Use environment variables or protected local config for credentials, avoid logging or committing API keys, and use custom base URLs only when independently trusted.

Risk: Server security guidance says not to rely on this skill for actual duplicate detection without separate tooling.

Mitigation: Use independent duplicate-detection, rights-review, or legal-review tooling for final determinations, especially where similarity, copyright, trademarks, privacy, or platform policy matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/batch-creative-duplicate-check-ai-hive)
- [ClawHub publisher profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE chat entry point](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON artifacts and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local files, upload or download media, and initiate AI-HIVE image or video generation after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
