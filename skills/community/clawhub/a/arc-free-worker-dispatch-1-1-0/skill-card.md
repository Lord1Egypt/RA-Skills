## Description:

Routes agent tasks to free AI models through OpenRouter for content writing, research, code generation, and similar delegated work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieyer](https://clawhub.ai/user/sieyer)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to delegate lower-risk writing, research, analysis, and code-generation prompts to OpenRouter free models while reserving primary model usage for review and orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated task content is sent to OpenRouter and downstream models.

Mitigation: Do not use the skill with secrets, proprietary code, customer data, regulated records, or sensitive business context.

Risk: Batch and output-file workflows may overwrite files or process unsafe batch inputs.

Mitigation: Avoid batch files from untrusted sources and avoid --output in batch mode until validation is fixed.

Risk: Some command paths can bypass the advertised free-model restriction and may use paid models.

Mitigation: Verify model names manually and check OpenRouter usage before relying on cost controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sieyer/skills/arc-free-worker-dispatch-1-1-0)
- [Publisher Profile](https://clawhub.ai/user/sieyer)
- [OpenRouter Chat Completions API](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Plain text or JSON on stdout, with optional file output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY; JSON mode can include model, token, and timing metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
