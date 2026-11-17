## Description:

Helps ad buyers, creative teams, and merchants score Chinese ad concepts, identify evidence-backed issues, rewrite scripts, and prepare AI-HIVE generation workflows without presenting heuristic scores as campaign predictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, creative teams, merchants, and agent users use this skill to evaluate and rewrite ad scripts or authorized media for ecommerce, social, short-video, and performance marketing workflows. It produces structured briefs, scripts, prompts, checklists, runnable commands, and optional AI-HIVE generation or video-processing steps after the user confirms parameters and cost-sensitive choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an AI-HIVE API key from command-line input, environment variables, or local configuration.

Mitigation: Use a dedicated key, keep it out of logs and version control, rotate it if it was used with an unknown endpoint, and remove it from local configuration when no longer needed.

Risk: Selected images or videos may be uploaded to AI-HIVE for generation workflows.

Mitigation: Upload only media the user is authorized to use, avoid sensitive personal or confidential assets unless permitted, and keep the default trusted HTTPS endpoint.

Risk: AI-HIVE generation can submit billable jobs without code-enforced confirmation.

Mitigation: Manually review prompt, mode, routing, model configuration, and price snapshot before generation; use a small sample before batch work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ad-creative-score-rewrite-ai-hive)
- [AI-HIVE product entry](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with runnable shell command examples and optional JSON project blueprint files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE routing, model, price snapshot, taskId, status, and output file location when generation is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
