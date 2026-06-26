## Description: <br>
Claw Operations Manager helps OpenClaw users audit operations, manage permissions, monitor files, and create git-based snapshots with multilingual dashboard support and rollback workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3273283](https://clawhub.ai/user/a3273283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and OpenClaw teams use this skill to review operation history, manage permission rules, monitor sensitive paths, and recover from mistakes through snapshot and rollback workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise broad local command, filesystem, snapshot, and web-management authority. <br>
Mitigation: Install only in environments where that authority is intended, scope monitored and snapshotted paths deliberately, and review permission rules before use. <br>
Risk: The dashboard and management APIs may expose operational controls if reachable by other users or hosts. <br>
Mitigation: Bind the dashboard to localhost, add authentication before shared use, and avoid exposing port 8080 beyond the local machine. <br>
Risk: Shell aliases or wrappers for arbitrary commands can turn normal command execution into broad audited operations. <br>
Mitigation: Avoid aliases for untrusted or arbitrary commands, and prefer reviewed integration points with explicit command scope. <br>
Risk: Snapshots and rollback are best-effort and may not provide full recovery for all files or operational states. <br>
Mitigation: Use dry-run restore checks, keep independent backups for important data, and treat rollback as a recovery aid rather than a guaranteed backup system. <br>
Risk: Audit databases and snapshots under ~/.openclaw may retain sensitive operational data. <br>
Mitigation: Set restrictive file permissions, define retention policies, and exclude sensitive paths from default monitoring or snapshots when appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/a3273283/claw-ops-manager) <br>
- [Publisher Profile](https://clawhub.ai/user/a3273283) <br>
- [API Reference](artifact/references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and inline code or shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local dashboard/API usage guidance, audit configuration examples, snapshot and rollback commands, and integration code snippets.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
