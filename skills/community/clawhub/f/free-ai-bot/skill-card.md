## Description:

Free AI Bot is a free AI aggregator that routes prompts across local Ollama models and configured free cloud providers such as Cloudflare Workers AI and Groq.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bo-aibot](https://clawhub.ai/user/bo-aibot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to ask questions through a command-line AI aggregator that prefers local Ollama models and can fall back to configured cloud AI providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default routing can send prompts to Cloudflare or Groq after local failure when cloud credentials are configured.

Mitigation: Use --provider ollama for local-only use and avoid submitting secrets or private data.

Risk: The included Python script appears broken as shipped due to syntax errors.

Mitigation: Review and test the script before operational use.

## Reference(s):

- [Free AI Bot ClawHub Page](https://clawhub.ai/bo-aibot/skills/free-ai-bot)
- [bo-aibot Publisher Profile](https://clawhub.ai/user/bo-aibot)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may come from a local model or a configured cloud provider depending on routing and credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
