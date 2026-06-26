## Description: <br>
ClawDNA helps an OpenClaw agent suggest, review, and run identity backup, sync, restore, and recovery workflows with the ClawDNA CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitpcl](https://clawhub.ai/user/gitpcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to keep identity files backed up, detect drift, review sync changes, and recover agent identity on new or broken machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup, pull, restore, clone, and fleet sync workflows can change or overwrite local identity files. <br>
Mitigation: Review diffs and use snapshots or dry-run options before applying sync or restore operations. <br>
Risk: Identity files and hub configuration can expose sensitive personal, agent, or token-related data if handled carelessly. <br>
Mitigation: Keep secrets and hub tokens out of identity files, use environment variables such as CLAWDNA_HUB_TOKEN for hub authentication, and address sanitizer findings before exporting or syncing. <br>
Risk: The background daemon can automatically sync identity changes after it is enabled. <br>
Mitigation: Enable the daemon only when ongoing automatic sync is intended, and review daemon status and configuration with clawdna doctor or daemon status. <br>


## Reference(s): <br>
- [ClawDNA Documentation](https://github.com/clawco-io/clawdna#readme) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend ClawDNA CLI commands such as snapshot, diff, push, pull, restore, clone, fleet, daemon, and doctor.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
