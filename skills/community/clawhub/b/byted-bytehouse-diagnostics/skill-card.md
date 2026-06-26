## Description: <br>
ByteHouse cluster diagnostics and health-check tooling for checking cluster health, diagnosing issues, reviewing node status, and analyzing cluster performance metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to run ByteHouse cluster health checks, inspect node, replica, partition, mutation, and system-table status, and review recent query history. It produces diagnostic summaries and JSON reports that help triage ByteHouse cluster issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches unpinned external ByteHouse MCP code at runtime and passes database credentials plus the shell environment to it. <br>
Mitigation: Pin the MCP server to a reviewed commit or release, run it from a clean environment containing only required ByteHouse variables, and use a least-privileged read-only ByteHouse account. <br>
Risk: Generated diagnostic reports may contain sensitive cluster, database, node, or query metadata. <br>
Mitigation: Protect report files and redact sensitive details before sharing them outside the intended operational audience. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/byted-bytehouse-diagnostics) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated JSON diagnostic reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are written to an output directory with timestamped filenames.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
