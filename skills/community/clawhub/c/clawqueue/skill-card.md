## Description: <br>
Turn GitHub Issues into a local agent queue. GitHub issues in, agent work out. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikil511](https://clawhub.ai/user/nikil511) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to operate a local, git-backed agent queue from GitHub Issues and Project Boards, including scheduler runs, diagnostics, retries, pauses, and report/state file locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes workflows that may read GitHub issues and project boards and update boards, commits, local reports, logs, state, or issue status. <br>
Mitigation: Use restricted GitHub tokens and ClawQueue profiles limited to repositories where automated queue processing is acceptable. <br>
Risk: Generated reports, commits, and queue state may affect the user's local workspace or public/private worklog repositories. <br>
Mitigation: Review configured repository paths, profile settings, generated reports, and commits before relying on or publishing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nikil511/clawqueue) <br>
- [ClawQueue core repository](https://github.com/ClawQueue/ClawQueue) <br>
- [ClawQueue organization](https://github.com/ClawQueue) <br>
- [ClawQueue reports repository](https://github.com/ClawQueue/ClawQueue-reports) <br>
- [ClawQueue documentation](https://clawqueue.github.io/ClawQueue/) <br>
- [OpenClaw balena edge deployment repository](https://github.com/ClawQueue/openclaw-balena) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and git according to the parsed ClawHub metadata.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
