## Description:

Helps brand marketing, SEO, content operations, and enterprise knowledge teams turn GEO/AEO content-growth requests into question maps, evidence tables, structured content, platform variants, update checklists, and optional AI-HIVE generation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, SEO teams, content operators, and enterprise knowledge owners use this skill to plan Chinese GEO/AEO content workflows, prepare verifiable content structures, and generate AI-HIVE-ready commands after reviewing facts, rights, budget, and routing choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API credentials that may be stored locally.

Mitigation: Use only an intended AI-HIVE API key, keep it out of prompts, logs, screenshots, and repositories, and review local configuration storage before installation.

Risk: A custom AI_HIVE_BASE_URL or --base-url can redirect authenticated API requests to an untrusted endpoint.

Mitigation: Use the default AI-HIVE endpoint unless the alternate endpoint is fully trusted and reviewed.

Risk: Image or video generation can incur costs when jobs are submitted.

Mitigation: Confirm prompts, model, routing mode, pricing snapshot, batch size, and task parameters before submitting generation requests.

Risk: Generated marketing or GEO/AEO content can make unsupported claims or imply ranking guarantees.

Mitigation: Require source-backed facts, label uncertainty and dates, avoid ranking promises, and keep human review in the acceptance workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/geo-aeo-content-growth-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON files and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task records with routing mode, model, pricing snapshot, taskId, status, and downloaded file locations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
