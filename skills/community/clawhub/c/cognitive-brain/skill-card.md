## Description: <br>
Provides a cross-session AI memory and cognition system with four-layer memory, real-time sharing, free thinking, prediction, and knowledge visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aboutyao](https://clawhub.ai/user/aboutyao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Cognitive Brain to store, retrieve, and inject long-lived memory across OpenClaw sessions with PostgreSQL-backed recall, CLI commands, and hooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent cross-session memory can retain broad conversation history with limited privacy disclosure or user control. <br>
Mitigation: Install only when persistent memory is intended, review what session data is scanned, and confirm users can inspect, disable, and delete stored memories. <br>
Risk: Database-backed memory may expose sensitive context if configured with broad privileges or shared credentials. <br>
Mitigation: Use a dedicated local PostgreSQL account with least-privilege permissions and avoid running setup or runtime processes as root on sensitive hosts. <br>
Risk: Automatic setup and dependency installation can alter host services or pull packages during installation. <br>
Mitigation: Review setup scripts and regenerate dependencies from trusted HTTPS registries before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aboutyao/cognitive-brain) <br>
- [Cognitive Brain Documentation](docs/README.md) <br>
- [Architecture Guide](docs/ARCHITECTURE.md) <br>
- [Install Guide](docs/INSTALL_GUIDE.md) <br>
- [Cognitive Recall Hook](hooks/cognitive-recall/HOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JavaScript examples, JSON configuration, and runtime memory context] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent memory records and recall context backed by PostgreSQL, with optional Redis caching.] <br>

## Skill Version(s): <br>
7.0.1 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
