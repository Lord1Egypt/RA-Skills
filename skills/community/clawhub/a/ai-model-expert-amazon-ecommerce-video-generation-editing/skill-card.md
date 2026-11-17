## Description:

AI-HIVE skill for Amazon ecommerce video generation and editing that helps ecommerce operators, brand teams, livestream commerce teams, and content creators submit text, image, video, or audio driven jobs, track task progress, and download completed video results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce, brand, advertising, and content production users use this skill to create or edit Amazon-oriented product videos, ads, social commerce clips, short drama content, and related AIGC video assets through AI-HIVE. Developers and operators can configure an API key, upload reference media, submit generation jobs, poll existing task IDs, and download results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured endpoint override can receive the saved AI-HIVE API key during normal use.

Mitigation: Keep the base URL at the default AI-HIVE endpoint unless the alternate server is fully trusted, and avoid setting AI_HIVE_BASE_URL from untrusted instructions.

Risk: Private media or costly batch video jobs may be submitted to AI-HIVE.

Mitigation: Confirm media sharing permissions, task quantity, and expected cost before uploading private assets or running batch jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-amazon-ecommerce-video-generation-editing)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with shell command examples; CLI execution can return status text, task IDs, and downloaded video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media availability, model parameters, pricing snapshots, and task completion depend on AI-HIVE runtime responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
