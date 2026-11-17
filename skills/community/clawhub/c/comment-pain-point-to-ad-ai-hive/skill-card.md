## Description:

Turns comment-section pain points into ad strategy, scripts, prompts, runnable AI-HIVE commands, and acceptance checklists for Chinese ecommerce and social content teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, product teams, media buyers, and user researchers use this skill to turn authorized comment exports or screenshots and product facts into ad concepts, pain-point priorities, scripts, image or video tasks, and review checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can send the AI-HIVE bearer API key to an arbitrary configured API URL.

Mitigation: Use the default AI-HIVE endpoint unless the destination is fully trusted; avoid --base-url, AI_HIVE_BASE_URL, and modified ~/.ai-hive/config.json values, and prefer a dedicated revocable low-balance API key.

Risk: Image or video generation can be billable and may upload selected business media to AI-HIVE.

Mitigation: Review prompts, routing, model selection, and uploaded media before generation; start with a small sample and keep task records for audit and retry decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/comment-pain-point-to-ad-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with JSON files and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce task records with routing mode, model, price snapshot, taskId, status, and file paths; billable AI-HIVE generation is intended to be confirmed before submission.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
