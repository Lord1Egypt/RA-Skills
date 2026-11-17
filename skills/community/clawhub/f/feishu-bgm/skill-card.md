## Description:

Feishu BGM helps an agent generate instrumental background music for Feishu group-chat scenarios using MiniMax Music and send the resulting audio back to the group.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylinr](https://clawhub.ai/user/kylinr)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team facilitators can ask an agent in a Feishu group for context-appropriate instrumental BGM for meetings, brainstorming, overtime work, reviews, and similar workplace moments. The skill guides the agent to build a music prompt, invoke MiniMax generation, and return the MP3 audio file to the group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run command-line music generation and setup commands.

Mitigation: Review commands before execution, prefer pinned local dependencies, and require explicit user confirmation before invoking generation from a Feishu group.

Risk: BGM prompts may include sensitive meeting, project, or workplace context sent to an external music generation service.

Mitigation: Avoid confidential meeting or project details in BGM requests and keep prompts limited to broad mood, style, and scene descriptors.

Risk: Generated output paths and downloaded audio URLs are used before returning files to the group.

Mitigation: Sanitize output filenames and validate downloaded audio URLs before sending generated files back to the Feishu group.

## Reference(s):

- [MiniMax CLI](https://github.com/MiniMax-AI/cli)
- [MiniMax Token Plan](https://platform.minimaxi.com/subscribe/token-plan)
- [MiniMax Token Plan Global](https://platform.minimax.io/subscribe/token-plan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with shell commands and generated MP3 file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to guide an agent through MiniMax authentication, instrumental music generation, and Feishu audio-file delivery.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
