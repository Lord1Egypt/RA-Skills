## Description: <br>
Auto-backup and sync engine for AI agent workspaces that commits and pushes Git changes, backs up critical state to Supabase, stores memories with mem0, and captures state snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run backup workflows for AI agent workspaces, including Git synchronization, cloud state backup, and searchable memory persistence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports broad unauthenticated controls that can commit, push, and persist workspace data to external services. <br>
Mitigation: Review carefully before installing, run only in an isolated workspace with test data, and add authentication before exposing the HTTP API. <br>
Risk: Backup operations can send workspace data to Git remotes, Supabase, and mem0. <br>
Mitigation: Require explicit opt-in for each destination, use narrow file allowlists, exclude secrets, and disclose what data is sent before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/evezart/evez-backup-sync) <br>
- [Publisher profile](https://clawhub.ai/user/evezart) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Files] <br>
**Output Format:** [JSON API responses and command-line execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local backup state files and trigger Git commits, Git pushes, Supabase writes, or mem0 memory writes when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
