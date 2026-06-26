## Description: <br>
Generate narrative blog posts from AI coding session transcripts, selecting relevant sessions and producing agent-narrated Markdown in builder's log, tutorial, or technical deep-dive styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lordshashank](https://clawhub.ai/user/lordshashank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical writers use this skill to turn AI coding-session transcripts into publishable devlogs that explain what was built, how the human-agent collaboration unfolded, and which technical decisions mattered. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local AI coding-session transcripts, which may contain secrets, private paths, customer data, proprietary code details, or internal decisions. <br>
Mitigation: Use a specific project and time range, confirm the session index before transcript reading, and review and redact the generated Markdown before sharing or publishing. <br>
Risk: The skill can optionally publish generated Markdown to Hashnode when credentials are provided. <br>
Mitigation: Provide Hashnode credentials only when publishing is intentional, and inspect the final post content before running the publishing step. <br>


## Reference(s): <br>
- [DevLog Generator instructions](SKILL.md) <br>
- [Blog writing guide](references/blog-writing-guide.md) <br>
- [Claude Code platform reference](references/platforms/claude-code/claude-code.md) <br>
- [Codex platform reference](references/platforms/codex/codex.md) <br>
- [Gemini CLI platform reference](references/platforms/gemini-cli/gemini-cli.md) <br>
- [OpenClaw platform reference](references/platforms/openclaw/openclaw.md) <br>
- [OpenCode platform reference](references/platforms/opencode/opencode.md) <br>
- [Hashnode publishing reference](references/publishing/hashnode/hashnode.md) <br>
- [ClawHub skill listing](https://clawhub.ai/lordshashank/devlog) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown blog file with a brief text report; optional published post URL when publishing is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Mermaid diagrams in Markdown when session content involves architecture, flows, or multi-component interactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
