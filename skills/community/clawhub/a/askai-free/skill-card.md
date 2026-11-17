## Description:

Use the AskAI.free API to ask available ChatGPT, Claude, and DeepSeek models, list the live model catalogue, or check token usage. Use when the user explicitly wants AskAI.free or wants a model through their AskAI account; do not use for unrelated AI requests or ASKAI media-workspace operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrick86](https://clawhub.ai/user/henrick86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users who explicitly choose AskAI.free can submit a request to an available ChatGPT, Claude, or DeepSeek model, discover available models, or check account token usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests are sent to the third-party AskAI service, and API calls consume the account's monthly token allowance.

Mitigation: Use the service only for intended requests, consider what information is included, and monitor usage when needed.

Risk: The API key could expose the user's AskAI account if disclosed.

Mitigation: Keep ASKAI_API_KEY local and secret; do not paste it into chat, commit it, put it in a URL, or send it to another host.

## Reference(s):

- [AskAI API documentation](https://askai.free/api)
- [AskAI.free skill page](https://clawhub.ai/henrick86/skills/askai-free)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Text or Markdown model response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are non-streaming; default maximum is 1,000 tokens and API calls use the account's monthly token allowance.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
