## Description: <br>
Ghost Mode provides browser-style incognito behavior for an OpenClaw agent by suppressing memory writes while active and scrubbing session traces when deactivated. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stelloxx](https://clawhub.ai/user/stelloxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run private or sensitive agent sessions without adding those interactions to persistent agent memory, logs, transcripts, or search indexes. It is intended for explicit user-triggered privacy workflows such as experiments, sensitive discussions, one-off tasks, and cleanup of stale ghost sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can alter or delete session, transcript, memory, and search-index data. <br>
Mitigation: Review before installing, keep backups of important sessions, and use the documented dry-run and confirmation controls before destructive cleanup. <br>
Risk: Activation and safety boundaries may be unclear in some environments. <br>
Mitigation: Confirm OPENCLAW_WORKSPACE and OPENCLAW_HOME point only to the intended OpenClaw directories before use. <br>
Risk: Partial failures during cleanup may leave memory state inconsistent or incompletely scrubbed. <br>
Mitigation: Run the status and verification workflow after cleanup and restore from backups if the workspace is not in the expected state. <br>


## Reference(s): <br>
- [Architecture](references/ARCHITECTURE.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/stelloxx/ghost-mode) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces local command workflows and status text; it does not call external services.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
