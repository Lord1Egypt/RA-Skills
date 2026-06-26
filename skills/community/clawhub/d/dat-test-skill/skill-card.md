## Description: <br>
Generates ByteRover usage and health summaries for one or more project directories, covering query activity, curate activity, file changes, durations, and quota or rate-limit errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datpham-6996](https://clawhub.ai/user/datpham-6996) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run a local ByteRover metrics script for daily health checks, project-specific usage reports, or scheduled monitoring across one or more project directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runs the local ByteRover CLI through Node tooling on selected project directories. <br>
Mitigation: Install only when the local ByteRover CLI and Node tooling are trusted, and run it only against intended project paths. <br>
Risk: Metrics reports may expose private activity, file-change counts, errors, or quota details. <br>
Mitigation: Review reports before sharing outside the workspace and redact sensitive activity or error details. <br>
Risk: Environment variables can change the command path and lookback window. <br>
Mitigation: Keep BRV_CMD and BRV_SINCE simple and trusted, especially in cron or CI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/datpham-6996/dat-test-skill) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with query activity, curate activity, quota warnings, and a status line.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include separate project sections and a combined status line for multiple project directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
