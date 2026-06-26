## Description: <br>
ClankerHive is a SQLite-backed shared context store for coordinating state across multiple agent sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use ClankerHive to coordinate OpenClaw sessions, share short-lived facts, pass alerts, and claim tasks to avoid duplicate work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared facts and alerts can expose sensitive or stale local state if the database path is readable by others or retained too long. <br>
Mitigation: Keep the database path private, use restrictive file permissions, prefer short TTLs, and avoid storing secrets or sensitive user data. <br>
Risk: Agents may make automated decisions from outdated or unvalidated coordination values. <br>
Mitigation: Validate stored values before using them to trigger actions, and expire coordination facts with TTLs where possible. <br>


## Reference(s): <br>
- [ClankerHive ClawHub release](https://clawhub.ai/pfrederiksen/clankerhive) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands return plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands coordinate through a local SQLite database selected by CLANKERHIVE_DB or the default ~/.openclaw/hive.db path.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
