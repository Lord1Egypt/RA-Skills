## Description: <br>
Automatically captures corrections, command failures, and reusable discoveries into local `.learnings` files using signal-based filtering, retention scoring, and promotion of repeated patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omaression](https://clawhub.ai/user/omaression) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep local learning notes focused on reusable corrections, failures, feature requests, and workflow discoveries. It helps agents retain high-value lessons while pruning stale or low-value entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local learning notes may accidentally include secrets, personal data, or sensitive project details. <br>
Mitigation: Review `.learnings` periodically and avoid storing secrets or personal data in learned entries. <br>
Risk: Retention cleanup can archive or delete learning entries. <br>
Mitigation: Use `--dry-run` or keep backups before applying cleanup decisions. <br>


## Reference(s): <br>
- [Auto Improving Agent ClawHub release](https://clawhub.ai/omaression/auto-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, local markdown learning entries, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local `.learnings` files and may archive or delete stale entries when retention cleanup runs without `--dry-run`.] <br>

## Skill Version(s): <br>
1.0.0-alpha (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
