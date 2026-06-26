## Description: <br>
Local-first persistent memory for AI agents with SQLite storage, orchestrated retrieve/extract loops, hybrid retrieval, contradiction checks, correction learning, and optional SuperMemory mirroring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DobrinAlexandru](https://clawhub.ai/user/DobrinAlexandru) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Agent Brain to give an AI agent persistent local memory across sessions, including retrieval, fact extraction, conflict checks, corrections, and workflow pattern tracking. It is intended for agents that should apply remembered project context, user preferences, procedures, and learned corrections while responding to new tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to store user, project, preference, workflow, and correction information persistently across sessions. <br>
Mitigation: Install it only where persistent memory is desired, review exported or database-backed memory regularly, and avoid using it with sensitive or regulated data unless storage and export controls are in place. <br>
Risk: Stored memory can be mirrored to SuperMemory or sent to configured remote embedding services when those options are enabled. <br>
Mitigation: Keep AGENT_BRAIN_SUPERMEMORY_SYNC=off unless cloud sync is intentional, and configure remote embedding URLs only to trusted services. <br>
Risk: URL ingestion can introduce external content and may carry SSRF or untrusted-content risks if enabled without review. <br>
Mitigation: Keep ingest disabled unless explicitly needed, allow only reviewed public HTTPS URLs, and run conflict checks before storing ingested claims. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DobrinAlexandru/agent-brain) <br>
- [Agent Brain Homepage](https://github.com/alexdobri/agent-brain) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing memory operations and recommendations; persistent data is stored locally by default with optional configured remote mirroring.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
