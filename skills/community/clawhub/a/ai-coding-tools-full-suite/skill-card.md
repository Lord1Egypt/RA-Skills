## Description: <br>
Provides structured analysis, comparison, selection guidance, agent-design references, and prompt-engineering support for Cursor, Claude Code, Devin, Windsurf, and other AI coding tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wt865143010](https://clawhub.ai/user/wt865143010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering leads, product evaluators, and AI researchers use this skill to compare AI coding assistants, choose tools for teams or projects, design agent workflows, and improve coding prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad routing can trigger large analysis flows when user intent is ambiguous. <br>
Mitigation: Use explicit commands such as /ai-tools compare, /ai-tools analyze, /ai-tools design, or /ai-tools prompt when possible. <br>
Risk: Reference material describes file-write, shell, browser, and context-persistence capabilities of other AI coding tools. <br>
Mitigation: Treat those descriptions as analysis references only; separately approve any local tool access before an agent uses those capabilities. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wt865143010/ai-coding-tools-full-suite) <br>
- [AI coding assistant comparison reference](artifact/references/01-comparison.md) <br>
- [Cursor prompt analysis reference](artifact/references/02-cursor.md) <br>
- [Claude Code prompt analysis reference](artifact/references/03-claude-code.md) <br>
- [Devin AI agent loop analysis reference](artifact/references/04-devin.md) <br>
- [Windsurf prompt analysis reference](artifact/references/05-windsurf.md) <br>
- [AI agent design best practices reference](artifact/references/06-agent-design.md) <br>
- [Spec-driven development reference](artifact/references/07-spec-driven.md) <br>
- [AI coding tool definitions reference](artifact/references/08-tools-reference.md) <br>
- [Coding prompt engineering reference](artifact/references/09-prompt-engineering.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with comparison tables, command examples, prompt templates, and structured guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can route requests through /ai-tools, /aitools, @ai-coding-tools-full-suite, or natural-language prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
