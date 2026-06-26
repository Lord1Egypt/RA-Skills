## Description: <br>
Safely rename or migrate an OpenClaw agent by updating config and naming, migrating session content, fixing session metadata, restarting, verifying, and asking separately before deleting the old agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kid0114](https://clawhub.ai/user/kid0114) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to rename or migrate OpenClaw agents while keeping configuration, workspace paths, session content, and session display metadata consistent. It supports a cautious migration flow that verifies the new agent before asking separately about deleting the old one. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-permission helper scripts can make persistent local changes and copy session data. <br>
Mitigation: Back up OpenClaw configuration and agent/session directories before use, review planned changes, and verify the migrated agent before cleanup. <br>
Risk: Unvalidated agent IDs may cause scripts to inspect or copy unintended paths under the OpenClaw agent directory. <br>
Mitigation: Use simple, expected agent IDs and inspect command output before copying session content or deleting old agent data. <br>
Risk: Deleting the old agent too early can remove data still needed for rollback or verification. <br>
Mitigation: Delete old agent data only after separate user confirmation, optional backup, and successful verification of the migrated agent. <br>


## Reference(s): <br>
- [Agent Migration Checklist](references/checklist.md) <br>
- [Cleanup Notes](references/cleanup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kid0114/agent-migration) <br>
- [Publisher Profile](https://clawhub.ai/user/kid0114) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and checklist guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide persistent local changes to OpenClaw configuration, agent directories, workspace paths, and session metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
