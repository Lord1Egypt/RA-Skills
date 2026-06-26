## Description: <br>
Coordinates AI agent teams where one Claude Code agent creates code or content and Codex and Gemini reviewers provide parallel feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axtonliu](https://clawhub.ai/user/axtonliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and content teams use this skill in Claude Code to create a development or content team, produce work, and request parallel Codex and Gemini review before revising or accepting the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent teams can read local project files and send code or drafts to external Codex and Gemini CLI sessions. <br>
Mitigation: Use only in projects approved for those tools, avoid secrets or confidential, customer, unpublished, or regulated data, and review material before sending it for review. <br>
Risk: Long-lived agents with broad local authority may continue holding project context after the immediate task is complete. <br>
Mitigation: Start the team only in the intended workspace, keep the semi-automatic approval steps in place, review generated changes before relying on them, and run /ai-pair team-stop when finished. <br>


## Reference(s): <br>
- [Ai Pair on ClawHub](https://clawhub.ai/axtonliu/ai-pair) <br>
- [Claude Code Skills Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills) <br>
- [Claude Code Overview](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) <br>
- [OpenAI Codex CLI](https://github.com/openai/codex) <br>
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) <br>
- [Dev Team Example](examples/dev-team.md) <br>
- [Content Team Example](examples/content-team.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured review reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify project files through Claude Code agents and may invoke authenticated Codex and Gemini CLI sessions.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact metadata reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
