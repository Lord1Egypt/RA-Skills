## Description:

AgentScout discovers trending AI agent projects on GitHub and generates Xiaohongshu-ready tutorials, copy, cover images, and project metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auxito](https://clawhub.ai/user/auxito)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical content creators, and agent operators use AgentScout to find promising AI agent repositories, rank candidates, analyze selected projects, and generate publish-ready social content and visual assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted GitHub repository content can influence generated LLM output and browser-rendered image content.

Mitigation: Review generated analysis, posts, images, and commands before publishing or copying them, and run the skill in an isolated environment until prompt-injection handling and HTML escaping are improved.

Risk: Repository content and generated prompts may be sent to configured LLM or image providers.

Mitigation: Use approved providers, avoid private or sensitive repositories, and configure a low-scope GitHub token.

Risk: External URL and dependency controls are not described as fully hardened in the security evidence.

Mitigation: Restrict the runtime network environment where practical and review dependencies before deployment.

## Reference(s):

- [AgentScout ClawHub listing](https://clawhub.ai/auxito/skills/agentscout)
- [auxito publisher profile](https://clawhub.ai/user/auxito)

## Skill Output:

**Output Type(s):** [text, markdown, images, json, shell commands, configuration, guidance]

**Output Format:** [Markdown files, JSON metadata, generated image files, and concise command/configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated artifacts under an output directory for the selected project.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
