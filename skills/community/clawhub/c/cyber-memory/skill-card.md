## Description: <br>
Five-layer memory system with automatic fact extraction via local LLM (Ollama) that processes session transcripts locally with no external API required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[witnesssun](https://clawhub.ai/user/witnesssun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to preserve long-term agent memory, extract structured facts from recent sessions, and configure searchable local memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically reads private session transcripts and stores extracted facts and snapshots in local memory files. <br>
Mitigation: Review before installation when sessions may contain secrets, personal data, or proprietary work, and periodically inspect or delete files written under workspace/memory. <br>
Risk: A configurable OpenAI-compatible endpoint and API key path can send transcript-derived content outside the local machine if changed from the default. <br>
Mitigation: Keep baseUrl on localhost for private use and remove or isolate OPENAI_API_KEY unless external processing is intentional. <br>


## Reference(s): <br>
- [Cyber Memory on ClawHub](https://clawhub.ai/witnesssun/cyber-memory) <br>
- [Ollama](https://ollama.ai) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON5 configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes extracted facts, pre-compaction snapshots, and session reset logs as local Markdown files under workspace/memory.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
