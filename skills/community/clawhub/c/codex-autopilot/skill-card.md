## Description: <br>
Multi-model AI coding automation system with intelligent task routing and built-in CI/CD. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imwyvern](https://clawhub.ai/user/imwyvern) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate long-running Codex, Gemini, and Claude/OpenClaw coding workflows across multiple repositories. It helps route tasks, monitor tmux sessions, enqueue fixes, run reviews, and trigger test or coverage follow-up work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic permission approval, yolo/full-auto modes, and branch auto-merge can allow broad repository changes with limited confirmation. <br>
Mitigation: Install only in trusted, isolated repositories; disable automatic permission approval, yolo/full-auto modes, and branch auto-merge unless explicitly needed. <br>
Risk: Repository-defined shell checks, fallback agents, and task dispatch can run project commands or control coding agents continuously. <br>
Mitigation: Review scripts and configuration before deployment, use least-privilege tokens, and keep the skill away from secrets and production branches until behavior is verified. <br>
Risk: External Telegram and Discord notifications can expose project state or task content to configured channels. <br>
Mitigation: Use private channels, restrict bot and webhook credentials, and remove external notifications when they are not required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/imwyvern/codex-autopilot) <br>
- [Codex Autopilot README](README.md) <br>
- [Code Review Reference](code-review/references/README.md) <br>
- [Branch Isolation Design](docs/branch-isolation-design.md) <br>
- [Test Agent Design](docs/test-agent-design.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [OpenAI Codex](https://github.com/openai/codex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for agent-facing workflow automation and operational guidance.] <br>

## Skill Version(s): <br>
0.7.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
