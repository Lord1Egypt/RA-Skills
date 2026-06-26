## Description: <br>
Persistent semantic memory for AI agents. Store, search, recall, and forget memories across sessions using Qdrant + FastEmbed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[escapethefate1991](https://clawhub.ai/user/escapethefate1991) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Engram Memory to give OpenClaw or MCP-compatible agents persistent local memory for storing, searching, recalling, and deleting semantically indexed notes across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist user content and recall it in later sessions. <br>
Mitigation: Avoid storing secrets or regulated data, and disable autoCapture or autoRecall for sensitive work. <br>
Risk: Setup can make lasting local environment changes. <br>
Mitigation: Inspect shell startup file changes after setup and keep only the entries required for the deployment. <br>
Risk: The memory backend depends on local Qdrant and FastEmbed services. <br>
Mitigation: Keep those services bound to trusted local interfaces and review service exposure before use on shared systems. <br>
Risk: Query-based deletion can remove the closest matching memory rather than an exact intended item. <br>
Mitigation: Prefer deletion by explicit memory ID when removing important or sensitive entries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/escapethefate1991/engrammemory) <br>
- [Quick Start Guide](docs/QUICK_START.md) <br>
- [Architecture Overview](docs/ARCHITECTURE.md) <br>
- [OpenClaw Integration Guide](docs/OPENCLAW_INTEGRATION.md) <br>
- [Community Edition Scope](docs/LIMITATIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands, guidance] <br>
**Output Format:** [Text and JSON-like tool results with markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists user-provided memory content in a local Qdrant collection and returns semantic search or recall results to the agent.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
