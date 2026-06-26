## Description: <br>
Helps an agent read PDF and text documents, track learning progress across sessions, resume from saved positions, and persist document-derived notes in long-term memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzqzuigao-ui](https://clawhub.ai/user/yzqzuigao-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to turn large documents into resumable learning sessions with saved progress, summaries, and searchable memory notes. It is most useful for technical manuals, books, specifications, and other long-form reference material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document summaries, file paths, reading history, and progress data may persist locally in MEMORY.md, daily notes, and progress JSON files. <br>
Mitigation: Use the skill only with documents suitable for local persistence, and review or delete generated memory and progress files when they contain confidential or personal information. <br>


## Reference(s): <br>
- [Quick Start Guide](artifact/references/quick-start.md) <br>
- [Memory Integration Guide](artifact/references/memory_integration.md) <br>
- [ClawHub release page](https://clawhub.ai/yzqzuigao-ui/document-learning) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with optional JSON progress files and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local MEMORY.md notes, dated memory entries, document progress JSON, and optional extracted-text JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
