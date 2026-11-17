## Description:

AI-powered translation via Crazyrouter. Translate text between any languages using GPT-5, Claude, DeepSeek, or Qwen. Supports file translation and multi-model comparison. Use when user asks to translate text, documents, or compare translations. Requires environment variable CRAZYROUTER_API_KEY (get at https://crazyrouter.com).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xujfcn](https://clawhub.ai/user/xujfcn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate text or files between languages through Crazyrouter-backed AI models, optionally preserving Markdown formatting and selecting a model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom CRAZYROUTER_BASE_URL value can send the API key and translated content to an arbitrary endpoint.

Mitigation: Run only with CRAZYROUTER_BASE_URL unset or set to an explicitly trusted endpoint, and review the environment before execution.

Risk: Text and files submitted for translation are sent to an external model service.

Mitigation: Do not translate secrets, private documents, regulated data, or proprietary material unless use of the configured external service is approved.

## Reference(s):

- [Crazyrouter](https://crazyrouter.com)
- [Crazyrouter API endpoint](https://crazyrouter.com/v1)
- [ClawHub skill page](https://clawhub.ai/xujfcn/skills/crazyrouter-translate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Translated text to stdout or a user-selected output file; Markdown can be preserved when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CRAZYROUTER_API_KEY. The CRAZYROUTER_BASE_URL environment variable changes the service endpoint if set.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
