## Description:

Persistent agent operating system for OpenClaw. Agents remember across sessions, learn from experience, coordinate on complex projects without duplicate work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocana](https://clawhub.ai/user/cryptocana)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use Agent Os to create persistent multi-agent project workflows that decompose goals, assign tasks by capability, track execution, and preserve agent and project state across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent and project state is stored locally and may include goals, outputs, blockers, errors, and lessons.

Mitigation: Do not store secrets, regulated data, or sensitive business data in persisted state; review and remove state files before sharing or deploying.

Risk: Project IDs and agent IDs influence local file paths before path validation is added.

Mitigation: Use trusted IDs only, run the skill in an isolated workspace, and add path validation before accepting user-controlled identifiers.

Risk: The dashboard renders status data with innerHTML.

Mitigation: Treat dashboard data as trusted-only until rendering is changed to escape or sanitize untrusted values.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cryptocana/skills/agent-os)
- [README.md](artifact/README.md)
- [ARCHITECTURE.md](artifact/ARCHITECTURE.md)
- [BUILD_SUMMARY.md](artifact/BUILD_SUMMARY.md)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript examples, shell commands, and JSON state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local files under data/ for persisted agent and project state.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
