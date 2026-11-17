## Description:

Builds Chinese ad A/B creative matrices for ecommerce and social campaigns, turning product facts, audience goals, budget, historical assets, and test variables into hook-evidence-scene-CTA matrices, minimum test batches, generation tasks, and naming rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, ad optimizers, and creative production teams use this skill to plan explainable ad creative tests, prepare scripts and prompts, and optionally submit AI-HIVE image or video generation jobs after reviewing cost, routing, and input constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI-HIVE API key can be sent to a configured endpoint other than the intended AI-HIVE HTTPS service.

Mitigation: Before running generation or upload commands, verify --base-url, AI_HIVE_BASE_URL, and ~/.ai-hive/config.json, and keep the API key in an environment variable or protected local config only.

Risk: Generated advertising concepts can overstate product facts, imply unauthorized endorsements, or copy protected reference material too closely.

Mitigation: Use only authorized source assets, mark unverified claims for review, keep reference use at the structural level, and require human approval before paid generation or publication.

Risk: Paid batch generation can duplicate work or spend more than intended if tasks are submitted without review.

Mitigation: Review prompts, routing mode, model configuration, pricing snapshots, and a minimum sample batch before expanding concurrency.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ad-ab-creative-matrix-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, JSON task records, and optional generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query AI-HIVE model configuration and pricing snapshots, upload authorized reference media, poll asynchronous tasks, and download generated image or video outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
