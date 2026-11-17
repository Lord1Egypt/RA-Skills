## Description:

Run AIMLAPI LLM and reasoning workflows through chat completions with retries, structured outputs, and explicit User-Agent headers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aimlapihello](https://clawhub.ai/user/aimlapihello)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw/Codex users use this skill to run AIMLAPI chat-completion and reasoning calls, including structured JSON responses, with retry and User-Agent handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, system messages, selected extra JSON fields, and the AIMLAPI API key are sent to AIMLAPI.

Mitigation: Use the skill only with data approved for AIMLAPI, avoid sensitive or private prompt content, and provide credentials through AIMLAPI_API_KEY or a secured --apikey-file.

Risk: The --output option writes full response JSON to a user-selected path.

Mitigation: Choose output paths deliberately and avoid writing responses containing sensitive content to shared or unintended locations.

## Reference(s):

- [AIMLAPI LLM notes](references/aimlapi-llm.md)
- [Skill README](README.md)
- [ClawHub skill page](https://clawhub.ai/aimlapihello/skills/aiml-llm-reasoning)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print model response text to stdout or write full response JSON to a user-selected output path.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
