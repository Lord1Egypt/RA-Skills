## Description:

Execute AetherLang V3 AI workflows from Claude Code using nine specialized engines for culinary, business, research, marketing, and strategic analyses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contrario](https://clawhub.ai/user/contrario)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to call AetherLang V3 workflows from Claude Code for culinary, business, research, marketing, forecasting, debate, and analysis tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted queries and AetherLang flow code are sent to the third-party AetherLang API.

Mitigation: Use the skill only for data approved for third-party processing, and avoid secrets, private files, system prompts, conversation history, and confidential business or personal data.

Risk: Optional Pro tier authentication uses an API key.

Mitigation: Store AETHER_KEY in the environment and pass it through the X-Aether-Key header; do not hardcode it in flow code or scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/contrario/skills/aetherlang-claude-code)
- [Publisher profile](https://clawhub.ai/user/contrario)
- [Project homepage](https://masterswarm.net)
- [AetherLang API endpoint](https://api.neurodoc.app/aetherlang/execute)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The API response final output is structured markdown; the skill notes responses are in Greek and typical calls take 30-60 seconds.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
