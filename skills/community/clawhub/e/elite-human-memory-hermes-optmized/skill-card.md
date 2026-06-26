## Description: <br>
Hermes-optimized human-like memory system with semantic search, auto-promotion, conflict resolution, and direct integration with the Hermes memory tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cliftonwknox](https://clawhub.ai/user/cliftonwknox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Hermes agent users use this skill to add structured long-term memory, semantic retrieval, promotion review, and conflict handling to agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store and recall broad user context, which may include sensitive information if memory behavior is not configured. <br>
Mitigation: Confirm storage paths before use, gate or disable automatic writes where appropriate, and exclude secrets, credentials, health, financial, and private customer details by default. <br>
Risk: Stale or conflicting memories may influence later agent responses. <br>
Mitigation: Review saved memories, conflict logs, confidence fields, and expiry fields regularly, and require user confirmation before promoting or resolving higher-risk memories. <br>


## Reference(s): <br>
- [README.md](artifact/README.md) <br>
- [INTEGRATION.md](artifact/INTEGRATION.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with structured memory entries and source references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update MEMORY.md, daily memory files, conflict logs, and vector indexes when the agent has file and embedding access.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact docs mention 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
