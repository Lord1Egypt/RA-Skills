## Description: <br>
Compresses long agent conversations with a tiered strategy that preserves goals, decisions, preferences, and active work while summarizing useful context into a structured memory file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizlzzzz](https://clawhub.ai/user/lizlzzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to compress lengthy conversation history while retaining important user preferences, decisions, active tasks, and concise summaries. It can be invoked manually or connected to compatible PreCompact/PostCompact hooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation compression may persist sensitive details such as credentials, account data, private paths, or configuration into long-term memory. <br>
Mitigation: Review compressed memory before retaining it, exclude secrets and private account details, and periodically inspect or delete the memory file. <br>
Risk: Optional PreCompact/PostCompact hooks can cause memory updates to run automatically. <br>
Mitigation: Enable automatic hooks only after reviewing the hook configuration and confirming that automatic memory updates are desired. <br>
Risk: The skill asks the agent to preserve key credentials or config as important context. <br>
Mitigation: Treat that instruction as a persistence risk and redact credentials, tokens, sensitive paths, and private configuration before writing memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lizlzzzz/context-compression-claude-code) <br>
- [memory-template.md](artifact/memory-template.md) <br>
- [setup-hook.md](artifact/setup-hook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with memory-template content and optional hook configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update or guide creation of a long-term memory file during compression.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
