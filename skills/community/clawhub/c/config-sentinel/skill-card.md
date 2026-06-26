## Description: <br>
A strict guardrail for OpenClaw config changes that snapshots before editing, validates after editing, and rolls back immediately when config health fails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike-alford](https://clawhub.ai/user/mike-alford) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when modifying OpenClaw configuration to create recoverable snapshots, validate JSON structure and bindings, and roll back unsafe changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local OpenClaw config backups may contain tokens or account details. <br>
Mitigation: Keep the sentinel backup directory private, preserve owner-only permissions, and avoid sharing backup or log files. <br>
Risk: Unapproved or unvalidated config edits can break agent routing, bindings, startup behavior, or multi-agent setups. <br>
Mitigation: Get explicit user approval, run pre-change before editing, validate after editing, and roll back immediately if validation fails. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks and plain status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; the helper can create local backup and log files under the sentinel state directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
