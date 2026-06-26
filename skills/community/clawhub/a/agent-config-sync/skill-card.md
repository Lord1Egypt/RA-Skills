## Description: <br>
Synchronize configuration versions across OpenClaw multi-agent deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevensongxx](https://clawhub.ai/user/stevensongxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators running two or more OpenClaw agents use this skill to initialize, dispatch, track, and roll back configuration synchronization across agent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent cross-agent configuration synchronization behavior and can write coordination files across OpenClaw workspaces. <br>
Mitigation: Install only when one OpenClaw master agent should coordinate other agents; review the generated registry and BOOTSTRAP/HEARTBEAT edits, and use dry-run or manual setup when explicit approval is needed for each write. <br>
Risk: Release evidence says the skill overstates some safety guarantees. <br>
Mitigation: Treat the documented path validation, isolation, rollback, and no-secret claims as controls to verify in the target environment before relying on them. <br>
Risk: Configuration changes and pending sync content may accidentally include secrets or sensitive operational details. <br>
Mitigation: Keep pending sync files in intended workspaces and avoid placing raw secrets in CHANGELOG entries or pending sync manifests. <br>


## Reference(s): <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Quickstart](references/quickstart.md) <br>
- [Agent Registry](references/agent-registry.json) <br>
- [Sync Setup](references/sync-setup.md) <br>
- [Pending Sync Template](references/pending-sync-template.md) <br>
- [Sync Journal](references/sync-journal.md) <br>
- [Agent Setup](references/agent-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify OpenClaw workspace files such as SYNC.md, BOOTSTRAP.md and HEARTBEAT.md additions, pending_sync manifests, version sentinels, journals, and rollback snapshots.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
