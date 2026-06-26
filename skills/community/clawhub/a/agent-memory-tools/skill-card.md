## Description: <br>
Searches, stores, and manages agent memory across four sources: fact store, vector embeddings, BM25 full-text search, and a knowledge graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[primo-studio](https://clawhub.ai/user/primo-studio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to recall workspace knowledge, extract durable facts, detect contradictions, and maintain searchable local memory across fact, embedding, BM25, and graph stores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can index and retain workspace knowledge, including sensitive project notes, in local memory files. <br>
Mitigation: Set MEMORY_WORKSPACE narrowly, review or delete .cache memory files as needed, and only ingest directories intended for agent memory. <br>
Risk: Optional OpenAI, OpenRouter, or Convex configuration can send memory content to remote services despite the default local-first posture. <br>
Mitigation: For local-only use, leave convexUrl unset and avoid the openai and openrouter presets. <br>
Risk: Watch and platform auto-trigger modes can continuously ingest file changes without repeated confirmation. <br>
Mitigation: Use --scan for one-time ingestion and avoid --watch, LaunchAgent, systemd, cron, or Task Scheduler setup unless continuous ingestion is intentional. <br>


## Reference(s): <br>
- [Configuration Guide](references/configuration.md) <br>
- [Benchmark Results](references/benchmark-results.json) <br>
- [Ollama](https://ollama.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/primo-studio/agent-memory-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, terminal output, JSON configuration, and local cache files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can persist recalled and extracted workspace knowledge locally, with optional remote providers when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
