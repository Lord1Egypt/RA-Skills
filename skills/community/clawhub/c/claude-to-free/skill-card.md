## Description:

Helps migrate OpenClaw from Claude subscription OAuth to free or lower-cost providers such as OpenRouter, Gemini, or Ollama.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluebirdback](https://clawhub.ai/user/bluebirdback)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to diagnose Claude OAuth failures and switch an OpenClaw setup to OpenRouter, Gemini, or Ollama with matching authentication, model selection, restart, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Ollama install step pipes a remote installer script directly to the shell.

Mitigation: Review that step before use and prefer official package-manager installation or manually verified release instructions.

Risk: API keys shown directly in shell commands may be retained in shell history.

Mitigation: Use interactive authentication helpers, environment variables, or temporary shell history controls when entering real keys.

## Reference(s):

- [OpenClaw without Claude guides](https://github.com/BlueBirdBack/openclaw-without-claude)
- [Free model comparison guide](https://github.com/BlueBirdBack/openclaw-without-claude/blob/main/guides/model-comparison.md)
- [Model migration skill source](https://github.com/BlueBirdBack/openclaw-without-claude/tree/main/skills/model-migration)
- [OpenRouter API keys](https://openrouter.ai/keys)
- [Google AI Studio](https://aistudio.google.com)
- [Ollama install instructions](https://ollama.com/install.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider recommendations, CLI commands, restart steps, and verification checks for the user's OpenClaw configuration.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
