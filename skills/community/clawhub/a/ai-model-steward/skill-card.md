## Description:

AI 模型智能管家 monitors AI model releases and free token offers, generates weekly deployment recommendations, and supports approved OpenClaw fallback configuration changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhbb2221](https://clawhub.ai/user/hhbb2221)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to track model availability, free-token opportunities, and weekly model deployment recommendations. They can manually approve, remove, list, or roll back fallback-model configuration changes after reviewing the generated intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled network polling and API calls may contact external model and news sources on a recurring basis.

Mitigation: Install only when recurring network access is acceptable, and review configured data sources and credentials before enabling scheduled runs.

Risk: The skill uses an OpenRouter API key and stores model-intelligence data locally.

Mitigation: Provide only the intended API key, keep OpenClaw configuration access restricted, and review local cache contents under ~/.openclaw/.ai-model-steward.

Risk: Manual approve, reject, deploy, and rollback commands can change OpenClaw's active fallback model configuration.

Mitigation: Review generated recommendations and backup paths before changing production configuration, then verify model availability after deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hhbb2221/skills/ai-model-steward)
- [OpenRouter Models API](https://openrouter.ai/api/v1/models)
- [Hugging Face Blog](https://huggingface.co/blog)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [CLI text output, JSON status objects, and Markdown weekly reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes model-intelligence cache and report files under ~/.openclaw/.ai-model-steward and can update ~/.openclaw/openclaw.json after manual approval commands.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact metadata lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
