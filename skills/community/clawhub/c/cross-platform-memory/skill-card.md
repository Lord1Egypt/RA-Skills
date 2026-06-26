## Description: <br>
Injects recent Telegram, Discord, and local memory context into OpenClaw gateway requests so agents can maintain continuity across channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dq-stack](https://clawhub.ai/user/dq-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of OpenClaw deployments use this skill to bring recent Telegram, Discord, MEMORY.md, and daily-note context into gateway requests. It is intended for agents that need continuity across chat channels while preserving source labels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse private Telegram, Discord, MEMORY.md, and daily-note content across OpenClaw channels. <br>
Mitigation: Enable it only for intended deployments, restrict configured paths, add per-source opt-in controls, and review or redact sensitive memory content before use. <br>
Risk: Recalled chat content may contain untrusted or misleading instructions that influence agent responses. <br>
Mitigation: Treat recalled conversations as quoted user context rather than system-level instructions, preserve platform labels, and review outputs before relying on them. <br>


## Reference(s): <br>
- [memory-bridge.ts](references/memory-bridge.ts) <br>
- [ClawHub release page](https://clawhub.ai/dq-stack/cross-platform-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript code and shell command snippets; the runtime helper returns a plain text memory context string.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads the most recent session JSONL file, includes MEMORY.md and daily notes when present, defaults to 8 messages per platform, and filters messages older than 20 hours when timestamps are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
