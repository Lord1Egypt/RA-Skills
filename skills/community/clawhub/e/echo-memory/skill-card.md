## Description: <br>
Echo syncs OpenClaw markdown memory files to Supabase, with commands to sync, restore, and inspect memory state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkw-21](https://clawhub.ai/user/kkw-21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to synchronize local OpenClaw markdown memories with Supabase and restore or inspect memory sync status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload sensitive local memory files to a Supabase project. <br>
Mitigation: Verify the target Supabase project, credentials, and memory file scope before running sync commands. <br>
Risk: Restore behavior may overwrite existing local memory files. <br>
Mitigation: Back up memory files and run dry-run checks before restoring from Supabase. <br>
Risk: The executable behind echo-memory is not included in the artifact. <br>
Mitigation: Install only after verifying which echo-memory executable will run in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kkw-21/echo-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose dry-run, incremental sync, restore, and status-check commands that interact with local memory files and Supabase.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
