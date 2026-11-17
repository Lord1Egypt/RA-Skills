## Description:

9Router local/remote AI gateway. OpenAI-compatible REST for chat, image, TTS, STT, embeddings, web search/fetch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deyogaid](https://clawhub.ai/user/deyogaid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this skill to configure a local or remote 9Router gateway, discover available models, and form authenticated API requests for chat, media, embeddings, web, and vision capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote gateway access without authentication and HTTPS can expose access or traffic.

Mitigation: Use a trusted gateway and enable authentication and HTTPS for remote access.

Risk: Automatic provider fallback may send content to providers the user did not expect.

Mitigation: Check which providers may receive content through fallback before sending requests.

Risk: The linked capability instructions can change at their source URLs.

Mitigation: Review fetched capability instructions before relying on them.

## Reference(s):

- [9Router chat and code generation capability guide](https://raw.githubusercontent.com/decolua/9router/refs/heads/master/skills/9router-chat/SKILL.md)
- [9Router image generation capability guide](https://raw.githubusercontent.com/decolua/9router/refs/heads/master/skills/9router-image/SKILL.md)
- [9Router text-to-speech capability guide](https://raw.githubusercontent.com/decolua/9router/refs/heads/master/skills/9router-tts/SKILL.md)
- [9Router speech-to-text capability guide](https://raw.githubusercontent.com/decolua/9router/refs/heads/master/skills/9router-stt/SKILL.md)
- [9Router embeddings capability guide](https://raw.githubusercontent.com/decolua/9router/refs/heads/master/skills/9router-embeddings/SKILL.md)
- [9Router web search capability guide](https://raw.githubusercontent.com/decolua/9router/refs/heads/master/skills/9router-web-search/SKILL.md)
- [9Router web fetch capability guide](https://raw.githubusercontent.com/decolua/9router/refs/heads/master/skills/9router-web-fetch/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
