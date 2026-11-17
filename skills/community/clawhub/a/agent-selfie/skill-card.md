## Description:

AI agent self-portrait generator. Create avatars, profile pictures, and visual identity using Gemini image generation. Supports mood-based generation, seasonal themes, and automatic style evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iisweetheartii](https://clawhub.ai/user/iisweetheartii)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to generate avatar, banner, and full-body visual identity assets for AI agents from a personality profile, mood, and seasonal theme.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can call Gemini with the user's API key and generate files locally.

Mitigation: Install and run it only in environments where local file creation and Gemini API use are approved; keep GEMINI_API_KEY out of committed files and shell-history-heavy workflows.

Risk: Heartbeat workflows may encourage recurring public avatar changes or memory writes without enough review.

Mitigation: Require explicit human review of each generated image and approval of each target account before changing Discord, Twitter/X, AgentGram, or other public avatars.

## Reference(s):

- [ClawHub Agent Selfie](https://clawhub.ai/iisweetheartii/skills/agent-selfie)
- [Google AI Studio API Key](https://aistudio.google.com/apikey)
- [OpenClaw](https://openclaw.org)
- [AgentGram](https://clawhub.org/skills/agentgram)
- [Gemini Image Gen](https://clawhub.org/skills/gemini-image-gen)
- [OpenCode OMO](https://clawhub.org/skills/opencode-omo)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands; generated PNG files, prompts.json, and an HTML gallery when the script is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+ and GEMINI_API_KEY; can write generated image assets to a local output directory.]

## Skill Version(s):

1.2.1 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
