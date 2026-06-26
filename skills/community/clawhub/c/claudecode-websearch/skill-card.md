## Description: <br>
Free web search using Claude Code CLI or Codex CLI's built-in WebSearch tool, without requiring Tavily, Brave, or Exa API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinghan23](https://clawhub.ai/user/jinghan23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run concise web searches through an installed Claude Code or Codex CLI when no third-party search API is configured or quota remains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent through the installed Claude or Codex CLI and may include sensitive information if users paste it into the query. <br>
Mitigation: Use the skill for ordinary web searches only and avoid secrets, confidential project names, private URLs, regulated data, or credentials. <br>
Risk: The optional global alias creates a persistent command shortcut on the user's PATH. <br>
Mitigation: Create the ccws alias only when a persistent shortcut is desired and the target script location is trusted. <br>
Risk: The skill depends on whichever Claude Code or Codex CLI is installed and authenticated locally. <br>
Mitigation: Confirm the CLI installation, authentication state, and account trust before installing or running the wrapper. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jinghan23/claudecode-websearch) <br>
- [Claude Code CLI](https://claude.ai/code) <br>
- [OpenAI Codex CLI](https://openai.com/codex) <br>
- [OpenAI Codex repository](https://github.com/openai/codex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise text or Markdown summaries with source URLs, plus shell command examples for setup and use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output depends on the installed and authenticated Claude Code or Codex CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
