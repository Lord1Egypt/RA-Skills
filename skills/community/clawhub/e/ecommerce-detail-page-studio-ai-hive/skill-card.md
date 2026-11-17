## Description:

Helps ecommerce design, operations, brand marketing, and outsourced detail-page teams turn product facts, audience concerns, brand constraints, platform requirements, and authorized assets into detail-page structure, module copy, visual prompts, AI-HIVE media tasks, and mobile review checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce practitioners and developers use this skill to plan Chinese ecommerce detail pages and related campaign assets, then prepare reviewable copy, prompts, runnable AI-HIVE commands, task logs, and acceptance checks. It is intended for authorized product, brand, and marketing workflows, not unauthorized copying or unsupported commercial claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent API keys may be exposed or over-privileged.

Mitigation: Use a low-privilege, revocable AI-HIVE API key and keep it out of prompts, logs, screenshots, generated files, and version control.

Risk: Changing the AI-HIVE endpoint can send prompts, media, or credentials to an untrusted service.

Mitigation: Use the official AI-HIVE endpoint unless the alternate AI_HIVE_BASE_URL or --base-url target has been independently trusted.

Risk: Generated media downloads may overwrite or clutter local files.

Mitigation: Choose a dedicated output directory and review file paths before downloading generated images or videos.

Risk: Billable generation can run with the wrong prompt, routing mode, or uploaded media.

Mitigation: Confirm final prompts, routing mode, model selection, price snapshot, and authorized source media before submitting generation tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ecommerce-detail-page-studio-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with runnable shell commands, JSON task records, and checklist sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE routing mode, model choice, price snapshot, taskId, status, and downloaded file location when generation is run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
