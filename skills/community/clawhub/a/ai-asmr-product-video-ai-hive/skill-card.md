## Description:

This skill turns AI ASMR product-video requests into Chinese production workflows, storyboards, video prompts, sound-design checklists, runnable AI-HIVE commands, and review criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to plan and produce AI ASMR product-video assets for e-commerce, advertising, social media, and short-form content workflows. It helps gather product facts and authorized media, draft reviewable concepts and prompts, optionally submit AI-HIVE generation jobs, and validate finished clips against platform and brand requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys are read from the environment, CLI arguments, or ~/.ai-hive/config.json.

Mitigation: Use a limited, rotatable AI-HIVE API key, keep the config file private, and avoid placing real keys in prompts, logs, screenshots, or repositories.

Risk: The workflow can upload user media and download generated files.

Mitigation: Upload only media the user has rights to use, review files before submission, and direct downloads to a dedicated output directory.

Risk: Video and image generation may incur paid API charges.

Mitigation: Confirm prompts, model, routing mode, and price snapshot before submitting jobs; use small samples before batch generation.

Risk: Custom base URLs can redirect API calls to an untrusted endpoint.

Mitigation: Use the default HTTPS AI-HIVE endpoint unless the alternate AI_HIVE_BASE_URL is fully trusted and intentionally configured.

Risk: Generated content or plans could include unverifiable product claims, platform promises, or unauthorized imitation.

Mitigation: Mark unverified facts for review, require rights to reference materials, and avoid claims about sales, ranking, approval, or endorsement unless independently verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-asmr-product-video-ai-hive)
- [AI-HIVE chat entry point](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown with bash commands and JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include production briefs, shot lists, prompts, model routing choices, price snapshots, task IDs, status records, and downloaded file locations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
