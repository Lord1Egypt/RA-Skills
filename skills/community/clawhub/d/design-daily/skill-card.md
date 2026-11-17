## Description:

Daily design industry brief for UI/UX designers and PMs that covers AI and design, design engineering, product experience breakdowns, and design decision logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkk0124](https://clawhub.ai/user/tkk0124)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, product managers, and design-focused teams use this skill to generate a daily Chinese-language design brief from recent search results and configured role preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be stored in a local plaintext .env file when the setup wizard is used.

Mitigation: Prefer runtime environment variables; if a .env file is used, restrict its file permissions and avoid sharing archives or logs that include it.

Risk: The setup flow presents a cron command based on the installation path, which can be unsafe if the path contains spaces or shell metacharacters.

Mitigation: Review the cron entry before copying it, quote or escape paths as needed, and install the skill in a simple trusted path.

Risk: Search result material and configured design preferences are sent to external Serper and DeepSeek APIs.

Mitigation: Use non-sensitive role and preference data, and confirm external API use is acceptable before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tkk0124/skills/design-daily)
- [Serper search API](https://google.serper.dev/search)
- [DeepSeek chat completions API](https://api.deepseek.com/chat/completions)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown-style setup guidance; runtime output is a plain text brief and a JSON brief record.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SERPER_API_KEY and DEEPSEEK_API_KEY. Normal runs write dated brief files under logs/; preview mode prints without saving.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
