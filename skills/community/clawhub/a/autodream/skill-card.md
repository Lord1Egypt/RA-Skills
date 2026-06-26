## Description: <br>
Automatic memory consolidation for OpenClaw agents that analyzes daily memory files, removes duplicates, prunes stale entries, normalizes dates, and builds a clean MEMORY.md index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rimaslogic](https://clawhub.ai/user/rimaslogic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to consolidate scattered daily memory files into a maintained long-term MEMORY.md index, either manually or through heartbeat-based checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite long-term agent memory files. <br>
Mitigation: Run with --dry-run first, review proposed MEMORY.md changes, and keep the built-in backups enabled before allowing automatic consolidation. <br>
Risk: Heartbeat-based execution can apply memory changes without active user attention. <br>
Mitigation: Enable heartbeat consolidation only when long-term memory maintenance is intended and schedule it for quiet periods with reviewable reports. <br>
Risk: The skill depends on an external Node script or npm package to perform file changes. <br>
Mitigation: Verify the installed autodream script or package before use and install only from a trusted source. <br>


## Reference(s): <br>
- [Autodream ClawHub release](https://clawhub.ai/rimaslogic/autodream) <br>
- [Publisher profile: rimaslogic](https://clawhub.ai/user/rimaslogic) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for running memory consolidation, configuring .autodream.json, and reviewing MEMORY.md backups and reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
