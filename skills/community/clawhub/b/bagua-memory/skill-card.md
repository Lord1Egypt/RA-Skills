## Description: <br>
Bagua Memory is a file-based AI agent memory management framework that organizes local memories into eight categories with lifecycle decay and associative retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuanyizhi](https://clawhub.ai/user/xuanyizhi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to initialize and maintain a local long-term memory system for an AI agent. It guides memory writing, retrieval, archival, compression, recovery, and user-requested deletion across a workspace's memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add persistent agent memory rules and save conversation-derived data in local files. <br>
Mitigation: Review the injected AGENTS.md, SOUL.md, and HEARTBEAT.md text before activation, run initialization manually, and avoid use in workspaces that may contain secrets, regulated data, or private personal details that should not be retained. <br>
Risk: Persistent memory may retain outdated or unwanted information if users do not manage it. <br>
Mitigation: Use the documented deletion path for user-requested forgetting and perform regular archive, compression, and index maintenance. <br>


## Reference(s): <br>
- [architecture.md](references/architecture.md) <br>
- [soul-inject.md](references/soul-inject.md) <br>
- [heartbeat-inject.md](references/heartbeat-inject.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands and file-edit instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Initializes local memory directories and Markdown files when run manually.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
