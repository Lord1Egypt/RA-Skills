## Description:

Ai Pair coordinates a Claude Code creator with Codex and Gemini reviewers to produce and review code, articles, scripts, newsletters, and other creative work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axtonliu](https://clawhub.ai/user/axtonliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and other external users use this skill to run a semi-automatic multi-agent workflow where one Claude Code agent creates work and Codex and Gemini provide independent review before the user decides whether to revise or pass.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts multiple agents with broad workspace access and permission bypass behavior.

Mitigation: Install at the project level when possible, use it only in workspaces where multi-agent file access is acceptable, and stop the team when the workflow is finished.

Risk: Reviewer workflows may send selected code or drafts to external Codex and Gemini CLIs.

Mitigation: Avoid secrets, credentials, customer data, regulated data, and proprietary material unless organizational policy permits those providers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axtonliu/skills/ai-pair)
- [Claude Code skills documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills)
- [Claude Code overview](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
- [OpenAI Codex CLI](https://github.com/openai/codex)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands and code-oriented review summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces creator outputs and consolidated Codex/Gemini review feedback under user-approved review steps.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
